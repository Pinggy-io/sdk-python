
all: win linux macos source

source:
	python3 setup.py sdist

#=================

win: win-amd64 win-arm64 win32

win32:
	@rm -rf pinggy/bin build *.egg-info || true
	python3 setup.py bdist_wheel --plat-name=win32

win-arm64:
	@rm -rf pinggy/bin build *.egg-info || true
	python3 setup.py bdist_wheel --plat-name=win-arm64

win-amd64:
	@rm -rf pinggy/bin build *.egg-info || true
	python3 setup.py bdist_wheel --plat-name=win-amd64


#=================

macos: macos-universal
	@rm -rf pinggy/bin build *.egg-info || true

macos-universal:
	@rm -rf pinggy/bin build *.egg-info || true
	python3 setup.py bdist_wheel --plat-name=macosx-universal

#=================

linux: linux-x86_64 linux-i686 linux-armv7l linux-aarch64
	@rm -rf pinggy/bin build *.egg-info || true

linux-x86_64:
	@rm -rf pinggy/bin build *.egg-info || true
	python3 setup.py bdist_wheel --plat-name=linux-x86_64

linux-i686:
	@rm -rf pinggy/bin build *.egg-info || true
	python3 setup.py bdist_wheel --plat-name=linux-i686

linux-armv7l:
	@rm -rf pinggy/bin build *.egg-info || true
	python3 setup.py bdist_wheel --plat-name=linux-armv7l

linux-aarch64:
	@rm -rf pinggy/bin build *.egg-info || true
	python3 setup.py bdist_wheel --plat-name=linux-aarch64

clean:
	rm -rf dist || true
