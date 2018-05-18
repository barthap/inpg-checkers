@echo off
Title INPG Checkers
set "MISSING_PYTHON=true"
where python > NUL 2>&1 && set "MISSING_PYTHON=false"

IF "%MISSING_PYTHON%"=="false" (
  echo Running python script src/main.py
  python src/main.py
)


IF "%MISSING_PYTHON%"=="true" (
    set "MISSING_PYTHON3=true"
    where python3 > NUL 2>&1 && set "MISSING_PYTHON3=false"
    IF "%MISSING_PYTHON3%"=="true" (
        @echo python not found in path.
        exit /b
    )

    echo Running python3 script src/main.py
    python3 src/main.py
)
