#include<stdio.h>
#include<stdlib.h>
int main(){
    FILE *fptr;
char filename[]="file2.dat";
fptr=fopen(filename,"w");
if(fptr==NULL){
    printf("ERROR IN FILE CREATION");
return 1;
}
fclose(fptr);
return 0;
}