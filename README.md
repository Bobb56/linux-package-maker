# LPM (Linux Package Manager)

LPM (Linux Package Maker) est un utilitaire permettant de distribuer des applications Linux.
LPM utilise un fichier de configuration répertoriant les métadonnées de l'application (Nom, Description, Icône, ...) ainsi que les fichiers de l'application.
LPM compresse toutes ces données en un unique fichier exécutable qui installe automatiquement l'application à son lancement.
Ce fichier est généré avec une extension .lpk (Linux Package), mais reste un simple fichier binaire exécutable.
Les applications sont installées localement à chaque utilisateur, et sont stockées dans le dossier ~/.local/opt/<nom de l'application>
LPM ajoute automatiquement l'application à la liste des applications système, et crée également une pseudo-application appelée Uninstall <nom de l'application> et qui permet de désinstaller proprement l'application

## Comment installer LPM

LPM est distribué grâce à LPM, c'est-à-dire en fichier .lpk

Pour l'installer, il suffit de télécharger LPM_installer.lpk dans les releases, puis de l'exécuter.

Tout le reste est automatique.

## Comment utiliser LPM

Linux Package Maker expose la commande `lpm` qui prend en argument un chemin vers un fichier YAML contenant les informations nécessaires à la fabrication du paquet telles que le nom de l'application, le fichier exécutable principal, le dossier contenant toutes les données de l'application, etc.


Voici les champs que l'on peut spécifier dans le fichier YAML :

## Champs obligatoires :
- AppName: Nom de l'application
- AppDirectory: Dossier principal de toute l'arborescence de l'application. Il doit contenir tous les fichiers et dossiers nécessaires au bon fonctionnement de l'application.
Contrairement à la plupart des utilitaires de création de paquets, LPM laisse une liberté totale quant à l'organisation interne de l'arborescence de l'application. Il a seulement besoin de connaître le chemin de l'exécutable principal à l'intérieur de l'arborescence, et c'est le but du champ Launcher

- Launcher: Indique quel fichier doit être lancé au lancement de l'application. Le chemin doit être relatif au dossier AppDirectory

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

Gérer les chemins de manière bien plus propre de manière à ne pas traîner des ../.. si jamais il y en a au début
Faire fonctionner LPM dans un environnement python virtuel contenant tkinter, pyyaml et toutes les libs
Faire une interface graphique pour créer le fichier YAML
Ajouter un système de crypto et de signature
Script postinst et préinst
