#include <stdio.h>
#include <stdlib.h>
#include <dlfcn.h>
int main(int argc, char **argv) {
    void *handle;
    void * (*dlopen_my)(const char*, int);
    char *error;
    handle = dlopen ("libdl.so", RTLD_LAZY);
    
    if (!handle) {
        fputs (dlerror(), stderr);
        exit(1);
    }
    else {
    	printf("pointer: %u\n", handle);
    }
    dlopen_my = dlsym(handle, "dlopen");
    void *libc = dlopen_my("android.hardware.biometrics.fingerprint@2.1.so", RTLD_LAZY);
    
    if ((error = dlerror()) != NULL)  {
        fprintf (stderr, "%s\n", error);
        exit(1);
    }
    printf("fine %u %u\n", handle, libc);
    dlclose(handle);
}

//cd My_Projects/Music && gcc -rdynamic -o test Test.c -ldl && ./test