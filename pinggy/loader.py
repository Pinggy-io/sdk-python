import ctypes
import platform
import os
import sys

# Get package directory
package_dir = os.path.dirname(os.path.abspath(__file__))

# Determine OS and architecture
system = platform.system().lower()
machine = platform.machine().lower()

# Mapping system to correct shared library name
lib_name = {
    "windows": "pinggy.dll",
    "linux": "libpinggy.so",
    "darwin": "libpinggy.dylib",
}.get(system)

# Locate the shared library dynamically
lib_path = os.path.join(package_dir, "bin", lib_name)

# Ensure the shared library exists
if not os.path.exists(lib_path):
    sys.exit(f"Shared library missing: `{lib_path}`")

# Load the shared library
try:
    cdll = ctypes.CDLL(lib_path)
except Exception as err:
    sys.exit(f"Failed to load shared library. Ensure dependencies like OpenSSL are installed if required.\n{err}")
