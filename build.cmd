@echo off

:WHEEL
	pip install wheel
	python setup.py bdist_wheel
	goto EXIT

:PYC
	del /a/f/q/s *.pyc
	set PATH=D:\Python27;D:\Python27\Scripts
	python setup.py build_py bdist_egg --exclude-source-files

	del /a/f/q/s *.pyc
	set PATH=D:\Apps\Python26;D:\Apps\Python26\Scripts
	python setup.py build_py bdist_egg --exclude-source-files

:EXIT
