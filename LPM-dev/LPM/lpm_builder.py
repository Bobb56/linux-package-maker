"""
LPM (Linux Package Maker) est un utilitaire permettant de distribuer des applications Linux.
LPM utilise un fichier de configuration répertoriant les métadonnées de l'application (Nom, Description, Icône, ...)
et ainsi que les fichiers de l'application
LPM compresse toutes ces données en un unique fichier exécutable qui installe automatiquement l'application à son lancement.
Ce fichier est généré avec une extension .lpk (Linux Package), mais reste un simple fichier binaire exécutable
Les applications sont installées localement à chaque utilisateur, et sont stockées dans le dossier ~/.local/opt/nom de l'application
LPM ajoute automatiquement l'application à la liste des applications système, et crée également une pseudo-application appelée Uninstall <nom de l'application> et qui permet de désinstaller proprement l'application

Voici les champs que LPM permet de spécifier pour une application :

Champs obligatoires :
---------------------
AppName: Nom de l'application
AppDirectory: Dossier principal de l'application
Launcher: Indique quel fichier doit être lancé au lancement de l'application

Champs facultatifs :
--------------------
Icon: Chemin vers l'icône de l'application
ShortDescription: Description rapide du type d'application
Description: Description plus longue
Terminal: true ou false suivant si l'application doit être lancée dans le terminal ou non
Author: Auteur de l'application
Version: Version de l'appliction
Category: Catégorie principale de l'application
InstFileName: Nom voulu pour le fichier d'installation généré. Il sera automatiquement affublé de l'extension .lpk
CompressionMode: Mode de compression des données dans l'exécutable. xz ou gz
DesktopIcon: true ou false, permet de spécifier si une icône doit être ajoutée au bureau
Command: Nom de la commande qui permet de lancer l'application depuis n'importe quel shell
"""


import os
import sys
import yaml
import shutil
import tarfile
from distutils.dir_util import copy_tree

dependencies = ["objcopy", "gcc"]


EXTRACTOR_SCRIPT_NAME = "installer.ne"
UNINSTALLER_BINARY_C_FILE = "uninstaller.c"
UNINSTALLER_BINARY_LAUNCHER = "uninstaller"
UNINSTALLER_SCRIPT_NAME = "uninstaller.ne"
EXTRACTOR_DATAFILE_NAME = "appdata.ne"
MAIN_C_FILE = "extractor.c"

# Définition des noms données aux attributs
APP_DIRECTORY = "AppDirectory"
APP_NAME = "AppName"
ICON = "Icon"
INST_NAME = "InstFileName"
COMPRESSION_MODE = "CompressionMode"

LPM_TEMP_DIR = ".LPM.temp"

ARCHIVE_NAME = LPM_TEMP_DIR + "/payload.tar"
HEADER_FILE_NAME = LPM_TEMP_DIR + "/params.h"
ICON_FILE_NAME = "icon.png"

# Dossier que l'on ajoute dans l'arborescence de l'application pour y stocker l'icône et le fichier desktop
LPM_DATA_DIRECTORY = ".LPM"

LPM_EXTRACTING_DIR = ".LPK.temp"

INSTALL_DIRECTORY = "~/.local/opt"


def failwith(error):
    print(error)
    sys.exit()


def has_command(cmd):
    return shutil.which(cmd) is not None


def check_dependencies(commands):
    for command in commands:
        if shutil.which(command) is None:
            return False
    return True

def get_missing_dependencies_error_message(dependencies):
    return f"Please ensure to have installed the following commands on your system :\n{'-' + '\n-'.join(dependencies)}"


def alert_missing_dependencies_error(display_function):
    if not check_dependencies(dependencies):
        display_function(get_missing_dependencies_error_message(dependencies))
        sys.exit()



def get_installation_dir():
    if getattr(sys, 'frozen', False):
        # Exécutable PyInstaller
        return os.path.dirname(sys.executable)
    else:
        # Script Python normal
        return os.path.dirname(os.path.abspath(__file__))

def get_location_in_installation_dir(file):
    return get_installation_dir() + '/' + file

def get_working_dir():
    return os.getcwd()

def get_location_in_temp_dir(file):
    return get_working_dir() + '/' + LPM_TEMP_DIR + '/' + file

def copy_to_temp_dir(*args):
    for file in args:
        shutil.copyfile(get_location_in_installation_dir(file), get_location_in_temp_dir(file))



def create_folder(path):
    try:
        os.mkdir(path)
    except:
        pass

def delete_folder(path):
    try:
        shutil.rmtree(path)
    except:
        pass



def make_header(name, args):
    """
    args est un dictionnaire (nom, valeur)
    la fonction make_header crée un fichier headers C du nom `name` associant chaque nom avec chaque valeur
    """
    f = open(name, "w+")
    for (name, value) in args.items():
        f.write(f"#define {name} \"{value}\"\n")
    f.close()



def make_extractor_strings(config):
    EXTRACTED_ARCHIVE_NAME = ".archive.tar"
    EXTRACTING_LIBNEON_PATH = LPM_EXTRACTING_DIR + '/' + config[APP_NAME] + '/' + LPM_DATA_DIRECTORY + '/' + 'neon'
    LAUNCH_EXTRACTOR = EXTRACTING_LIBNEON_PATH + ' ' + LPM_EXTRACTING_DIR + '/' + EXTRACTOR_SCRIPT_NAME

    return {
        "EXTRACTING_LIBNEON_PATH"   : EXTRACTING_LIBNEON_PATH,
        "LIBNEON_PATH"              : INSTALL_DIRECTORY + '/' + config[APP_NAME] + '/' + LPM_DATA_DIRECTORY + '/neon',
        "LAUNCH_EXTRACTOR"          : LAUNCH_EXTRACTOR,
        "EXTRACTED_ARCHIVE_NAME"    : EXTRACTED_ARCHIVE_NAME,
        "EXTRACTING_COMMAND"        : f"tar -xf {EXTRACTED_ARCHIVE_NAME}",
        "UNINSTALLER_PATH"          : INSTALL_DIRECTORY + '/' + config[APP_NAME] + '/' + LPM_DATA_DIRECTORY + '/' + UNINSTALLER_SCRIPT_NAME
    }


def make_extractor_datafile(name, args):
    f = open(name, "w+")
    for (name, value) in args.items():
        f.write(f"{name} = {str([value])[1:-1]}\n")
    f.close()


def load_config(config_file):
    with open(config_file, "r") as file:
        config = yaml.safe_load(file)

    # Checking if all required entries are present

    REQUIRED = ["AppName", "AppDirectory", "Launcher"]
    DEFAULT_VALUES = {
        "Icon" : None,
        "ShortDescription" : None,
        "Description" : None,
        "Terminal" : False,
        "Author" : None,
        "Version" : None,
        "Category" : None,
        "InstFileName" : config[APP_NAME] + "_installer",
        "CompressionMode" : "",
        "DesktopIcon" : None,
        "Command" : None
    }


    for entry in REQUIRED:
        if not (entry in config):
            failwith(f"Entry \"{entry}\" is required in {config_file}")

    for entry in config:
        if (not (entry in REQUIRED)) and (not (entry in DEFAULT_VALUES)):
            failwith(f"Unknown entry \"{entry}\"")

    # Add default values for missing entries

    for entry in DEFAULT_VALUES:
        if not (entry in config):
            config[entry] = DEFAULT_VALUES[entry]


    # Transformation des chemins relatifs au fichier de config en chemins absolus
    config_directory = getFileDirectory(config_file)

    config[ICON] = solve_relative_path(config_directory, config[ICON]) if config[ICON] else config[ICON]
    config[APP_DIRECTORY] = solve_relative_path(config_directory, config[APP_DIRECTORY])

    return config


def solve_relative_path(containing_folder, path):
    if path[0] != '/':
        return containing_folder + '/' + path
    else:
        return path


def compress_directory(config, compress_method):
    archive_name = ARCHIVE_NAME
    directory = LPM_TEMP_DIR + '/' + LPM_EXTRACTING_DIR

    with tarfile.open(archive_name, f"w:{compress_method}") as tar:
        tar.add(directory, arcname=os.path.basename(directory))


def getFileDirectory(filepath):
    folders = filepath.split('/')
    folders.pop()

    if folders == []:
        return '.'
    else:
        return '/'.join(folders)






def build_installer(config_file):
    alert_missing_dependencies_error(print)

    # Création du dossier temporaire de travail
    create_folder(LPM_TEMP_DIR)

    config = load_config(config_file)

    print(f"Packaging {config[APP_NAME]}...")

    # Création du header pour donner les constantes au fichier C
    make_header(HEADER_FILE_NAME, make_extractor_strings(config))

    # Ajout des fichiers source au dossier temporaire de travail de LPM
    copy_to_temp_dir(MAIN_C_FILE, "neon", EXTRACTOR_SCRIPT_NAME, UNINSTALLER_SCRIPT_NAME)

    # Création du dossier temporaire de travail de l'extracteur
    create_folder(LPM_TEMP_DIR + '/' + LPM_EXTRACTING_DIR);

    # Ajoute le script d'extraction
    shutil.copyfile(LPM_TEMP_DIR + '/' + EXTRACTOR_SCRIPT_NAME, LPM_TEMP_DIR + '/' + LPM_EXTRACTING_DIR + '/' + EXTRACTOR_SCRIPT_NAME)

    # Création du fichier de constantes pour le script d'extraction
    make_extractor_datafile(LPM_TEMP_DIR + '/' + LPM_EXTRACTING_DIR + '/' + EXTRACTOR_DATAFILE_NAME, config)

    # Ajout de toute l'arborescence de l'application
    copy_tree(config[APP_DIRECTORY], LPM_TEMP_DIR + '/' + LPM_EXTRACTING_DIR + '/' + config[APP_NAME])

    # Crée le sous-dossier dans l'arborescence de l'application utilisé pour stocker notamment l'icone et les scripts de désinstallation
    create_folder(LPM_TEMP_DIR + '/' + LPM_EXTRACTING_DIR + '/' + config[APP_NAME] + '/' + LPM_DATA_DIRECTORY)

    # Ajoute la bibliothèque dynamique Neon
    shutil.copyfile(LPM_TEMP_DIR + '/' + "neon", LPM_TEMP_DIR + '/' + LPM_EXTRACTING_DIR + '/' + config[APP_NAME] + '/' + LPM_DATA_DIRECTORY + '/' + 'neon')

    # Ajoute l'icône
    if config[ICON]:
        shutil.copyfile(config[ICON], LPM_TEMP_DIR + '/' + LPM_EXTRACTING_DIR + '/' + config[APP_NAME] + '/' + LPM_DATA_DIRECTORY + '/' + ICON_FILE_NAME)

    # Ajoute le désinstallateur
    shutil.copyfile(LPM_TEMP_DIR + '/' + UNINSTALLER_SCRIPT_NAME, LPM_TEMP_DIR + '/' + LPM_EXTRACTING_DIR + '/' + config[APP_NAME] + '/' + LPM_DATA_DIRECTORY + '/' + UNINSTALLER_SCRIPT_NAME)

    # Compression de l'archive complète
    compress_directory(config, config[COMPRESSION_MODE])

    # Transformation de l'archive en fichier objet
    os.system(f"objcopy --input binary --output elf64-x86-64 --binary-architecture i386:x86-64 {ARCHIVE_NAME} \"{LPM_TEMP_DIR}/payload.o\"")

    os.system(f"gcc \"{LPM_TEMP_DIR}/{MAIN_C_FILE}\" \"{LPM_TEMP_DIR}/payload.o\" -lm -o \"{config[INST_NAME]}.lpk\"")

    print(f"{config[APP_NAME]} successfully packaged in {config[INST_NAME]}.lpk")


    # Suppression du dossier temporaire de travail
    delete_folder(LPM_TEMP_DIR)
