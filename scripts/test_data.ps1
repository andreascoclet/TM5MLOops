@echo off
REM Exit immediately if a command exits with a non-zero status
setlocal enabledelayedexpansion
set "errorlevel=0"

REM Activate the virtual environment
call ..\venv\Scripts\activate

REM Take a data sample
echo Sampling data...
python src\data.py
if %errorlevel% neq 0 (
    echo Failed to sample data.
    exit /b 1
)

REM Validate the data sample
echo Validating data...
python src\validate.py
if %errorlevel% neq 0 (
    echo Data validation failed. Data will not be versioned.
    exit /b 1
)
echo Data validation passed.

REM Version the data sample
echo Versioning data...
git commit -m "Add sampled data %date% %time% and version with DVC"
if %errorlevel% neq 0 (
    echo Git commit failed.
    exit /b 1
)

git tag -a "v1.1" -m "add data version v1.1"
if %errorlevel% neq 0 (
    echo Git tag failed.
    exit /b 1
)

dvc push
if %errorlevel% neq 0 (
    echo DVC push failed.
    exit /b 1
)

git push
if %errorlevel% neq 0 (
    echo Git push failed.
    exit /b 1
)

endlocal
