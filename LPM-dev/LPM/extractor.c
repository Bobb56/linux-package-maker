#include <stdlib.h>
#include <stdio.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <pwd.h>
#include <unistd.h>
#include <string.h>
#include <errno.h>

#include "params.h"


extern unsigned char _binary__LPM_temp_payload_tar_start[];
extern unsigned char _binary__LPM_temp_payload_tar_end[];
extern unsigned char _binary__LPM_temp_payload_tar_size[];


// Définition d'un buffer global pour faire des opérations sur les chaînes de caractères sans mallocs
#define PATH_BUFFER_SIZE 1024
char PATH_BUFFER[PATH_BUFFER_SIZE] = {0};

// ATTENTION : Cette fonction n'est pas safe à utiliser plusieurs fois en même temps dans le même appel de fonction
// Il faut en faire des copies
char* process_path(char* path) {
    struct passwd *pw = getpwuid(getuid());

    if (path[0] == '~') {
        memset(PATH_BUFFER, 0, PATH_BUFFER_SIZE);
        strcpy(PATH_BUFFER, pw->pw_dir);
        strcat(PATH_BUFFER, path + 1);
        return PATH_BUFFER;
    }
    else
        return path;
}


void extract_archive_from_elf(void) {
    size_t size = _binary__LPM_temp_payload_tar_end - _binary__LPM_temp_payload_tar_start;
    FILE *f = fopen(process_path(EXTRACTED_ARCHIVE_NAME), "wb");
    fwrite(_binary__LPM_temp_payload_tar_start, 1, size, f);
    fclose(f);
}

void extract_archive(void) {
    system(EXTRACTING_COMMAND);
    remove(process_path(EXTRACTED_ARCHIVE_NAME));
}


/* Ajoute les droits d'exécution au fichier */
int make_executable(const char *path)
{
    struct stat st;

    /* Récupérer les permissions actuelles */
    if (stat(path, &st) != 0)
        return errno;

    /* Ajouter les bits d'exécution (user, group, others) */
    mode_t new_mode = st.st_mode | S_IXUSR | S_IXGRP | S_IXOTH;

    if (chmod(path, new_mode) != 0)
        return errno;

    return 0;
}



int main() {
    extract_archive_from_elf();
    extract_archive();
    make_executable(process_path(EXTRACTING_LIBNEON_PATH));
    system(process_path(LAUNCH_EXTRACTOR));
    return 0;
}
