@echo off
for /f delims^= %%i in ('dir /b /s /a-d') do (
	if %%~xi == .ui (
		if NOT %%~ni == CameraConfigDialog (
			pyside2-uic %%i -x -o %%~dpni.py 	
		)
	)
	if %%~xi == .qrc (
		pyside2-rcc %%i -o %%~dpni.py 	 
	)
)