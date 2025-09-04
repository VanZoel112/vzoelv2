# utils/__init__.py

# Kita kumpulin 'alat-alat' terbaik dari setiap file 
# dan kita pajang di sini biar gampang diambil.

# Dari file tools.py
# Anggap isinya ada fungsi buat 'process_data' dan 'generate_report'
from .tools import process_data, generate_report

# Dari file misc.py (miscellaneous/serba-serbi)
# Anggap isinya ada fungsi 'log_message'
from .misc import log_message

# Dari file utils.py (ini agak unik karena namanya sama kayak folder)
# Anggap isinya ada fungsi inti 'get_config'
from .utils import get_config

# Dari file external.py yang jadi rencana cadangan Master
# Anggap isinya ada fallback 'FallbackLibraryA' dan 'FallbackLibraryB'
from .external import FallbackLibraryA, FallbackLibraryB


# [SANGAT DIREKOMENDASIKAN]
# Definisikan API publik untuk package 'utils' ini.
# Ini bikin kode Master lebih bersih dan jelas.
__all__ = [
    'process_data',
    'generate_report',
    'log_message',
    'get_config',
    'FallbackLibraryA',
    'FallbackLibraryB'
]

