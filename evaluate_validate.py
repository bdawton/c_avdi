import numpy as np
from sklearn.metrics import confusion_matrix
from imblearn.under_sampling import RandomUnderSampler


# evaluate
def evaluate(fit_model, x_train, y_train, x_test, y_test):

    # training
    fit_model.fit(x_train, y_train)
    test_score = fit_model.score(x_train, y_train)

    # prediction with test data
    y_pred = fit_model.predict(x_test)

    # generate confusion matrix
    conf_mat = confusion_matrix(y_test, y_pred)

    return test_score, conf_mat, fit_model, y_pred


# leave-one-subject-out validation, with option to output predictions and resampled compressive measurements for export to MCU
def validate(x_train, y_train, x_test, y_test, orig_model, compressive_measurements=None, random_state=None):
    uniq_train, counts_train = np.unique(y_train, return_counts=True)
    counts_train[:] = np.min(counts_train)
    sampler_train = RandomUnderSampler(sampling_strategy=dict(zip(uniq_train, counts_train)), random_state=random_state)
    uniq_test, counts_test = np.unique(y_test, return_counts=True)
    counts_test[:] = np.min(counts_test)
    sampler_test = RandomUnderSampler(sampling_strategy=dict(zip(uniq_test, counts_test)), random_state=random_state)

    # resample data to balance the training/test data
    x_train_resamp, y_train_resamp = sampler_train.fit_resample(x_train, y_train)
    x_test_resamp, y_true = sampler_test.fit_resample(x_test, y_test)


    if compressive_measurements is not None:
        # obtain the corresponding resampled compressive measurements we only need the "test" entries, because the
        # classifier is trained in Python and exported to MCU, no training on MCU.
        x_compressive_measurements_resamp, y_compressive_measurements_resamp = sampler_test.fit_resample(compressive_measurements, y_test)
    else:
        x_compressive_measurements_resamp = None

    score, conf_mat, fit_model, y_pred = evaluate(orig_model, x_train_resamp, y_train_resamp, x_test_resamp, y_true)

    return score, conf_mat, fit_model, y_pred, y_true, x_compressive_measurements_resamp
