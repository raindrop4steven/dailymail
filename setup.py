import sys
from cx_Freeze import setup, Executable

includefiles = ['config.ini']

setup(
    name = "Dailymail spider",
    version = "1.0",
    description = "Dailymail.",
    options = {'build_exe': {'include_files': includefiles}},
    executables = [Executable(script="app.py", icon="icon.ico")])