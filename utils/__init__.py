# utils/__init__.py

# Import semua utilities yang tersedia
from .misc import *
from .external import *

# Import asset manager jika tersedia
try:
    from .assets import *
except ImportError:
    pass

