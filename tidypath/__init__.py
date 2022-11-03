import sys as _sys
import os as _os
from . import decorators
from . import fmt
from . import storage
from .decorators import savedata, savefig

# Set all paths refered to RootDir
RootDir = _os.path.dirname(_os.path.dirname(__file__))
_os.chdir(RootDir)
_sys.path.append(RootDir)

__version__ = "1.0"

__all__ = ['RootDir',
           'decorators',
           "savedata",
           "savefig",
           'fmt',
           'storage'
          ]