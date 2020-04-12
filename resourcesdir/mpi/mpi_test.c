#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>
int main (int argc, char* argv[]){
	MPI_Init(&argc,&argv);

	int rank, nprocs;
	MPI_Comm_rank(MPI_COMM_WORLD,&rank);
	MPI_Comm_size(MPI_COMM_WORLD,&nprocs);
        int sum=0;
        MPI_Reduce(&rank, &sum, 1, MPI_INT ,MPI_SUM, 0, MPI_COMM_WORLD); 
        if (rank == 0)
            printf("Sum is %d\n",sum);
	MPI_Finalize();
	return 0;


} 
