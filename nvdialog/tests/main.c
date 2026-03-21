#include <stdlib.h>
#include <nvdialog/nvdialog.h>
#include <stdio.h>

int main(void) {
        /* Initializing the library is important to find which functions to use in each platform, initialize the system and
         * ensure that any runtime dependencies are present */
        if (nvd_init() != 0) {
                puts("Failed to initialize NvDialog.\n");
                exit(EXIT_FAILURE);
        }

        /* Constructing the dialog. */
        NvdDialogBox* dialog = nvd_dialog_box_new(
                "Hello, world!", // Title of the dialog
                "Hello world ! This is a dialog box created using libnvdialog!", // Message of the dialog
                NVD_DIALOG_SIMPLE // What is the dialog representing? (Eg a warning). In this
                                  // case, it represents a simple dialog with no context.
        );

        /* Showing the dialog to the user/client. */
        nvd_show_dialog(dialog);
        /* Freeing the dialog is important since it takes up memory to exist. */
        nvd_free_object(dialog);
        return 0;
}
