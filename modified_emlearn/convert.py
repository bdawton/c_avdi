
from . import trees
from . import net
from . import bayes

def convert(estimator, kind=None,  method='pymodule', int_toggle=None, dtype='float'):
    """Main entrypoint for converting a model"""

    if kind is None:
        kind = type(estimator).__name__

    # Use name instead of instance to avoid hard dependency on the libraries
    if kind in ['RandomForestClassifier', 'ExtraTreesClassifier', 'DecisionTreeClassifier']:
        return trees.Wrapper(estimator, method, int_toggle, dtype=dtype)
    elif kind == 'MLPClassifier':
        return net.convert_sklearn_mlp(estimator, method)
    elif kind == 'Sequential':
        return net.convert_keras(estimator, method)
    elif kind == 'GaussianNB':
        return bayes.Wrapper(estimator, method)
    else:
        raise ValueError("Unknown model type: '{}'".format(kind))
