import ctypes
import platform
import os
import sys
import urllib
import urllib.request
import tempfile
import ssl
import zipfile
import tarfile

from . import __version__ as version
from . import pinggyexception

PinggyNativeLoaderError = pinggyexception.PinggyNativeLoaderError

def defaultLoader():
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
        raise PinggyNativeLoaderError("Could not find the require native libraries. Try setting the environment variable `PINGGY_DL_NATIVE` to `true` to download the native libraries.")

    # Load the shared library
    try:
        cdll = ctypes.CDLL(lib_path)
        return cdll
    except Exception as err:
        raise PinggyNativeLoaderError(f"Could not load native library. {err}. Try setting the environment variable `PINGGY_DL_NATIVE` to `true` to download the native libraries.")



lib_version = version.__lib_pinggy_version
base_url = f"{version.__lib_pinggy_url_prefix}{lib_version}"

def get_architecture():
    machine = platform.machine().lower()

    if machine in ('x86_64', 'amd64'):
        return 'x86_64'
    elif machine in ('i386', 'i686', 'x86'):
        return 'i686'
    elif machine in ('aarch64', 'arm64'):
        return 'aarch64'
    elif machine.startswith('armv7'):
        return 'armv7'
    else:
        return machine

def load_native():
    tempDir = tempfile.gettempdir()

    if os.environ.get("LIBPAINGGY_NATIV_PATH", "") != "" :
        tempDir = os.environ.get("LIBPAINGGY_NATIV_PATH", "")

    # Determine OS and architecture
    system = platform.system().lower()
    machine = get_architecture()

    file = {
        "linux":   f"libpinggy-{lib_version}-ssl-linux-{machine}.tgz",
        "darwin":  f"libpinggy-{lib_version}-ssl-macos-universal.tgz",
        "windows": f"libpinggy-{lib_version}-windows-{machine}-MT.zip",
    }.get(system)

    url = f"{base_url}/{file}"
    caching_dir_path = f"{tempDir}/libpinggy/v{lib_version}/{system}/{machine}"
    cached_file_path = f"{caching_dir_path}/{file}"


    # Mapping system to correct shared library name
    lib_path = {
        "windows": f"{caching_dir_path}/pinggy.dll",
        "linux":   f"{caching_dir_path}/libpinggy.so",
        "darwin":  f"{caching_dir_path}/libpinggy.dylib",
    }.get(system)

    if not os.path.exists(cached_file_path):
        try:
            os.makedirs(caching_dir_path)
        except:
            pass
        try:
            # print(f"Downloading `{url}` to `{cached_file_path}`")
            if platform.system() == "Windows":
                ssl._create_default_https_context = ssl._create_unverified_context
            urllib.request.urlretrieve(url, cached_file_path)
        except Exception as err:
            raise PinggyNativeLoaderError(f"Failed to download shared library `{cached_file_path}` from `{url}`. {err}")

    if not os.path.exists(lib_path) or os.path.getmtime(cached_file_path) > os.path.getmtime(lib_path):
        try:
            if cached_file_path.endswith('.zip'):
                with zipfile.ZipFile(cached_file_path, 'r') as zip_ref:
                    zip_ref.extractall(caching_dir_path)
                # print(f"Extracted ZIP to {caching_dir_path}")
            elif cached_file_path.endswith(('.tar.gz', '.tgz', '.tar.bz2', '.tar.xz', '.tar')):
                with tarfile.open(cached_file_path, 'r:*') as tar_ref:
                    tar_ref.extractall(caching_dir_path)
                # print(f"Extracted TAR to {caching_dir_path}")
            else:
                sys.exit(f"Unsupported archive format: {cached_file_path}")
        except Exception as err:
            raise PinggyNativeLoaderError(f"Failed to load shared library. Ensure dependencies like OpenSSL are installed if required. {err}")



    # Ensure the shared library exists
    if not os.path.exists(lib_path):
        sys.exit(f"Shared library missing: `{lib_path}`")

    # Load the shared library
    try:
        cdll = ctypes.CDLL(lib_path)
        return cdll
    except Exception as err:
        raise PinggyNativeLoaderError(f"Failed to load shared library. Ensure dependencies like OpenSSL are installed if required. {err}")

try:
    cdll = defaultLoader()
except PinggyNativeLoaderError as exp:
    if os.environ.get("PINGGY_DL_NATIVE", "") != "":
        cdll = load_native()
    else:
        raise exp

# try:
#     cdll = defaultLoader()
# except:
#     cdll = load_native()
