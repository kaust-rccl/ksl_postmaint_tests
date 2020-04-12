ifeq ($(PAWSEY_CLUSTER),zeus)
    CC=mpicc
    CFLAGS=-fopenmp
else
    CC=cc
    CFLAGS=-homp
endif
SRC=mpi_test.c
all:
	$(CC) $(CFLAGS) $(SRC) -o mpi_test
clean:
	rm mpi_test
