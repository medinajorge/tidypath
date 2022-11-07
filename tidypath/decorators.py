"""
Main uses: save and cache data, save figures, change figure color, timing.
"""
import inspect
from pathlib import Path
from functools import wraps
from collections.abc import Iterable
from plotly.graph_objs._figure import Figure as plotly_figure
from matplotlib.figure import Figure as mpl_figure
import matplotlib.pyplot as plt
from . import storage
from .paths import datapath, figpath
from .inspection import classify_call_attrs, merge_wrapper_signatures
from ._helper import merge_nested_dict

def savedata(keys_or_function=None, ext="lzma", include_classes="file",
             overwrite=False, save=True, keys="kwargs", load_opts_default_save=True,  #defaults for extra arguments
             load_opts={}, **save_opts):    
    """
    Decorator for automatically saving output and then loading cached data.
    Default behavior:
        1st function call:   stores the data with extension 'ext'.
        rest:                loads stored data if the key args passed to the function coincide.
        
    NOTE (!) decorated funcs will have extra arguments:
        - save (bool).                 whether to save the output of the function.
        - overwrite (bool).            whether to overwrite the saved version.
        - keys (dict/str/iterable)   · dict:     specifies filename of the form k1-v1_k2-v2_...kn_vn. 
                                                 k_i do not have to be arguments of the function.
                                     · str:       key of a keyword argument. Example: keys = 'x'.
                                                 "kwargs_defaults"  =>  default kwargs that were not modified.
                                                 "kwargs"           =>  kwargs passed during function call.
                                                 "kwargs_full"      =>  kws_defaults + kws.
                                                 "pos_only"         =>  length of *args
                                                 "args"             =>  attrs != **kwargs, *args.
                                                 "all"              =>  all attrs.
                                                 can combine options using "+". Example: "args+rest", "x+y+kwargs".
                                     · iterable: containing a combination of the available string keys (above). ["k1", "k2"] == "k1+k2".
                                                 RECOMMENDED OPTION.
                                         
        
    Attrs:
        - function:                function to which the decorator is applied
        - ext:                     storing extension. Selects 'storage' functions save_ext, load_ext
        - include_classes:         include class tree in saving_path.
        - load_opts:               kws for storage.load_ext. default kws are those of 'saving_options', those specified update saving_options dict.
        - save_opts:               kws for storage.save_ext
        - load_opts_default_save:  use save_opts as default for load_opts.
        - rest:                    default behavior for decorated funcs extra arguments (above).
        
    Returns: Function decorator
    """
    if isinstance(keys_or_function, Iterable):
        keys = keys_or_function
        func = None
    elif callable(keys_or_function):
        func = keys_or_function
    else:
        func = None
        
    if load_opts_default_save:
        load_opts = {**save_opts, **load_opts}
        
    def _savedata(func):  
        @wraps(func)
        def wrapper(*args, overwrite=overwrite, keys=keys, save=save, **kwargs):
            key_opts = classify_call_attrs(func, args, kwargs)
            save_keys = merge_nested_dict(key_opts, keys, key_default="all")                    
            saving_path = datapath(keys=save_keys, func=func, ext=ext, include_classes=include_classes)
            
            if Path(saving_path).exists() and not overwrite:
                return getattr(storage, f"load_{ext}")(saving_path, **load_opts)
            else:
                result = func(*args, **kwargs)
                getattr(storage, f"save_{ext}")(result, saving_path, **save_opts)
                return result

        wrapper.__signature__ = merge_wrapper_signatures(wrapper, ["overwrite", "keys", "save"])
        wrapper.__out__ = "data"
        return wrapper
        
    if func is None:
        return _savedata
    else:
        return _savedata(func)
    

def savefig(keys_or_function=None, ext="png", include_classes="file", return_fig=False,
            keys="kwargs", overwrite=True, save=True,  #defaults for extra arguments
            **save_opts):    
    """
    Generates figsaver decorator.
    Figure returned by function is automatically saved. Compatible with matplotlib and plotly.
        
    NOTE (!) decorated funcs will have extra arguments:
        - return_fig (bool)            whether to return the figure (output of function).
        - save (bool).                 whether to save the figure.
        - overwrite (bool).            whether to overwrite the saved version.
        - keys (dict/str/iterable)   · dict:     specifies filename of the form k1-v1_k2-v2_...kn_vn. 
                                                 k_i do not have to be arguments of the function.
                                     · str:       key of a keyword argument. Example: keys = 'x'.
                                                 "kwargs_defaults"  =>  default kwargs that were not modified.
                                                 "kwargs"           =>  kwargs passed during function call.
                                                 "kwargs_full"      =>  kws_defaults + kws.
                                                 "pos_only"         =>  length of *args. Also self and cls are counted as pos_only arguments.
                                                 "args"             =>  attrs != **kwargs, *args.
                                                 "all"              =>  all attrs.
                                                 can combine options using "+". Example: "args+rest", "x+y+kwargs".
                                     · iterable: containing a combination of the available string keys (above). ["k1", "k2"] == "k1+k2".
                                                 RECOMMENDED OPTION.
                                         
        
    Attrs:
        - function:                function to which the decorator is applied
        - ext:                     storing extension. 'eps' recommended for articles.
        - include_classes:         include class tree in saving_path.
        - save_opts:               kws for saving function.
        - rest:                    default behavior for decorated funcs extra arguments (above).
        
    Returns: Function decorator
    """
    if isinstance(keys_or_function, Iterable):
        keys = keys_or_function
        func = None
    elif callable(keys_or_function):
        func = keys_or_function
    else:
        func = None
        
    mpl_save_defaults = dict(bbox_inches="tight")
        
    def _savefig(func):  
        @wraps(func)
        def wrapper(*args, overwrite=overwrite, keys=keys, save=save, return_fig=return_fig, **kwargs):
            fig = func(*args, **kwargs)
            key_opts = classify_call_attrs(func, args, kwargs)
            save_keys = merge_nested_dict(key_opts, keys, key_default="all")                    
            saving_path = figpath(keys=save_keys, func=func, ext=ext, include_classes=include_classes)
            
            if not Path(saving_path).exists() or overwrite:
                if isinstance(fig, mpl_figure):
                    fig.savefig(saving_path, format=ext, **{**mpl_save_defaults, **save_opts})
                    plt.close(fig)
                elif isinstance(fig, plotly_figure):
                    if ext == "html":
                        fig.write_html(saving_path, **save_opts)
                    else:
                        fig.write_image(saving_path, format=ext, **save_opts)
                else:
                    raise TypeError(f"fig type '{type(fig)}' not valid. Available: 'matplotlib.figure.Figure', 'plotly.grap_objs._figure.Figure'.")
                    
            if return_fig:
                return fig
            else:
                return
            
        wrapper.__signature__ = merge_wrapper_signatures(wrapper, ["overwrite", "keys", "save", "return_fig"])
        wrapper.__out__ = "figure"
        return wrapper
    
    if func is None:
        return _savefig
    else:
        return _savefig(func)
    
class classproperty(object):
    """ @classmethod+@property """
    def __init__(self, f):
        self.f = classmethod(f)
    def __get__(self, *a):
        return self.f.__get__(*a)()
    
    
def dark_figure(orig_func):
    """Wrapping for showing figures in black in jupyter notebook (monokai) after having saved them in normal color."""
    import matplotlib.pyplot as plt
    plt.ion()
    @wraps(orig_func)
    def wrapper(*args,**kwargs):
        result = orig_func(*args,**kwargs)
        for fig_num in plt.get_fignums():
            fig = plt.figure(fig_num)
            for ax in fig.get_axes():
                ax.set_facecolor('#161b1e')
                ax.xaxis.label.set_color('#a8a49d') 
                ax.yaxis.label.set_color('#a8a49d')
                ax.tick_params(axis='both', colors='#a8a49d')
                l = ax.legend(loc='center left', bbox_to_anchor=(1, 0.5),fontsize=18, facecolor='#161b1e', edgecolor='#161b1e', framealpha=1)
                for text in l.get_texts():
                    text.set_color('#a8a49d')
                for spine in ax.spines.values():
                    spine.set_edgecolor('#a8a49d')
                ax.set_title(ax.get_title(), color='#a8a49d')
            fig.patch.set_facecolor('#161b1e')
        plt.show()
        return result
    return wrapper


def timer(func):
    """Wrapper for timing functions"""
    @wraps(func)
    def wrapper(*args,**kwargs):
        t1 = time.time()
        result = func(*args,**kwargs)
        dt = time.time() - t1
        print('{} ran in: {:.2f} s = {:.2f} min = {:.2f} h'.format(func.__name__, dt,dt/60,dt/3600))
        return result
    return wrapper


class timer_class(object):
    """Wrapper for timing functions. Same as timer but in a class."""
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        t1 = time.time()
        result = self.func(*args, **kwargs)
        dt = time.time() - t1
        print('{} ran in: {} sec'.format(self.func.__name__, dt))
        return result

    
def identity(orig_func):
    """Wrapper that does not do anything."""
    @wraps(orig_func)
    def wrapper(*args, **kwargs):
        result = orig_func(*args, **kwargs)
        return result
    return wrapper
