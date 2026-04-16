#include <windows.h> // FOR MAC USERS use <sys/mount.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>
#include <time.h>
unsigned __int64 global_file_count = 0; // PROGRESS TRACKEING
void set_color(int color) {
    SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), color);
}
//SIZE CALCUALTON
unsigned __int64 get_folder_size(const char* sz_path) {
    char sz_find[MAX_PATH];
    WIN32_FIND_DATA find_file_data;
    unsigned __int64 size = 0;
    // WINDWOS API CALL
    int len = (int)strlen(sz_path);
    if (len == 0 || len > MAX_PATH - 3) return 0;

    if (sz_path[len - 1] == '\\') sprintf(sz_find, "%s*", sz_path);
    else sprintf(sz_find, "%s\\*", sz_path);

    HANDLE h_find = FindFirstFile(sz_find, &find_file_data);
    if (h_find == INVALID_HANDLE_VALUE) return 0;
    do {
        if (strcmp(find_file_data.cFileName, ".") != 0 && strcmp(find_file_data.cFileName, "..") != 0) {
            global_file_count++;
            
            if (find_file_data.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY) {
                char sz_full_sub_path[MAX_PATH];
                sprintf(sz_full_sub_path, "%s\\%s", sz_path, find_file_data.cFileName);
                size += get_folder_size(sz_full_sub_path);
            } else {
                size += ((unsigned __int64)find_file_data.nFileSizeHigh << 32) | find_file_data.nFileSizeLow;
            }
        }
    } while (FindNextFile(h_find, &find_file_data));
    FindClose(h_find);
    return size;
}
int main() {
    srand((unsigned int)time(NULL));
    ULARGE_INTEGER free_bytes_to_caller, total_bytes, free_bytes;
    char path_input[MAX_PATH];
    int choice;
    unsigned __int64 divider;
    char* unit;
    // Animation
    char* username = getenv("USERNAME");
    if (username == NULL) username = "USER";
    char upper_name[100];
    strncpy(upper_name, username, 99);
    upper_name[99] = '\0';
    for(int i = 0; upper_name[i]; i++) upper_name[i] = toupper(upper_name[i]);
    for(int i = 0; i < 10; i++) {
    system("cls");
    set_color(i % 2 == 0 ? 9 : 15);
    printf("==================================================\n");
    printf("         %s'S PRO DISK ANALYZER\n", upper_name);  // %s (will show name of the user laptop name)
    printf("==================================================\n\n");
    printf("   [ BOOTING SYSTEM .");
    for(int j = 0; j < (i % 4); j++) printf(".");
    printf(" ]\n");
    Sleep(15); // VARY ACCORDING TO YOUR NEED (FOR EPILEPTIC PATIENT 150-200 for convience )
    }
    // 2. INPUT HANDLING
    set_color(7);
    printf("\nEnter Drive (C:\\) or Folder Path: ");
    if (fgets(path_input, sizeof(path_input), stdin) == NULL) return 1;
    path_input[strcspn(path_input, "\r\n")] = 0;

    printf("View size in (1: MB, 2: GB): ");
    if (scanf("%d", &choice) != 1) choice = 2;
    
    divider = (choice == 1) ? (1024LL * 1024) : (1024LL * 1024 * 1024);
    unit = (choice == 1) ? "MB" : "GB";

    // 3. SCANNING PHASE
    printf("\n[SCANNING] Analyzing files, please wait...\n");
    global_file_count = 0;
    unsigned __int64 folder_size = get_folder_size(path_input);

    // 4. DATA RETRIEVAL & DISPLAY
    system("cls");
    set_color(11);
    printf("==================================================\n");
    printf("              ANALYSIS COMPLETE :)\n");
    printf("==================================================\n\n");
    set_color(7);

    if (GetDiskFreeSpaceEx(path_input, &free_bytes_to_caller, &total_bytes, &free_bytes)) {
        double total = (double)total_bytes.QuadPart;
        double free = (double)free_bytes.QuadPart;
        double used = total - free;
        double percent_used = (used / total) * 100.0;

        printf("Target: %s\n", path_input);
        printf("Files Found: %I64u\n\n", global_file_count);

        // Folder Size -  double (%.2f) to avoid the rounding error
        set_color(14); 
        printf(">> CURRENT FOLDER SIZE: %.2f %s\n", (double)folder_size / divider, unit);
        set_color(7);

        // Drive Bar
        printf("Drive Usage: [");
        for (int i = 0; i < 20; i++) {
            if (i < (int)(percent_used / 5)) {
                if (percent_used > 90) set_color(12);
                else if (percent_used > 75) set_color(14);
                else set_color(10);
                printf("|");
            } else {
                set_color(8);
                printf(".");
            }
        }
        set_color(7);
        printf("] %.1f%%\n\n", percent_used);

        printf("  TOTAL DRIVE SPACE: %7.1f %s\n", (double)total_bytes.QuadPart / divider, unit); // vary according to users 
        printf("  FREE DRIVE SPACE:     %7.1f %s\n", (double)free_bytes_to_caller.QuadPart / divider, unit);

        printf("\nADVICE: ");
        if (percent_used > 90) {
            set_color(12); printf("CRITICAL! Drive is almost full.\n");
        } else if (folder_size > (total_bytes.QuadPart * 0.5)) {
            set_color(14); printf("This specific folder is taking up over 50%% of your drive!\n");
        } else {
            set_color(10); printf("Everything looks good.\n");
        }
        set_color(7);
    } else {
        set_color(12);
        printf("[ERROR] Could not access drive data. Check path permissions.\n");
        set_color(7);
    }

    printf("\nPress Enter twice to exit...");
    fflush(stdin); getchar(); getchar();
    return 0;
}
