import numpy as np
import pandas as pd


def extract_features(d, axis=0, shape=1):
    feature_names = ['mean','std','med','abs_max','iqr']
    idx = 0
    series_flag = False

    if isinstance(d, pd.Series):
        series_flag = True
        name = d.name
        row_name = d.index
        d.to_numpy()

    if np.ndim(d) == 1:
        features = np.empty([1, len(feature_names)], dtype=np.float64)
    else:
        features = np.empty([d.shape[shape], len(feature_names)], dtype=np.float64)
        # mean
    features[:, idx] = np.mean(d, axis)
    idx += 1
    # std
    features[:, idx] = np.std(d, axis)
    idx += 1
    # med
    features[:, idx] = np.median(d, axis)
    idx += 1
    # largest absolute value
    features[:, idx] = np.max(np.abs(d), axis)
    idx += 1
    # inter-quantile range
    features[:, idx] = np.subtract(*np.percentile(d, [75, 25], axis))
    idx += 1

    if series_flag is True:
        series_features = pd.Series(np.squeeze(features), index=feature_names, name='ex_feat_' + name)
        return series_features, feature_names

    return features, feature_names