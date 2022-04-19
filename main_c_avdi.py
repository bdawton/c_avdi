import os
import glob
import wave
import struct
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import seaborn as sns
import tailored_prs as prs
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import copy
from itertools import chain
from quantiser import quantiser
from feature_extraction import extract_features
from evaluate_validate import validate
import time

abs_path = os.path.abspath(__file__)
abs_dir = os.path.dirname(abs_path)
data_folder = abs_dir + '/VehicleData'
group_list = glob.glob(data_folder + '/*')
remove_list = (data_folder + "/G10", data_folder + "/G15")

for r in remove_list:
    group_list.remove(r)

"""# Simulation Parameters"""
rand_seed = 0
exclude_types = ['Bus', 'Truck']
x_hold = {}
y_hold = {}
big_table_data = {}
big_table_label = {}
target_types = None
type_ids = None

for group in group_list:

    """# load wav files"""

    file_list = glob.glob(group + '/*/*')
    group_name = os.path.basename(group)
    print(f"loading in {group_name}")
    label_str = np.array(list(map(lambda xl: os.path.basename(os.path.dirname(xl)), file_list)))
    vehicle_types = np.array(['NoVeh', 'Car', 'Scooter', 'Bus', 'Truck'])
    # vehicle_types = np.unique(label_str)  # to automatically extract vehicle types, use this line
    type_ids = dict(zip(range(len(vehicle_types)), vehicle_types))
    raw_label = np.empty(len(label_str), dtype=int)
    for k, v in type_ids.items():
        raw_label[label_str == v] = k

    data = None
    for i in range(len(file_list)):
        with wave.open(file_list[i], 'rb') as w:
            num_sample = w.getnframes()
            sample_size = w.getsampwidth()
            f_sim = w.getframerate()
            ch = w.getnchannels()
            # read all the data
            raw_data = w.readframes(num_sample)

        # allocate memory for output
        if data is None:
            data = np.empty([len(raw_label), num_sample * ch], dtype=int)
        # convert binary to integer
        pack_str = '<{0}{1}'.format(num_sample * ch, {1: 'b', 2: 'h', 3: 'i', 4: 'i', 8: 'q'}[sample_size])
        data[i, :] = np.array(list(struct.unpack(pack_str, raw_data)))

    big_table_label[group_name] = raw_label
    big_table_data[group_name] = data
    big_table_temp = copy.deepcopy(big_table_data)

"""# random demodulation"""

f_upper_band = 3000
f_prs = f_upper_band * 2
sample_freq = f_prs / 2
f_cutoff = sample_freq / 2

sequence_root_1 = prs.prs(0.001, 0, 1, 2, f_prs, 0)
sequence_1 = np.tile(sequence_root_1, int(f_sim / f_prs))
sequence_root_2 = prs.prs(0.999, 0, 0, 2, f_prs, 0)
sequence_2 = np.tile(sequence_root_2, int(f_sim / f_prs))
sequence = sequence_1 * sequence_2

for entry in big_table_data:
    input_sigs = big_table_data[entry]
    label = big_table_label[entry]

    # mix
    mixed = sequence * input_sigs

    """# LPF (< 1.5kHz)"""

    lpf = signal.butter(2, f_cutoff, btype='lowpass', fs=f_prs)
    lpf_mixed = signal.lfilter(lpf[0], lpf[1], mixed, axis=1)

    """# sampling @3kHz"""

    B = 12
    scaling_factor = int(f_sim / f_prs)
    downsample_interval = int(scaling_factor * f_prs / sample_freq)
    start = 0
    sampled_data = lpf_mixed[:, start::downsample_interval]
    quant_sampled_data = quantiser(sampled_data, B, axis=1, dec_points=2)

    """# feature extraction"""

    # extraction time
    start_time = time.time()
    features, feature_names = extract_features(quant_sampled_data)
    print("time elapsed: {:.2f}s".format(time.time() - start_time))

    """# vehicle type estimation """

    # exclude vehicle types specified by exclude_types

    target_types = {k: v for k, v in type_ids.items() if v not in exclude_types}

    # separate data and labels

    x = features[np.isin(label, list(target_types.keys())), :]
    y = label[np.isin(label, list(target_types.keys()))]
    x_hold[entry] = x
    y_hold[entry] = y

"""# Perform classification"""
# Final matrix, labels, and predictions
iter_conf_mat = np.zeros([3, 3], dtype=int)
y_true_list = []  # The resampled test data used in "evaluate" function
y_pred_list = []  # The outputted predictions are already "resampled" as they are obtained from resampled test data

# Perform procedure 10 times to account for differences due to the random undersampling
for itr in range(10):
    print(f"validation iteration: {itr}")
    # Matrix for each successive test group
    group_conf_mat = np.zeros([3, 3], dtype=int)

    for group in group_list:
        group_name = os.path.basename(group)
        print(f"current test group: {group_name}")

        x_temp = copy.deepcopy(x_hold)
        y_temp = copy.deepcopy(y_hold)

        x_test = x_temp.pop(group_name)
        y_test = y_temp.pop(group_name)
        x_train = np.concatenate(list(chain(x_temp.values())))
        y_train = np.concatenate(list(chain(y_temp.values())))

        orig_model = RandomForestClassifier(n_estimators=1000, min_samples_leaf=3, random_state=rand_seed, n_jobs=-1) # n_jobs is -1 for multithreading
        score, conf_mat, fit_model, y_pred, y_true, unused_var = validate(x_train, y_train, x_test, y_test, orig_model,
                                                              random_state=rand_seed)
        y_true_list.append(y_true)
        y_pred_list.append(y_pred)
        group_conf_mat += conf_mat

    iter_conf_mat += group_conf_mat

""""# Set plotting parameters for use in Latex publication """

plt.rcParams['font.family'] = 'Times'
plt.rcParams['font.size'] = 22
plt.rcParams['ps.useafm'] = True
plt.rcParams['pdf.use14corefonts'] = True
plt.rcParams['text.usetex'] = True

""""# Plot confusion matrix """

iter_conf_mat_labels = np.array(sorted(target_types.items()))[:, 1]
fig = plt.figure(figsize=(8, 5))
sns_plot = sns.heatmap(
    iter_conf_mat / np.tile(iter_conf_mat.sum(axis=1), [iter_conf_mat.shape[0], 1]).T * 1e2,
    cmap="Blues",
    annot=True,
    fmt='.2f',
    cbar=False,
    xticklabels=iter_conf_mat_labels,
    yticklabels=iter_conf_mat_labels

)
plt.show()
plt.xlabel('Estimated Type'),
plt.ylabel('Actual Type'),

"""# Output metrics"""

metrics = classification_report(np.concatenate(y_true_list), np.concatenate(y_pred_list), digits=3)
print(metrics)
