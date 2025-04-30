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
    raise Exception("Could not find the require native libraries")

# Load the shared library
try:
    cdll = ctypes.CDLL(lib_path)
except Exception as err:
    raise Exception("Could not load native library")
