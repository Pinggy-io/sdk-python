# setup.py may depricate-https://blog.ganssle.io/articles/2021/10/setup-py-deprecated.html

import os
import sysconfig
import sys
from setuptools import setup, find_packages
from setuptools.dist import Distribution
from wheel.bdist_wheel import bdist_wheel as _bdist_wheel
import tempfile
import zipfile
import tarfile
import ssl
import urllib
import subprocess
from pinggy import __version__ as version

PINGGY_LIB_VERSION = version.__lib_pinggy_version
BASE_URL = f"{version.__lib_pinggy_url_prefix}{PINGGY_LIB_VERSION}"

def parse_platname_and_arch(platform_key):

    defaultsKeys = {
        "macosx-universal" : ("macosx", "universal"),
        "linux-aarch64"    : ("linux", "aarch64"),
        "linux-arm7l"      : ("linux", "armv7"),
        "linux-i686"       : ("linux", "i686"),
        "linux-x86_64"     : ("linux", "x86_64"),
        "win-amd64"        : ("win", "x86_64"),
        "win-arm64"        : ("win", "aarch64"),
        "win32"            : ("win", "i686"),
    }

    if platform_key in defaultsKeys:
        return defaultsKeys[platform_key]


    arch_map = {
        "2_28-x86_64": "x86_64",
        "amd64": "x86_64",
        "x86_64": "x86_64",
        "i386": "i686",
        "win32": "i686",
        "armv7l": "armv7",
        "arm64": "aarch64",
    }

    # raise RuntimeError(f"unsupported platform ${platform_key}")

    if (platform_key.startswith("mac")):
        return "macosx", "universal"
        # system, _, arch = platform_key.split("-")
    else:
        system, arch = platform_key.split("-")

    return system, arch_map.get(arch, arch)

class custom_bdist_wheel(_bdist_wheel):
    # Meaning of these tags in wheel file name are defined in - https://peps.python.org/pep-0425/
    def get_tag(self):

        supported_platforms = {
            "macosx-universal" : "macosx_11_0_universal2",
            "linux-aarch64"    : "manylinux_2_28_aarch64",
            "linux-armv7l"     : "manylinux_2_28_armv7l",
            "linux-i686"       : "manylinux_2_28_i686",
            "linux-x86_64"     : "manylinux_2_28_x86_64",
            "win-amd64"        : "win_amd64",
            "win-arm64"        : "win_arm64",
            "win32"            : "win32",
        }


        finalPlatform = supported_platforms.get(self.plat_name, self.plat_name)
        if self.plat_name in supported_platforms:
            return "cp310", "abi3", finalPlatform,

        # Extracting OS and architecture from --plat-name={OS}-{architecture}
        if "-" in self.plat_name:
            plat, arch = parse_platname_and_arch(self.plat_name)

        # Returing wheel name parameters- impl_tag, abi_tag, plat_tag
        if plat.startswith("macosx"):
            return (
                "cp310",
                "abi3",
                "macosx_11_0_universal2",
            )  # dev_pinggy-1.0.0-cp310-abi3-macosx_11_0_universal2
        # elif finalPlatform.startswith("linux"):
        #     return (
        #         "cp310",
        #         "abi3",
        #         finalPlatform,
        #     )  # dev_pinggy-1.0.0-cp310-abi3-manylinux_2_28_{architecture}
        # elif finalPlatform.startswith("win"):
        #     return (
        #         "cp310",
        #         "abi3",
        #         finalPlatform,
        #     )  # dev_pinggy-1.0.0-cp310-abi3-win-{architecture}

        return "cp310", "abi3", self.plat_name


def download_and_extract_files(system, arch, destination):
    tempDir = tempfile.gettempdir()
    base_url = os.environ.get("LIB_PINGGY_SERVER", BASE_URL)
    file = {
        "linux":   f"libpinggy-{PINGGY_LIB_VERSION}-ssl-linux-{arch}.tgz",
        "macosx":  f"libpinggy-{PINGGY_LIB_VERSION}-ssl-macos-universal.tgz",
        "win":     f"libpinggy-{PINGGY_LIB_VERSION}-windows-{arch}-MT.zip",
    }.get(system)

    libfilename = {
        "linux":   "libpinggy.so",
        "macosx":  "libpinggy.dylib",
        "win":     "pinggy.dll",
    }.get(system)


    url = f"{base_url}/{file}"
    print(url)
    caching_dir_path = f"{tempDir}/libpinggy/v{PINGGY_LIB_VERSION}/{system}/{arch}"
    cached_file_path = f"{caching_dir_path}/{file}"
    destination_file = f"{destination}/{libfilename}"

    if not os.path.exists(cached_file_path):
        try:
            os.makedirs(caching_dir_path)
        except:
            pass
        try:
            print(f"Downloading `{url}` to `{cached_file_path}`")
            if system == "win":
                ssl._create_default_https_context = ssl._create_unverified_context
            urllib.request.urlretrieve(url, cached_file_path)
            # response = requests.get(url, stream=True)
            # response.raise_for_status()
            # with open(destination_file, "wb") as f:
            #     for chunk in response.iter_content(chunk_size=8192):
            #         if chunk:
            #             f.write(chunk)
        except Exception as err:
            sys.exit(f"Failed to download shared library `{cached_file_path}` from `{url}`.\n{err}")


    if not os.path.exists(destination_file) or os.path.getmtime(cached_file_path) > os.path.getmtime(destination_file):
        try:
            if cached_file_path.endswith('.zip'):
                with zipfile.ZipFile(cached_file_path, 'r') as zip_ref:
                    zip_ref.extractall(path=destination)
                # print(f"Extracted ZIP to {caching_dir_path}")
            elif cached_file_path.endswith(('.tar.gz', '.tgz', '.tar.bz2', '.tar.xz', '.tar')):
                with tarfile.open(cached_file_path, 'r:*') as tar_ref:
                    tar_ref.extractall(path=destination)
                # print(f"Extracted TAR to {caching_dir_path}")
            else:
                sys.exit(f"Unsupported archive format: {cached_file_path}")
        except Exception as err:
            sys.exit(f"Failed to load shared library. Ensure dependencies like OpenSSL are installed if required.\n{err}")

    if os.path.exists(destination_file):
        listOfFiles  = {
            "linux":   ["libpinggy.so", "openssl/lib/libcrypto.so", "openssl/lib/libssl.so", "openssl/lib/libcrypto.so.3", "openssl/lib/libssl.so.3"],
            "macosx":  ["libpinggy.dylib", "openssl/lib/libcrypto.dylib", "openssl/lib/libssl.dylib", "openssl/lib/libcrypto.3.dylib", "openssl/lib/libssl.3.dylib"],
            "win":     ["pinggy.dll", "pinggy.lib"],
        }.get(system)
        return listOfFiles
    sys.exit("cannot download required files")

def get_shared_libraries():
    system = None
    arch = None

    for arg in sys.argv:
        if arg.startswith("--plat-name="):
            plat = arg.split("=")[-1].lower()
            if "-" in plat:
                system, arch = parse_platname_and_arch(plat)
            elif "macosx" in plat:
                system, arch = "macosx", "universal"

    if system is None:
        platform_key = sysconfig.get_platform().lower()
        system, arch = parse_platname_and_arch(platform_key)

    print(f"platform = {system}\narch={arch}")

    package_files = []
    # Download lib files for binary distributon only
    if "bdist_wheel" in sys.argv:
        dest_dir = "pinggy/bin"
        os.makedirs(dest_dir, exist_ok=True)

        files_to_be_packaged = download_and_extract_files(system, arch, dest_dir)
        for file in files_to_be_packaged:
            package_files.append(f"bin/{file}")

    print(package_files)
    return package_files


class BinaryDistribution(Distribution):
    def has_ext_modules(self):
        return True

def get_version():
    try:
        return subprocess.check_output(['git', 'describe', '--tags', '--abbrev=0']).decode().strip()
    except Exception as e:
        print("Exception occured while getting tag: ", e)
        return "0.0.0"

setup(
    name="pinggy",
    version=version.__version__,
    packages=find_packages(),
    include_package_data=True,
    package_data={"pinggy": get_shared_libraries()},
    description="Tunneling tool",
    long_description=open("PyPI_Description.md").read(),
    long_description_content_type="text/markdown",
    author="Pinggy",
    license="Apache 2.0",
    distclass=BinaryDistribution,
    cmdclass={"bdist_wheel": custom_bdist_wheel},
    zip_safe=False,
)
