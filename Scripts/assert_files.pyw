import os
import sys
import winreg
import pickle
import platform

# Defining this projects path
project_path = os.path.abspath("")


def premature_exit(error):
    with open(project_path + "{}".format("\\Saves\\General Info\\errors.txt"), 'w') as txt:
        if error:
            txt.write(error)
        else:
            txt.write("None")
    with open(project_path + "{}".format("\\Saves\\General Info\\clear run.txt"), 'w') as do_we_run:
        do_we_run.write("False")
    raise SystemExit


if not os.path.exists(project_path + "/Saves"):
    premature_exit('Error: Could not find the folder "{}\\Saves"'.format(project_path))

if not os.path.exists(project_path + "/Saves/Player saves"):
    premature_exit('Error: Could not find the folder "{}\\Saves\\Player saves"'.format(project_path))

if not os.path.exists(project_path + "/Saves/General info"):
    premature_exit('Error: Could not find the folder "{}\\Saves\\General info"'.format(project_path))

# The versions i am supporting
# This is basically information about the size of the console, used in interactive choices
accepted_windows_versions = ('Windows-8', 'Windows-10', 'Windows-8.1')

supported_os = True
version = platform.platform(terse=True)
if version in accepted_windows_versions:
    with open(project_path + "{}".format("/Saves/General Info/Platform.txt"), 'w') as f:
        f.write(version)
else:
    with open(project_path + "{}".format("/Saves/General Info/Platform.txt"), 'w') as f:
        f.write('Windows-10')
    supported_os = False
    with open(project_path + "{}".format("/Saves/General Info/errors.txt", 'w')) as file:
        file.write("Unsupported os. Will use settings for windows 10. Might not work")

audio_path = project_path + "\\Audio\\"
audio_files = ("abc_123_a.ogg",)
missing_audio_files = []
for audio_file in audio_files:
    if not os.path.isfile(audio_path + audio_file):
        missing_audio_files.append(audio_file)

if not len(missing_audio_files) == 0:
    audio_error = "Error: You are missing the following audio files:"
    for missing_audio in missing_audio_files:
        audio_error = audio_error + "\n" + missing_audio
    premature_exit(audio_error)

# We only want to meddle with the registry if we know what we are dealing with
if supported_os:
    # Reading the user's initial values set for the console in case they want to reverse it later
    py_exe_installed = False
    try:
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Console\%SystemRoot%_py.exe", 0,
                                      winreg.KEY_READ)
        quickedit, __ = winreg.QueryValueEx(registry_key, "Quickedit")
        winreg.CloseKey(registry_key)
        py_exe_installed = True
    except WindowsError:
        try:
            registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Console", 0,
                                          winreg.KEY_READ)
            quickedit, __ = winreg.QueryValueEx(registry_key, "Quickedit")
            winreg.CloseKey(registry_key)
        except WindowsError:
            quickedit = 0
            print("You are probably not using windows. Shit might not work")

    try:
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Console", 0,
                                      winreg.KEY_READ)
        legacy, __ = winreg.QueryValueEx(registry_key, "ForceV2")
        winreg.CloseKey(registry_key)
    except WindowsError:
        legacy = None

    with open(project_path + "{}".format("/Saves/General Info/Original settings console.pickle"), 'wb') as f:
        original_console_settings = {'Quickedit': quickedit, 'ForceV2': legacy}
        pickle.dump(original_console_settings, f)

    # Setting registry values of the console for an optimized experience
    # If the option to enable legacy console exists, we want do that
    if legacy is not None:
        path = r"Console"
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, path, 0, winreg.KEY_WRITE)
        winreg.SetValueEx(key, "ForceV2", 0, winreg.REG_DWORD, 0)
        winreg.CloseKey(key)

    # Disabling quickedit
    if py_exe_installed:
        path = r"Console\%SystemRoot%_py.exe"
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, path, 0, winreg.KEY_WRITE)
        winreg.SetValueEx(key, "Quickedit", 0, winreg.REG_DWORD, 0)
        winreg.CloseKey(key)
    else:
        path = r"Console"
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, path, 0, winreg.KEY_WRITE)
        winreg.SetValueEx(key, "Quickedit", 0, winreg.REG_DWORD, 0)
        winreg.CloseKey(key)

# This code will only be reached if no errors are caught
with open(project_path + "{}".format("\\Saves\\General Info\\clear run.txt"), 'w') as f:
    f.write("True")


