import numpy as np
import pandas as pd


def quantiser(input_signal, B, axis, dec_points):
    df_flag = False
    series_flag = False

    if isinstance(input_signal, pd.DataFrame):
        df_flag = True
        col_names = input_signal.columns
        row_names = input_signal.index
        input_signal.to_numpy()

    if isinstance(input_signal, pd.Series):
        series_flag = True
        name = input_signal.name
        row_name = input_signal.index
        input_signal.to_numpy()

    if np.ndim(input_signal) == 1:
        min_signal = np.min(input_signal)
        max_signal = np.max(input_signal)
        r_signal = np.abs(max_signal) + np.abs(min_signal)
        num_quanta = 2 ** B
        p_start = min_signal + (r_signal / (2 ** B))
        p_step = r_signal / (2 ** B)
        c_start = min_signal + ((r_signal / (2 ** B)) / 2)
        c_step = r_signal / (2 ** B)
        input_signal = np.asarray(input_signal, dtype=float)  # May not need this line - leave for now

        quant_sig_list = []
        sig_slice = input_signal
        indices = np.empty_like(sig_slice, dtype=float)
        np.floor_divide((sig_slice - p_start + p_step), p_step, indices)  # store result in "indices"
        np.clip(indices, 0, num_quanta - 1, indices)
        quant_sig = np.asarray(indices, dtype=float) * c_step + c_start
        quant_sig = np.around(quant_sig,
                              dec_points)  # Dec_points was set as "1" for IEEE Access, but maybe good to know?
        quant_sig_list.append(quant_sig)
        quant_sig_array = np.squeeze(np.array(quant_sig_list))

    elif np.ndim(input_signal) == 2:
        min_signal = np.min(input_signal, axis)
        max_signal = np.max(input_signal, axis)
        r_signal = np.abs(max_signal) + np.abs(min_signal)
        num_quanta = 2 ** B
        p_start = min_signal + (r_signal / (2 ** B))
        p_step = r_signal / (2 ** B)
        c_start = min_signal + ((r_signal / (2 ** B)) / 2)
        c_step = r_signal / (2 ** B)
        input_signal = np.asarray(input_signal, dtype=float)  # May not need this line - leave for now

        quant_sig_list = []

        for slice_var in range(np.shape(input_signal)[1 - axis]):
            if axis == 0:
                sig_slice = input_signal[:, slice_var]
            elif axis == 1:
                sig_slice = input_signal[slice_var, :]
            else:
                print("axis needs to be '0' or '1'")
                break

            indices = np.empty_like(sig_slice, dtype=float)
            np.floor_divide((sig_slice - p_start[slice_var] + p_step[slice_var]), p_step[slice_var], indices)  # store result in "indices"
            np.clip(indices, 0, num_quanta - 1, indices)
            quant_sig = np.asarray(indices, dtype=float) * c_step[slice_var] + c_start[slice_var]
            quant_sig = np.around(quant_sig,
                                  dec_points)  # Dec_points was set as "1" for IEEE Access, but maybe good to know?
            quant_sig_list.append(quant_sig)

        quant_sig_array = np.array(quant_sig_list)

    else:
        print('error: more than 2-dimensions not supported')
        return None

    if df_flag is True:
        if axis == 0:
            quant_sig_array = np.transpose(quant_sig_array)
        df_quant_sig_array = pd.DataFrame(quant_sig_array, index=row_names, columns=col_names)
        return df_quant_sig_array

    if series_flag is True:
        df_quant_sig_array = pd.Series(quant_sig_array, index=row_name, name=name)
        return df_quant_sig_array

    return quant_sig_array
