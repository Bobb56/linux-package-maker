# Fichier principal de Linux Package Maker
import lpm_builder
import lpm_gui
import sys

def print_help():
    print("Linux Package Maker (LPM)")
    print("LPM builds installation packages for any app")
    print("Usage :")
    print("lpm : open the LPM graphical wizard")
    print("lpm build <config_file>.yaml : build an installation package from the command line, using an existing config file.")


def main():
    if len(sys.argv) == 1:
        lpm_gui.launch_app()
    elif len(sys.argv) == 3 and sys.argv[1] == 'build':
        lpm_builder.build_installer(sys.argv[2])
    else:
        lpm_builder.alert_missing_dependencies_error(print)
        print_help()


if '__main__' == __name__:
    main()
