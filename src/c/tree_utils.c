#include <stdio.h>
#include <string.h>
#include <stdlib.h>

// char* alloc_memory(){
//     char* str = strdup("Hello World");
//     printf("Memory Allocated...\n");
//     return str;
// }

// void free_memory(char* ptr){
//     printf("Memory Deallocated...\n");
//     free(ptr);
// }

// int sumArray(int *arr, int size){
//     int sum = 0;
//     for(int i = 0; i<size; i++){
//         sum += arr[i];
//     }
//     return sum;
// }

// int* incArray(int *arr, int size){
//     for(int i = 0; i<size; i++){
//         arr[i]++;
//     }
//     return arr;
// }

int* getArray(){
    int *arr = (int*)malloc(10*sizeof(int));
    for(int i = 0; i<10; i++){
        arr[i] = i;
    }
    return arr;
}

void free_memory(int* ptr){
    free(ptr);
}