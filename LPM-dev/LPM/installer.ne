TEMP_FOLDER = ".LPK.temp"
LPM_DATA_FOLDER = ".LPM"

# Importation des données concernant l'application
import (TEMP_FOLDER + '/appdata')

# Dossier home utilisateur
HOME = getHomePath()

# Dossier d'installation du fichier .desktop
DESKTOP_FOLDER = HOME + "/.local/share/applications"

# Dossier d'installation de l'icône
ICON_FOLDER = HOME + '/.local/opt/' + SafeAppName + '/.LPM'

# Dossier d'installation de l'application
INSTALL_DIR = HOME + '/.local/opt'

# Dossier dans lequel on stocke la commande
COMMAND_FOLDER = HOME + '/.local/bin'



function split(string, separator) do
    parsable_string = "['" + string.replace(separator, "', '") + "']"
    return (eval(parsable_string))
end

function isInPATH(path) do
    PATH = split(getEnvVar("PATH"), ':')
    return (path in PATH)
end

function addToPath(string) do
    PATH = getEnvVar("PATH")
    setEnvVar("PATH", string + ':' + PATH)
end



function lowercase_bool(bool) do
    if (bool) then
        return ('true')
    else
        return ('false')
    end
end

$
This function checks if an app is already installed as a Linux Package
$
function isAlreadyInstalled() do
    try
        readFile(DESKTOP_FOLDER + '/' + SafeAppName + '.desktop')
        return (True)
    except () do
        return (False)
    end
end


function getDesktopEntries() do
    entries = [
        ["Type", "Application"],
        ["Name", AppName],
        ["Terminal", lowercase_bool(Terminal)],
        ["Exec", INSTALL_DIR + '/' + SafeAppName + '/' + Launcher]
    ]

    if (Description != None) then
        entries.append(["Comment", Description])
    end

    if (ShortDescription != None) then
        entries.append(["GenericName", ShortDescription])
    end

    if (Icon != None) then
        entries.append(["Icon", ICON_FOLDER + '/icon.png'])
    end

    if (Category != None) then
        entries.append(["Categories", Category])
    end

    if (Version != None) then
        entries.append(["Version", Version])
    end

    return (entries)
end




function makeDesktopContent(entries) do
    content = "[Desktop Entry]\n"

    foreach (entry, entries) do
        if (len(entry) == 2) then
            content += entry[0] + '=' + entry[1] + '\n'
        end
    end

    content += '\n'

    return (content)
end



$
Returns the absolute path to the desktop
$
function getDesktopPath() do
    copyPath(HOME + "/.config/user-dirs.dirs", TEMP_FOLDER + '/xdg_variables.ne')
    try
        import(TEMP_FOLDER + "/xdg_variables")
    except () do
        pass
    end
    deletePath(TEMP_FOLDER + '/xdg_variables.ne')
    return (XDG_DESKTOP_DIR.replace("$HOME", HOME))
end


function getUninsDesktopEntries() do
    lpm_data_path = INSTALL_DIR + '/' + SafeAppName + '/' + LPM_DATA_FOLDER

    entries = [
        ["Type", "Application"],
        ["Name", "Uninstall " + AppName],
        ["Exec", lpm_data_path + '/neon ' + lpm_data_path + '/uninstaller.ne']
    ]

    if (Icon != None) then
        entries.append(["Icon", ICON_FOLDER + '/icon.png'])
    end

    return (entries)
end


function saveUninsDat(paths) do
    content = "created_paths = " + str(created_paths) + '\nAppName = "' + AppName + '"\nSafeAppName = "' + SafeAppName + '"\n'
    writeFile(INSTALL_DIR + '/' + SafeAppName + '/' + LPM_DATA_FOLDER + "/uninsdat.ne", content)
end

$
This function updates the path value with a new string
It adds a new entry in the existing files among .bashrc, .zshrc, .profile in order to make the changes permanent
$
function update_path(string) do
    if (not isInPATH(string)) then
        files = [
                    HOME + "/.bashrc",
                    HOME + "/.profile",
                    HOME + "/.zshrc"
        ]
        foreach (file, files) do
            try
                content = readFile(file)
                content += '\nexport PATH="' + string + ':$PATH"'
                writeFile(file, content)
            except () do
                pass
            end
        end
        addToPath(string)
    end
end


function main() do
    if (isAlreadyInstalled()) then
        message = "Do you want to update "
    else
        message = "Do you want to install "
    end

    if (confirm(AppName, message + AppName + "?", "yescancel")) then
        # Liste qui va contenir tous les fichiers/dossiers créés à supprimer lors de la désinstallation
        created_paths = []

        # Création du dossier d'installation des applications et de sauvegarde des fichiers .desktop
        makeDirectory(INSTALL_DIR)
        makeDirectory(DESKTOP_FOLDER)

        # Copie de toutes les données de l'application
        copyPath(TEMP_FOLDER + '/' + SafeAppName, INSTALL_DIR + '/' + SafeAppName)

        created_paths.append(INSTALL_DIR + '/' + SafeAppName)

        # Rend le programme de lancement exécutable
        makeExecutable(INSTALL_DIR + '/' + SafeAppName + '/' + Launcher)

        # Crée le fichier .desktop de l'application
        desktop_content = makeDesktopContent(getDesktopEntries())

        # Enregistre le .desktop dans le dossier standard
        desktop_file_path = DESKTOP_FOLDER + '/' + SafeAppName + '.desktop'
        writeFile(desktop_file_path, desktop_content)

        created_paths.append(desktop_file_path)

        if (DesktopIcon == None) then
            DesktopIcon = confirm(AppName, "Do you want to add an icon on the desktop?", "yesno")
        end

        if (DesktopIcon) then
            createSymlink(desktop_file_path, getDesktopPath() + '/' + SafeAppName + '.desktop')
            created_paths.append(getDesktopPath() + '/' + SafeAppName + '.desktop')
        end

        # Création de la commande
        if (Command != None) then

            command_path = COMMAND_FOLDER + "/" + Command
            makeDirectory(COMMAND_FOLDER)

            createSymlink(INSTALL_DIR + '/' + SafeAppName + '/' + Launcher, command_path)
            makeExecutable(command_path)

            update_path(COMMAND_FOLDER)

            created_paths.append(command_path)
        end

        # Rend exécutable l'interpréteur
        makeExecutable(INSTALL_DIR + '/' + SafeAppName + '/' + LPM_DATA_FOLDER + '/neon')

        # Création du .desktop pour le désinstallateur
        unins_desktop_content = makeDesktopContent(getUninsDesktopEntries())
        writeFile(DESKTOP_FOLDER + '/Unins' + SafeAppName + '.desktop', unins_desktop_content)

        created_paths.append(DESKTOP_FOLDER + '/Unins' + SafeAppName + '.desktop')

        # Sauvegarde des fichiers/dossiers à supprimer lors de la désinstallation
        saveUninsDat(created_paths)

        alert(AppName, AppName + " was successfully installed!", "Finish")
    end

    deletePath(TEMP_FOLDER)
end


main()


