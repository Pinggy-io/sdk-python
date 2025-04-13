# setup.py may depricate-https://blog.ganssle.io/articles/2021/10/setup-py-deprecated.html

import os
import sysconfig
import sys
import urllib.request
from urllib.request import urlopen
import ssl
from setuptools import setup, find_packages
from setuptools.dist import Distribution
from wheel.bdist_wheel import bdist_wheel as _bdist_wheel


class custom_bdist_wheel(_bdist_wheel):
    # Meaning of these tags are defined in - https://peps.python.org/pep-0425/
    def get_tag(self):
        plat = None
        arch = None

        # Extracting OS and architecture from --plat-name={OS}-{architecture}
        if "-" in self.plat_name:
            plat, arch = self.plat_name.split("-")
        else:
            plat = self.plat_name

        # Returing wheel name parameters- impl_tag, abi_tag, plat_tag
        if plat.startswith("mac"):
            return (
                "cp310",
                "abi3",
                "macosx_11_0_universal2",
            )  # dev_pinggy-1.0.0-cp310-abi3-macosx_11_0_universal2
        elif plat.startswith("linux"):
            return (
                "cp310",
                "abi3",
                "manylinux_2_28_" + arch,
            )  # dev_pinggy-1.0.0-cp310-abi3-manylinux_2_28_{architecture}
        elif plat.startswith("win"):
            return (
                "cp310",
                "abi3",
                self.plat_name,
            )  # dev_pinggy-1.0.0-cp310-abi3-win-{architecture}


arch_map = {
    "2_28-x86_64": "x86_64",
    "amd64": "x86_64",
    "x86_64": "x86_64",
    "i386": "i686",
    "win32": "i686",
    "armv7l": "armv7",
    "arm64": "aarch64",
}


def get_shared_libraries():
    system = None
    arch = None

    VERSION = "v0.1"
    DEFAULT_URL = f"http://127.0.0.1:8000/"
    BASE_URL = None

    for arg in sys.argv:
        if arg.startswith("--plat-name="):
            plat = arg.split("=")[-1].lower()
            if "-" in plat:
                system, arch = plat.split("-")
            elif "macos" in plat:
                system, arch = "darwin", "universal"

    if system is None:
        platform_key = sysconfig.get_platform().lower()
        system, _, arch = platform_key.partition("-")

    # Trying to fetch LibPinggy base_url from environment variable
    if BASE_URL is None:
        BASE_URL = os.environ.get("LIB_PINGGY_SERVER", DEFAULT_URL)

    arch = arch_map.get(arch, arch)

    print(f"platform = {system}\narch={arch}")

    url = None
    dest_path = None
    src = None
    package_files = []

    # Download lib files for binary distributon only
    if "bdist_wheel" in sys.argv:
        dest_dir = "pinggy/bin"
        os.makedirs(dest_dir, exist_ok=True)

        # Downloading library file according to OS
        if system == "linux":
            src = "libpinggy.so"
            url = f"{BASE_URL}/{VERSION}/{system}/{arch}/libpinggy.so"
            dest_path = os.path.join(dest_dir, os.path.basename(src))
            print(f"[+] Downloading libpinggy.so from {url}")
        elif system == "win":
            src = "pinggy.dll"
            url = f"{BASE_URL}/{VERSION}/{system}/{arch}/pinggy.dll"
            dest_path = os.path.join(dest_dir, os.path.basename(src))
            print(f"[+] Downloading pinggy.dll from {url}")
        elif system == "darwin":
            src = "libpinggy.dylib"
            url = f"{BASE_URL}/{VERSION}/{system}/{arch}/libpinggy.dylib"
            dest_path = os.path.join(dest_dir, os.path.basename(src))
            print(f"[+] Downloading libpinggy.dylib from {url}")

        ssl_context = ssl._create_unverified_context()  # for test purpose only
        # urllib.request.urlretrieve(url, dest_path, context=ssl_context)
        with urlopen(url, context=ssl_context) as response, open(
            dest_path, "wb"
        ) as out_file:
            out_file.write(response.read())
        package_files.append(dest_path)
        # package_files.append(f"bin/{os.path.basename(src)}")
    return package_files


class BinaryDistribution(Distribution):
    def has_ext_modules(self):
        return True


setup(
    name="dev-pinggy",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    package_data={"pinggy": get_shared_libraries()},
    description="Tunneling tool",
    author="Bishnu Thakur",
    license="Apache 2.0",
    distclass=BinaryDistribution,
    cmdclass={"bdist_wheel": custom_bdist_wheel},
    zip_safe=False,
)
