
all: win linux macos

#=================

win: win-amd64 win-arm64 win32

win32: dist/dev_pinggy-0.0.8-cp310-abi3-win32.whl

win-arm64: dist/dev_pinggy-0.0.8-cp310-abi3-win_arm64.whl

win-amd64: dist/dev_pinggy-0.0.8-cp310-abi3-win_amd64.whl

dist/dev_pinggy-0.0.8-cp310-abi3-win32.whl:
	@rm -rf pinggy/bin build dev_pinggy.egg-info || true
	python3 setup.py bdist_wheel --plat-name=win32

dist/dev_pinggy-0.0.8-cp310-abi3-win_amd64.whl:
	@rm -rf pinggy/bin build dev_pinggy.egg-info || true
	python3 setup.py bdist_wheel --plat-name=win-amd64

dist/dev_pinggy-0.0.8-cp310-abi3-win_arm64.whl:
	@rm -rf pinggy/bin build dev_pinggy.egg-info || true
	python3 setup.py bdist_wheel --plat-name=win-arm64

#=================

macos: macos-universal
	@rm -rf pinggy/bin build dev_pinggy.egg-info || true

macos-universal: dist/dev_pinggy-0.0.8-cp310-abi3-macosx_11_0_universal2.whl

dist/dev_pinggy-0.0.8-cp310-abi3-macosx_11_0_universal2.whl:
	@rm -rf pinggy/bin build dev_pinggy.egg-info || true
	python3 setup.py bdist_wheel --plat-name=macosx-universal

#=================

linux: linux-x86_64 linux-i686 linux-armv7l linux-aarch64
	@rm -rf pinggy/bin build dev_pinggy.egg-info || true

linux-x86_64: dist/dev_pinggy-0.0.8-cp310-abi3-manylinux_2_28_x86_64.whl

linux-i686: dist/dev_pinggy-0.0.8-cp310-abi3-manylinux_2_28_i686.whl

linux-armv7l: dist/dev_pinggy-0.0.8-cp310-abi3-manylinux_2_28_armv7l.whl

linux-aarch64: dist/dev_pinggy-0.0.8-cp310-abi3-manylinux_2_28_aarch64.whl

dist/dev_pinggy-0.0.8-cp310-abi3-manylinux_2_28_aarch64.whl:
	@rm -rf pinggy/bin build dev_pinggy.egg-info || true
	python3 setup.py bdist_wheel --plat-name=linux-aarch64

dist/dev_pinggy-0.0.8-cp310-abi3-manylinux_2_28_armv7l.whl:
	@rm -rf pinggy/bin build dev_pinggy.egg-info || true
	python3 setup.py bdist_wheel --plat-name=linux-armv7l

dist/dev_pinggy-0.0.8-cp310-abi3-manylinux_2_28_i686.whl:
	@rm -rf pinggy/bin build dev_pinggy.egg-info || true
	python3 setup.py bdist_wheel --plat-name=linux-i686

dist/dev_pinggy-0.0.8-cp310-abi3-manylinux_2_28_x86_64.whl:
	@rm -rf pinggy/bin build dev_pinggy.egg-info || true
	python3 setup.py bdist_wheel --plat-name=linux-x86_64