"""
Helper functions
"""

def merge_nested_dict(d, keys, key_default=None):
    """
    Returns the result of merging several keys of a dictionary.
    
    Attrs:
            - d:             nested dictionary
            - keys:          d keys to be merged. can be a string of the form 'k' or 'k1+k2+...', or other iterables containing the keys.
            - key_default:   if a key does not belong to d => it is searched in d[key_default]
    """
    if isinstance(keys, str):
        keys = keys.split("+")
    keys = set(keys)
    d_keys = set(d)
    keys_in_d = keys.intersection(d_keys)
    keys_in_default = keys - keys_in_d
    
    if not keys_in_default.issubset(set(d[key_default])):
        raise RuntimeError("Some keys don't belong to d or d[key_default]")
    else:    
        d_merged = {}    
        for k in keys_in_d:
            d_merged.update(d[k])
        d_default = d[key_default]
        d_merged.update({k: d_default[k] for k in keys_in_default})
        return d_merged

class NoFigure():
    """
    Fill type for plotly/matplotlib figures, if the package is not available.
    Allows tidypath.savefig to work with matplotlib/plotly when the other one is not present.
    """
    pass