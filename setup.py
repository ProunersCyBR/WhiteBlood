import sys
from cx_Freeze import setup, Executable

# Opções para o comando bdist_msi
bdist_msi_options = {
    'upgrade_code': '{66620F3A-DC3A-11E2-B341-002219E9B01E}',
    'add_to_path': False,
    'initial_target_dir': r'[ProgramFilesFolder]\\%s\\%s' % ("ProunersCyBR", "WhiteBlood"),
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name = "WhiteBlood",
    version = "2.0",
    description = "Antiransomware",
    options={'bdist_msi': bdist_msi_options},
    executables = [Executable("WhiteBlood.py", base=base)]
)