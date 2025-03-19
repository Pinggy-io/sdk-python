from setuptools import setup, find_packages
import sys
import platform
import shutil
import os
import re
from wheel.bdist_wheel import bdist_wheel as _bdist_wheel

class custom_bdist_wheel(_bdist_wheel):
    # def __init__(self):
    #     print("helllllllloooooooooooooooooooooooooooooooooooooo")
    #     super().__init__()
    def run(self):
        print("=====########",self.plat_name)
        _bdist_wheel.run(self)

def get_plat_name():
    """Extract --plat-name from sys.argv"""
    for arg in sys.argv:
        match = re.match(r"--plat-name=(.+)", arg)
        if match:
            return match.group(1)
    return None

def get_shared_libraries():
    print("Fetching shared libraries with args:", sys.argv)

    plat_name = get_plat_name()
    
    if plat_name:
        print(f"Using provided --plat-name: {plat_name}")
        system, _, machine_folder = plat_name.partition("-")
        system = system.lower()
        print(f"system = {system}, machine_folder = {machine_folder}")
    else:
        system = platform.system().lower()
        machine_folder = platform.machine().lower()


    arch_map = {
        "2_28-x86_64":"x86_64",
        "amd64": "x86_64",
        "x86_64": "x86_64",
        "i386": "i686",
        "win32": "i686",
        "armv7l": "armv7",
        "arm64": "aarch64",
    }

    machine_folder = arch_map.get(machine_folder, machine_folder)

    if system == "manylinux":
        src_files = [f"pinggy/linux/{machine_folder}/libpinggy.so", f"pinggy/linux/{machine_folder}/pinggyclient"]
    elif system == "macosx":
        src_files = ["pinggy/macos/universal/libpinggy.dylib", "pinggy/macos/universal/pinggyclient"]
    elif system == "win":
        src_files = [f"pinggy/windows/{machine_folder}/pinggy.dll"]
    else:
        # machine_folder = "x86_64"
        # src_files = [f"pinggy/windows/{machine_folder}/pinggy.dll"]
        raise RuntimeError(f"Unsupported OS: {system}")

    dest_dir = "pinggy/bin"
    os.makedirs(dest_dir, exist_ok=True)

    copied_files = []
    for src in src_files:
        print(f"copyinggggg ---- {src}")
        dest = os.path.join(dest_dir, os.path.basename(src))
        shutil.copy2(src, dest)
        copied_files.append(f"bin/{os.path.basename(src)}")

    return copied_files

setup(
     cmdclass={
        'bdist_wheel': custom_bdist_wheel,
    },
    name="dev-pinggy",
    version="1.0.0",
    author="Bishnu",
    author_email="bishnuthakur284@gmail.com",
    description="Pinggy package for tunneling",
    packages=find_packages(),
    has_ext_modules=lambda: True,
    include_package_data=True,
    package_data={"pinggy": get_shared_libraries()}, 
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
