# LPM (Linux Package Manager)

LPM (Linux Package Maker) est un utilitaire permettant de distribuer des applications Linux.
LPM utilise un fichier de configuration répertoriant les métadonnées de l'application (Nom, Description, Icône, ...)
et ainsi que les fichiers de l'application
LPM compresse toutes ces données en un unique fichier exécutable qui installe automatiquement l'application à son lancement.
Ce fichier est généré avec une extension .lpk (Linux Package), mais reste un simple fichier binaire exécutable
Les applications sont installées localement à chaque utilisateur, et sont stockées dans le dossier ~/.local/opt/nom de l'application
LPM ajoute automatiquement l'application à la liste des applications système, et crée également une pseudo-application appelée Uninstall <nom de l'application> et qui permet de désinstaller proprement l'application

Voici les champs que LPM permet de spécifier pour une application :

## Champs obligatoires :
- AppName: Nom de l'application
- AppDirectory: Dossier principal de l'application
- Launcher: Indique quel fichier doit être lancé au lancement de l'application

## Champs facultatifs :
- Icon: Chemin vers l'icône de l'application
- ShortDescription: Description rapide du type d'application
- Description: Description plus longue
- Terminal: true ou false suivant si l'application doit être lancée dans le terminal ou non
- Author: Auteur de l'application
- Version: Version de l'appliction
- Category: Catégorie principale de l'application
- InstFileName: Nom voulu pour le fichier d'installation généré. Il sera automatiquement affublé de l'extension .lpk
- CompressionMode: Mode de compression des données dans l'exécutable. xz ou gz
- DesktopIcon: true ou false, permet de spécifier si une icône doit être ajoutée au bureau
- Command: Nom de la commande qui permet de lancer l'application depuis n'importe quel shell



# TODO :

Nettoyer un peu le code et Single Point Of Truth
Script postinst et préinst
Interface graphique
