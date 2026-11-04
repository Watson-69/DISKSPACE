#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>
#include <time.h>
#include <dirent.h>    // For directory handling
#include <sys/stat.h>  // For file status/size
#include <sys/mount.h> //MAc users
#include <unistd.h>    // For usleep
typedef unsigned long long uint64;
uint64 global_file_count = 0;
// Replaces Windows SetConsoleTextAttribute with ANSI escape codes
void set_color(int color)
{
    switch (color)
    {
    case 9:
        printf("\033[1;34m");
        break; // Blue
    case 11:
        printf("\033[1;36m");
        break; // Cyan
    case 12:
        printf("\033[1;31m");
        break; // Red
    case 14:
        printf("\033[1;33m");
        break; // Yellow
    case 10:
        printf("\033[1;32m");
        break; // Green
    case 8:
        printf("\033[1;30m");
        break; // Gray
    case 15:
        printf("\033[1;37m");
        break; // White
    default:
        printf("\033[0m");
        break; // Reset
    }
}
// POSIX Recursive Folder Size Calculation
uint64 get_folder_size(const char *sz_path)
{
    DIR *d = opendir(sz_path);
    if (!d)
        return 0;
    struct dirent *entry;
    struct stat st;
    uint64 total_size = 0;
    while ((entry = readdir(d)) != NULL)
    {
        // Ignore "." and ".." to avoid infinite loops
        if (strcmp(entry->d_name, ".") == 0 || strcmp(entry->d_name, "..") == 0)
            continue;

        char path[1024];
        snprintf(path, sizeof(path), "%s/%s", sz_path, entry->d_name);

        if (lstat(path, &st) == 0)
        {
            global_file_count++;
            if (S_ISDIR(st.st_mode))
            {
                total_size += get_folder_size(path);
            }
            else
            {
                total_size += st.st_size;
            }
        }
    }
    closedir(d);
    return total_size;
}
int main()
{
    srand((unsigned int)time(NULL));
    char path_input[1024];
    int choice;
    uint64 divider;
    char *unit;
    // 1. ANIMATION & USERNAME
    char *username = getenv("USER"); // Mac uses "USER"
    if (username == NULL)
        username = "USER";
    char upper_name[100];
    strncpy(upper_name, username, 99);
    for (int i = 0; upper_name[i]; i++)
        upper_name[i] = toupper(upper_name[i]);
    for (int i = 0; i < 10; i++)
    {
        printf("\e[1;1H\e[2J"); // Mac clear screen
        set_color(i % 2 == 0 ? 9 : 15);
        printf("==================================================\n");
        printf("         %s'S MAC PRO DISK ANALYZER\n", upper_name);
        printf("==================================================\n\n");
        printf("   [ BOOTING SYSTEM .");
        for (int j = 0; j < (i % 4); j++)
            printf(".");
        printf(" ]\n");
        usleep(100000); // VARY ACCORDING TO YOUR NEED (FOR EPILEPTIC PATIENT use 400000 for convience )
    }

    // 2. INPUT HANDLING
    set_color(15);
    printf("\nEnter Folder Path: ", username); // ignore this it will run :)
    if (fgets(path_input, sizeof(path_input), stdin) == NULL)
        return 1;
    path_input[strcspn(path_input, "\n")] = 0;
    printf("View size in (1: MB, 2: GB): ");
    if (scanf("%d", &choice) != 1)
        choice = 2;
    divider = (choice == 1) ? (1024ULL * 1024) : (1024ULL * 1024 * 1024);
    unit = (choice == 1) ? "MB" : "GB";
    // 3. SCANNING PHASE
    printf("\n[SCANNING] Analyzing files, please wait...\n");
    global_file_count = 0;
    uint64 folder_size = get_folder_size(path_input);
    // 4. DATA RETRIEVAL & DISPLAY
    struct statfs stats;
    printf("\e[1;1H\e[2J");
    set_color(11);
    printf("==================================================\n");
    printf("              ANALYSIS COMPLETE :)\n");
    printf("==================================================\n\n");
    set_color(15);
    if (statfs(path_input, &stats) == 0)
    {
        uint64 total_bytes = (uint64)stats.f_blocks * stats.f_bsize;
        uint64 free_bytes = (uint64)stats.f_bavail * stats.f_bsize;
        uint64 used_bytes = total_bytes - free_bytes;
        double percent_used = ((double)used_bytes / total_bytes) * 100.0;
        printf("Target: %s\n", path_input);
        printf("Files Found: %llu\n\n", global_file_count);
        set_color(14);
        printf(">> CURRENT FOLDER SIZE: %.2f %s\n", (double)folder_size / divider, unit);
        set_color(15);
        // Usage Bar
        printf("Drive Usage: [");
        for (int i = 0; i < 20; i++)
        {
            if (i < (int)(percent_used / 5))
            {
                if (percent_used > 90)
                    set_color(12);
                else if (percent_used > 75)
                    set_color(14);
                else
                    set_color(10);
                printf("|");
            }
            else
            {
                set_color(8);
                printf(".");
            }
        }
        set_color(15);
        printf("] %.1f%%\n\n", percent_used);
        printf("  TOTAL DRIVE SPACE: %7.1f %s\n", (double)total_bytes / divider, unit); // vary according to users
        printf("  FREE DRIVE SPACE:  %7.1f %s\n", (double)free_bytes / divider, unit);
        printf("\nADVICE: ");
        if (percent_used > 90)
        {
            set_color(12);
            printf("CRITICAL! Drive is almost full.\n");
        }
        else if (folder_size > (total_bytes * 0.5))
        {
            set_color(14);
            printf("This specific folder is taking up over 50%% of your drive!\n");
        }
        else
        {
            set_color(10);
            printf("Everything looks good.\n");
        }
    }
    else
    {
        set_color(12);
        printf("[ERROR] Could not access drive data. Check path permissions.\n");
    }
    set_color(15);
    printf("\nPress Enter to exit...");
    getchar();
    getchar();
    return 0;
}
