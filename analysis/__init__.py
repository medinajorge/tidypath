import os as _os
import sys as _sys
from . import variable1

# Set all paths refered to RootDir
RootDir = _os.path.dirname(_os.path.dirname(__file__))
_os.chdir(RootDir)
_sys.path.append(RootDir)

__all__ = ["time",
           "RootDir"
          ]