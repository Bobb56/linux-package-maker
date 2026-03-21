TEMP_FOLDER = ".LPK.temp"
LPM_DATA_FOLDER = ".LPM"

# Importation des données concernant l'application
import (getCurrentPath() + '/' + TEMP_FOLDER + "/appdata")

# Dossier d'installation du fichier .desktop
DESKTOP_FOLDER = getHomePath() + "/.local/share/applications"

# Dossier d'installation de l'icône
ICON_FOLDER = getHomePath() + '/.local/opt/' + AppName + '/.LPM'

# Dossier d'installation de l'application
INSTALL_DIR = getHomePath() + '/.local/opt'



function getDesktopEntries() do
    entries = [
        ["Type", "Application"],
        ["Name", AppName],
        ["Terminal", str(Terminal)],
        ["Exec", INSTALL_DIR + '/' + AppName + '/' + Launcher]
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


function confirm(question) do
    ans = input(question + " (Y/n): ")
    return (ans in ['y', 'Y'] or len(ans) == 0)
end




function getDesktopPath() do
    copyPath(getHomePath() + "/.config/user-dirs.dirs", TEMP_FOLDER + '/xdg_variables.ne')
    try
        import(TEMP_FOLDER + "/xdg_variables")
    except () do
        pass
    end
    deletePath(TEMP_FOLDER + '/xdg_variables.ne')
    return (XDG_DESKTOP_DIR.replace("$HOME", getHomePath()))
end


function getUninsDesktopEntries() do
    entries = [
        ["Type", "Application"],
        ["Name", "Uninstall " + AppName],
        ["Terminal", "True"],
        ["Exec", INSTALL_DIR + '/' + AppName + '/' + LPM_DATA_FOLDER + '/uninstaller']
    ]

    if (Icon != None) then
        entries.append(["Icon", ICON_FOLDER + '/icon.png'])
    end

    return (entries)
end


function saveUninsDat(paths) do
    content = "created_paths = " + str(created_paths) + '\nAppName = "' + AppName + '"\n'
    writeFile(INSTALL_DIR + '/' + AppName + '/' + LPM_DATA_FOLDER + "/uninsdat.ne", content)
end


function main() do
    print("Installing " + AppName + "...")

    # Liste qui va contenir tous les fichiers/dossiers créés à supprimer lors de la désinstallation
    created_paths = []

    # Création du dossier d'installation des applications
    makeDirectory(INSTALL_DIR)

    # Copie de toutes les données de l'application
    print("Copying app data...")
    copyPath(TEMP_FOLDER + '/' + AppName, INSTALL_DIR + '/' + AppName)

    created_paths.append(INSTALL_DIR + '/' + AppName)

    # Rend le programme de lancement exécutable
    makeExecutable(INSTALL_DIR + '/' + AppName + '/' + Launcher)

    # Rend le programme de désinstallation exécutable
    makeExecutable(INSTALL_DIR + '/' + AppName + '/' + LPM_DATA_FOLDER + '/uninstaller')

    # Crée le fichier .desktop de l'application
    desktop_content = makeDesktopContent(getDesktopEntries())

    # Enregistre le .desktop dans le dossier standard
    writeFile(DESKTOP_FOLDER + '/' + AppName + '.desktop', desktop_content)

    created_paths.append(DESKTOP_FOLDER + '/' + AppName + '.desktop')

    if (DesktopIcon) then
        print("Adding desktop icon...")
        writeFile(getDesktopPath() + '/' + AppName + '.desktop', desktop_content)
        created_paths.append(getDesktopPath() + '/' + AppName + '.desktop')
    end

    # Création de la commande
    if (Command != None) then
        content = "#!/bin/sh\n" + INSTALL_DIR + '/' + AppName + '/' + Launcher + ' "$@"'
        command_path = getHomePath() + "/.local/bin/" + Command
        writeFile(command_path, content)
        makeExecutable(command_path)

        created_paths.append(command_path)
    end

    # Création du .desktop pour le désinstallateur
    unins_desktop_content = makeDesktopContent(getUninsDesktopEntries())
    writeFile(DESKTOP_FOLDER + '/Unins' + AppName + '.desktop', unins_desktop_content)

    created_paths.append(DESKTOP_FOLDER + '/Unins' + AppName + '.desktop')

    deletePath(TEMP_FOLDER)

    # Sauvegarde des fichiers/dossiers à supprimer lors de la désinstallation
    saveUninsDat(created_paths)

    print(AppName, "successfully installed!")
    input("Press ENTER to quit...")
end


main()


