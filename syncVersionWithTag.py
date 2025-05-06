import subprocess

version_file="pinggy/__version__.py"

version_data = []
with open(version_file) as version_fp:
    version_data = [line.strip() for line in version_fp if not line.startswith("__version__ = \"")]

version = subprocess.check_output(['git', 'describe', '--tags', '--abbrev=0']).decode().strip()

with open(version_file, "w") as version_fp:
    for line in version_data:
        print(line, file=version_fp)
    print(f"__version__ = \"{version}\"", file=version_fp)
