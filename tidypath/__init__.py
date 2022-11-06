import sys as _sys
import os as _os
from . import fmt
from . import storage
from .decorators import savedata, savefig
from .paths import add_arg, delete_arg, modify_arg

# Set all paths refered to RootDir
RootDir = _os.path.dirname(_os.path.dirname(__file__))
_os.chdir(RootDir)
_sys.path.append(RootDir)

__version__ = "1.0"

__all__ = ['RootDir',
           "savedata",
           "savefig",
           'fmt',
           'storage',
           "add_args",
           'delete_arg',
           'modify_arg'
          ]