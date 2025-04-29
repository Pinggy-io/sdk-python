# Python SDK for Pinggy

Step by step procedure to build `.whl` files for Pinggy, dependening on different OS & Architecture.

## 📁 Directory Structure
```bash
pinggy/
├── core.py
├── __init__.py
├── pinggy.h
└── pylib.py
setup.py
```

## 🛠️ Requirements

- Python 3.6+
- `wheel` and `setuptools`
> ```bash
>    pip install wheel setuptools requests
> ```
- Shared libraries (`.so`, `.dll`, `.dylib`) hosted on an HTTP server
    ### Structure
    ```
    v0.1
    ├── darwin
    │   └── universal
    │       ├── libpinggy.dylib
    ├── linux
    │   ├── aarch64
    │   │   ├── libpinggy.so
    │   ├── armv7
    │   │   ├── libpinggy.so
    │   ├── i686
    │   │   ├── libpinggy.so
    │   └── x86_64
    │       ├── libpinggy.so
    └── win
        ├── aarch64
        │   └── pinggy.dll
        ├── armv7
        │   └── pinggy.dll
        ├── i686
        │   └── pinggy.dll
        └── x86_64
            └── pinggy.dll
    ```
- Linux system for building all platform wheels (cross-platform)


## 🔧 Environment Setup

Set the environment variable for the shared library server:

```bash
export LIB_PINGGY_SERVER=http://lib_pinggy_server.com/
```

## Example Usage
```
python setup.py bdist_wheel --plat-name=win-amd64
```
```
python setup.py bdist_wheel --plat-name=linux-x86_64
```
```
python setup.py bdist_wheel --plat-name=macosx-universal
```

## License

[LICENSE](./LICENSE)