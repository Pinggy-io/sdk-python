import subprocess

version_file="pinggy/__version__.py"

version_data = []
with open(version_file) as version_fp:
    version_data = [line.strip() for line in version_fp if not line.startswith("__version__ = \"")]

version = subprocess.check_output(['git', 'describe', '--tags', '--abbrev=0']).decode().strip()
# Tags are conventionally prefixed with `v` (e.g. v0.1.0); strip it so the
# package version stays PEP 440 compliant.
if version.startswith("v"):
    version = version[1:]

with open(version_file, "w") as version_fp:
    for line in version_data:
        print(line, file=version_fp)
    print(f"__version__ = \"{version}\"", file=version_fp)
