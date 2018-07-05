import os
import sys
import winreg
import platform
import logging
import json

# Defining this projects path
project_path = os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), os.pardir))


def setup_logger(name, file, level=logging.WARNING):
    # Function to easily create loggers

    handler = logging.FileHandler(file)
    formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(filename)s:%(lineno)d:%(message)s")
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


# Info logger
info_log = setup_logger("Info logging", "{}\\Logs\\logging_info.log".format(project_path), level=logging.INFO)

# Error logger
error_log = setup_logger("Error logging", "{}\\Logs\\logging_errors.log".format(project_path))

setup = '''
{
    "os": null
}
'''
setup = json.loads(setup)

if not os.path.exists("{}\\Saves".format(project_path)):
    error_log.error.error('Error: Could not find the folder "{}\\Saves"'.format(project_path))
    with open("{}\\Saves".format(project_path), 'x') as f:
        pass

if not os.path.exists("{}\\Saves\\/Player saves".format(project_path)):
    error_log.error.error('Error: Could not find the folder "{}\\Saves\\Player saves"'.format(project_path))
    with open("{}\\Saves\\Player saves".format(project_path), 'x') as f:
        pass

if not os.path.exists("{}\\Saves\\Config".format(project_path)):
    error_log.error.error('Error: Could not find the folder "{}\\Saves\\Config"'.format(project_path))
    with open("{}\\Saves\\Config".format(project_path), 'x') as f:
        pass


if not os.path.exists("{}\\Logs".format(project_path)):
    error_log.error.error('Error: Could not find the folder "{}\\Logs"'.format(project_path))
    with open("{}\\Logs".format(project_path), 'x') as f:
        pass

# The versions i am supporting
# This is basically information about the size of the console, used in interactive choices
accepted_operating_systems = ('Windows-8', 'Windows-10', 'Windows-8.1')

supported_os = True
os_version = platform.platform(terse=True)
if os_version in accepted_operating_systems:
    setup['os'] = os_version
else:
    setup['os'] = os_version
    supported_os = False
    error_log.error("Unsupported os: {}. Will use settings for windows 10.".format(os))


audio_path = "{}\\Audio\\".format(project_path)
audio_files = ("abc_123_a.ogg",)
missing_audio_files = []
for audio_file in audio_files:
    if not os.path.isfile(audio_path + audio_file):
        missing_audio_files.append(audio_file)

if not len(missing_audio_files) == 0:
    audio_error = "Error: You are missing the following audio files:"
    for missing_audio in missing_audio_files:
        audio_error = audio_error + "\n" + missing_audio
    error_log.error.error(audio_error)

# We only want to meddle with the registry if we know what we are dealing with
if supported_os:
    # Reading the user's initial values set for the console in case they want to reverse it later
    py_exe_installed = False
    try:
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Console\\%SystemRoot%_py.exe", 0,
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

    try:
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Console", 0,
                                      winreg.KEY_READ)
        legacy, __ = winreg.QueryValueEx(registry_key, "ForceV2")
        winreg.CloseKey(registry_key)
    except WindowsError:
        legacy = None

    # Setting registry values of the console for an optimized experience
    # If the option to enable legacy console exists, we want do that
    if legacy is not None:
        path = "Console"
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, path, 0, winreg.KEY_WRITE)
        winreg.SetValueEx(key, "ForceV2", 0, winreg.REG_DWORD, 0)
        winreg.CloseKey(key)

    # Disabling quickedit
    if py_exe_installed:
        path = "Console\\%SystemRoot%_py.exe"
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, path, 0, winreg.KEY_WRITE)
        winreg.SetValueEx(key, "Quickedit", 0, winreg.REG_DWORD, 0)
        winreg.CloseKey(key)
    else:
        path = "Console"
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, path, 0, winreg.KEY_WRITE)
        winreg.SetValueEx(key, "Quickedit", 0, winreg.REG_DWORD, 0)
        winreg.CloseKey(key)
else:
    quickedit = None
    legacy = None

# Setting up the game settings with json
try:
    with open("{}\\Saves\\Config\\Config.json".format(project_path), 'x') as f:
        pass
except FileExistsError:
    pass

if os.stat("{}\\Saves\\Config\\Config.json".format(project_path)).st_size == 0:
    with open("{}\\Saves\\Config\\Config.json".format(project_path), 'w') as f:
        settings = '''
        {
            "nerd mode": false,
            "Quickedit": null,
            "ForceV2": null
        }
        '''
        settings = json.loads(settings)
        settings['Quickedit'] = quickedit
        settings['ForceV2'] = legacy
        json.dump(settings, f)
else:
    with open("{}\\Saves\\Config\\Config.json".format(project_path), 'r') as f_1:
        test_content = f_1.readlines()
        if test_content[0] == "\n" and len(test_content) == 1:
            with open("{}\\Saves\\Config\\Config.json".format(project_path), 'w') as f_2:
                settings = '''
                        {
                            "nerd mode": false,
                            "Quickedit": null,
                            "ForceV2": null
                        }
                        '''
                settings = json.loads(settings)
                settings['Quickedit'] = quickedit
                settings['ForceV2'] = legacy
                json.dump(settings, f_2)

try:
    with open("{}\\Saves\\Config\\Setup.json".format(project_path), 'x') as f:
        pass
except FileExistsError:
    pass

if os.stat("{}\\Saves\\Config\\Setup.json".format(project_path)).st_size == 0:
    with open("{}\\Saves\\Config\\Setup.json".format(project_path), 'w') as f:
        json.dump(setup, f)

else:
    with open("{}\\Saves\\Config\\Setup.json".format(project_path), 'r') as f_1:
        test_content = f_1.readlines()
        if test_content[0] == "\n" and len(test_content) == 1:
            with open("{}\\Saves\\Config\\Setup.json".format(project_path), 'w') as f_2:
                json.dump(setup, f_2)



