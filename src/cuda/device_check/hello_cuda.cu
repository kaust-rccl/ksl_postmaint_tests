#include <stdio.h>
#include <cuda.h>
int devCount;
int myid;
int ihavecuda;
int deviceselector=0;


int main(void) {

    cudaGetDeviceCount(&devCount);
    if (devCount == 0) {
        printf("Devcount %4d NONE\n", devCount);
        ihavecuda=0;
    }
    else{
        ihavecuda=1;
        if (devCount >= 1){
            printf("Devcount %4d\n", devCount);
            for (int i = 0; i < devCount; ++i)
            {
                cudaDeviceProp devProp;
                cudaGetDeviceProperties(&devProp, i);
                printf(" devprop name %s i=(%d) \n ", devProp.name, i);
            }
        }
    }


}
