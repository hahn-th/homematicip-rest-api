@ECHO OFF

pushd %~dp0

if "%SPHINXAPIDOC%" == "" (
	set SPHINXAPIDOC=sphinx-apidoc
)

set SOURCEDIR=source

%SPHINXAPIDOC% -o %SOURCEDIR% ../homematicip

popd