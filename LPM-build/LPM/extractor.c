#include <stdlib.h>
#include <stdio.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <pwd.h>
#include <unistd.h>
#include <string.h>
#include <dlfcn.h>

#include "params.h"

// Déclaration des fonctions d'interface avec l'interpréteur Neon
void (*execFile) (char*);
void (*neonInit) (void);
void (*neonExit) (void);


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


void load_neon_functions(void) {
    void *handle = dlopen(EXTRACTING_LIBNEON_PATH, RTLD_LAZY);
    neonInit = dlsym(handle, "neonInit");
    neonExit = dlsym(handle, "neonExit");
    execFile = dlsym(handle, "execFile");
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



int main() {
    extract_archive_from_elf();
    extract_archive();

    load_neon_functions();

    neonInit();
    execFile(EXTRACTOR_PATH);
    neonExit();
    return 0;
}
