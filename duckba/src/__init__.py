from Tools.Directories import fileExists
from os import symlink
from Tools.HardwareInfo import HardwareInfo

try:
    if not fileExists('/tmp/fw_env.config'):
        model = HardwareInfo().get_device_name()
        if model == 'spark' and fileExists('/usr/lib/enigma2/python/Plugins/Extensions/DuckBA/bin/fw_env.config.spark'):
            symlink('/usr/lib/enigma2/python/Plugins/Extensions/DuckBA/bin/fw_env.config.spark', '/tmp/fw_env.config')
        elif model == 'spark7162' and fileExists('/usr/lib/enigma2/python/Plugins/Extensions/DuckBA/bin/fw_env.config.spark7162'):
            symlink('/usr/lib/enigma2/python/Plugins/Extensions/DuckBA/bin/fw_env.config.spark7162', '/tmp/fw_env.config')
    if not fileExists('/usr/lib/enigma2/python/Plugins/Extensions/DuckBA/bin/fw_printenv'):
            symlink('/usr/lib/enigma2/python/Plugins/Extensions/DuckBA/bin/fw_setenv', '/usr/lib/enigma2/python/Plugins/Extensions/DuckBA/bin/fw_printenv')
except OSError:
    pass