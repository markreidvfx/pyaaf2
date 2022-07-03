@echo off
setlocal
@REM Build for Visual Studio compiler. Run your copy of vcvars32.bat or vcvarsall.bat to setup command-line compiler.

where /q cl || (
  echo ERROR: "cl" not found - please run this from the MSVC x64 native tools command prompt.
  exit /b 1
)

if "%Platform%" neq "x64" (
    echo ERROR: Platform is not "x64" - please run this from the MSVC x64 native tools command prompt.
    exit /b 1
)

cl /nologo /Zi /MD classdefs_gen.cpp
cl /nologo /Zi /MD typedefs_gen.cpp

classdefs_gen.exe > classdefs.py
typedefs_gen.exe  > typedefs.py

xcopy /y ".\classdefs.py" "..\..\src\aaf2\model\classdefs.py"
xcopy /y ".\typedefs.py"  "..\..\src\aaf2\model\typedefs.py"