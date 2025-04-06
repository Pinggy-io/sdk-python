import os
import sysconfig
import sys
import urllib.request
from setuptools import setup, find_packages
from setuptools.dist import Distribution


PLATFORM_FILES = {
    'linux-x86_64': 'libpinggy.so',
    'win-amd64': 'libpinggy.dll',
    'macosx_10_9_x86_64': 'lib.dylib',
}

arch_map = {
    "2_28-x86_64":"x86_64",
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
    
    # target_plat = os.environ.get("TARGET_PLAT")
    
    for arg in sys.argv:
        if arg.startswith("--plat-name="):
            plat = arg.split("=")[-1].lower()
            if "-" in plat:
                system, arch = plat.split("-") 
            elif "macos" in plat:
                system, arch = "darwin", "universal"       
        elif arg.startswith("--lib-server="):
            BASE_URL = arg.split("=")[-1].lower()
        
    if system is None:
        platform_key = sysconfig.get_platform().lower()
        system, _,arch = platform_key.partition("-")
        
    if BASE_URL is None:
        BASE_URL = os.environ.get("LIB_PINGGY_SERVER",DEFAULT_URL)
        
    arch = arch_map.get(arch, arch) 
    
    print(f"platform = {system}\narch={arch}")
    
    url = None
    dest_path = None
    src = None
    package_files = []
    
    dest_dir = "pinggy/bin"
    os.makedirs(dest_dir, exist_ok=True)

    
    if(system == "linux"):
        src = "libpinggy.so"
        url = f"{BASE_URL}{VERSION}/{system}/{arch}/libpinggy.so"
        dest_path = os.path.join(dest_dir, os.path.basename(src))
        print(f"[+] Downloading libpinggy.so from {url}")
    elif(system == "win"):
        src = "pinggy.dll"
        url = f"{BASE_URL}{VERSION}/{system}/{arch}/pinggy.dll"
        dest_path = os.path.join(dest_dir, os.path.basename(src))
        print(f"[+] Downloading pinggy.dll from {url}")
    elif(system == "darwin"):
        src = "libpinggy.dylib"
        url = f"{BASE_URL}{VERSION}/{system}/{arch}/libpinggy.dylib"
        dest_path = os.path.join(dest_dir, os.path.basename(src))
        print(f"[+] Downloading libpinggy.dylib from {url}")
    
    urllib.request.urlretrieve(url, dest_path)
    package_files.append(f"bin/{os.path.basename(src)}")
    return package_files


class BinaryDistribution(Distribution):
    def has_ext_modules(self):
        return True

setup(
    name='dev-pinggy',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    package_data={"pinggy": get_shared_libraries()},
    description='Cross-platform shared library package',
    author='Bishnu Thakur',
    license='MIT',
    distclass=BinaryDistribution,
    # cmdclass={'build_py': CustomBuild},
    zip_safe=False,
)
