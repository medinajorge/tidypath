"""
Creates paths for automatically organizing files.

Two schemes:
    1. By module => Module -> submodules -> class tree (until classes in module by default) -> func
    2. By class  => Class organization is a class to be inherited. Sets path: parentDir -> subfolder (optionally specified) -> inheritance_tree -> func_name.
(1) is the most appropiate.
"""
import os
import sys
import inspect
from pathlib import Path
from .fmt import dict_to_id
from .inspection import get_class_that_defined_method

dataDir = "data"
figDir = "figs"

def join_paths(*paths):
    path = paths[0]
    for p in paths[1:]:
        path = os.path.join(path, p)
    return path

def module_path(func=None, depth=3, include_classes="file", skip=1):
    """
    returns module path and func_name.
    
    include_classes:   'file': path: module -> class tree contained in func file -> func_name.
                       'all': path: module -> full class tree -> func_name.
    """
    if func is None:
        frame = sys._getframe(depth)
        func_name = frame.f_code.co_name
        module = frame.f_globals["__name__"]
    else:
        func_name = func.__name__
        module = func.__module__
    if include_classes:
        func_class = get_class_that_defined_method(func)
        if func_class is not None:
            if include_classes == "file":
                clsmembers = inspect.getmembers(sys.modules[module], inspect.isclass)
                cls_names, clss = zip(*clsmembers)
                class_tree = "/".join([c.__name__.lower() for c in func_class.mro()[:-skip][::-1] if c in clss])
            elif include_classes == "all":
                "/".join([c.__name__.lower() for c in func.__class__.mro()[:-skip][::-1]])
            else:
                raise ValueError(f"include_classes: {include_classes} not valid. Available: 'file', 'all', ''.")
        else:
            class_tree = ""
    else:
        class_tree = ""
    path = join_paths(*module.split(".")[1:], class_tree, func_name)
    return path

def saving_path(Dir, ext, keys={}, subfolder="", **kwargs):
    """Tree path: subfolder -> module -> (classes) -> func_name."""
    parentDir = join_paths(Dir, subfolder, module_path(**kwargs))
    Path(parentDir).mkdir(exist_ok=True, parents=True)                
    return os.path.join(parentDir, f"{dict_to_id(keys)}_.{ext}")
    
def figpath(ext="png", **kwargs):
    return saving_path(figDir, ext, **kwargs)

def datapath(ext="lzma", **kwargs):
    return saving_path(dataDir, ext, **kwargs)


class Organizer():
    dataDir = dataDir
    figDir = figDir
    subfolder = ""
    
class ClassPath(Organizer):
    """
    Updates fig and data dir of the class as follows:
    parentDir -> subfolder -> inheritance_tree -> func_name
    """
    
    @classmethod
    def inheritance_path(cls, skip=2):
        return "/".join([c.__name__.lower() for c in cls.mro()[:-skip][::-1]])
    
    @classmethod
    def create_dir(cls, dirKey, depth=2):
        """Creates tree: parentDir -> subfolder -> inheritance_tree -> func_name"""
        path = cls.join_paths(getattr(cls, f"{dirKey}Dir"),
                              cls.subfolder,
                              cls.inheritance_path(),
                              sys._getframe(depth).f_code.co_name
                             )
        Path(path).mkdir(exist_ok=True, parents=True)
        return path
        
    @classmethod
    def create_figDir(cls):
        return cls.create_dir("fig")
    
    @classmethod
    def create_dataDir(cls):
        return cls.create_dir("data")
    