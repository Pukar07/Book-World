#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

struct matrix
{
  int r;
  int c;
  double *value;
};

struct matrix_AB
{
  struct matrix *matrix;
};

struct threadVars
{
  int thread_id;
  int slice_value;
  int start;
  int finish;
  struct matrix_AB *matrix_AB;
};

double *allocate_array(int size)
{
  double *array = (double *)malloc(sizeof(double) * size);
  return array;
}

int getIndex(int r, int c, int n_c)
{
  return r* n_c + c;
}

void print_matrix_func(struct matrix M)
{
  int i,j;
  printf("%d,%d\n", M.r, M.c);

  for (i = 0; i < M.r; i++)
  {
    for (j = 0; j < M.c; j++)
    {
      printf("%lf ", M.value[getIndex(i, j, M.c)]);
    }
    printf("\n");
  }
  printf("\n");
}

// declaring the pthread mutex lock
pthread_mutex_t mutex;

// setting the output filename
  char *outputName = "Samir2052250.txt";

void write_matrix(struct matrix M)
{
  FILE *fp;

  // mutex lock locked
  pthread_mutex_lock(&mutex);

  
  // critical section starts
  fp = fopen(outputName, "a");
  fprintf(fp, "%d,%d\n", M.r, M.c);

  for (int i = 0; i < M.r; i++)
  {
    for (int j = 0; j < M.c; j++)
    {
      fprintf(fp, "%lf ", M.value[getIndex(i, j, M.c)]);
    }
    fprintf(fp, "\n");
  }
  fprintf(fp, "\n");

  fclose(fp);
  // critical section finishs
  
  // mutex lock unlocked
//  printf("mutex unlocked...\n");
  pthread_mutex_unlock(&mutex);
}

int false_matrix_mult = 0;

void matrix_multiplication(struct matrix_AB *matrix_AB)
{
  struct matrix A = matrix_AB->matrix[0];
  struct matrix B = matrix_AB->matrix[1];

  if (A.c == B.r)
  {
    struct matrix C;

    C.r= A.r;
    C.c = B.c;
    C.value = allocate_array(C.r* C.c);

    for (int i = 0; i < C.r; i++)
    {
      for (int j = 0; j < C.c; j++)
      {
        C.value[getIndex(i, j, C.c)] = 0.0;
        for (int k = 0; k < B.r; k++)
        {
          C.value[getIndex(i, j, C.c)] += A.value[getIndex(i, k, A.c)] * B.value[getIndex(k, j, B.c)];
        }
        
      }
     
    }

    
    write_matrix(C);
  }
  else
  {
    printf("Unable to perform matrix multiplication\n");
    false_matrix_mult++;
    return;
  }
}


void *matrix_mult_parallelly(void *arg)
{
  
  struct threadVars *data = (struct threadVars *)arg;
  int id = data->thread_id;
  int slice_value = data->slice_value;
  int start = data->start;
  int finish = data->finish;
  struct matrix_AB *matrix_AB = data->matrix_AB;


  printf("Thread %d will perform %d matrix multiplications \n", id, slice_value);

  if (slice_value > 0)
  {
    for (int i = start; i <= finish; i++)
    {
      
      matrix_multiplication(&matrix_AB[i]);
    }
    return NULL;
  }
  
  return NULL;
}

// count total number of multiplications in the fileNames

int multiplicationNum_count_func(char *fileNames[], int n)
{
  int count = 0;

  for (int i = 0; i < n; i++)
  {
    FILE *fp = fopen(fileNames[i], "r");
    if (fp == NULL)
    {
      printf("Error opening file %s\n", fileNames[i]);
      continue;
    }
    else
    {
      printf("File %s was opened\n", fileNames[i]);

      fp = fopen(fileNames[i], "r");

      while (!feof(fp))
      {
        for (int i = 0; i < 2; i++)
        {
          int m, n;
          fscanf(fp, "%d,%d", &m, &n);

          double temp = 0.0;

          for (int i = 0; i < m; i++)
          {
            for (int j = 0; j < n - 1; j++)
            {
              fscanf(fp, "%lf,", &temp);
            }
            fscanf(fp, "%lf\n", &temp);
          }
        }
        count++;
      }
    }

    fclose(fp);
  }

  return count;
}

void matrix_sum_func(struct matrix_AB *matrix_pair_list, char *fileNames[], int n)
{
  
  int matrix_pair_index = 0;

  for (int i = 0; i < n; i++)
  {
    FILE *fp = fopen(fileNames[i], "r");
    if (fp == NULL)
    {
    	continue;
    }
    else
    {
      fp = fopen(fileNames[i], "r");

      while (!feof(fp))
      {
        struct matrix_AB *matrix_pair = (struct matrix_AB *)malloc(sizeof(struct matrix_AB));

        matrix_pair->matrix = (struct matrix *)malloc(sizeof(struct matrix) * 2);

        for (int i = 0; i < 2; i++)
        {
          struct matrix *M;
          M = &matrix_pair->matrix[i];
          fscanf(fp, "%d,%d", &M->r, &M->c);
          
          M->value = allocate_array(M->r* M->c);


          int n = 0;
          double temp = 0.0;

          for (int i = 0; i < M->r; i++)
          {
            // printf("[ ");
            for (int j = 0; j < M->c - 1; j++)
            {
              fscanf(fp, "%lf,", &temp);
              M->value[getIndex(i, j, M->c)] = temp;
            }
            fscanf(fp, "%lf\n", &temp);
            M->value[getIndex(i, M->c - 1, M->c)] = temp;
          }
        }
        matrix_pair_list[matrix_pair_index] = *matrix_pair;
        matrix_pair_index++;

        
        free(matrix_pair);
      }
    }
  }
}

int main( int argc, char *argv[])
{
  if(argc<=1){
  printf("No. of threads not provided!!!\n");
  return 0;
  }		
  int threadNum = atoi(argv[1]);
  int file_count= 1;
  // file names of the input files
  char *fileNames[] = {
       //"SampleMatricesWithErrors.txt"
    //   "SampleMatricesWithErrors.txt",
     // "SampleMatricesWithErrors2.txt",
    //   "SampleMatricesWithErrors3.txt",
  //     "SampleMatricesWithErrors4.txt",
        "SampleMatricesWithErrors5.txt"
  };
 

  // for calculating the total number of matrix multiplications to be performed
  int multiplicationNum = multiplicationNum_count_func(fileNames, file_count);
  printf("\nTotal number of matrix multiplications -> %d\n\n", multiplicationNum);
  
  //printf("Enter number of threads: ");
   while (threadNum >500 || threadNum < 1)
  {
    printf("Number of threads you supplied is not valid.\n");
    printf("Enter number of threads again \n -> ");
    scanf("%d", &threadNum);
    
  }
  printf("\n");
  
  
  if(multiplicationNum < threadNum){
  	threadNum = multiplicationNum;
  	printf("Number of threads is set to %d\n",multiplicationNum);
  }
 
  
  // create a dynamic array to store all the matrix pairs
  struct matrix_AB *matrix_pair_list = (struct matrix_AB *)malloc(sizeof(struct matrix_AB) * multiplicationNum);

  // add all the matrix pairs into the dynamic array
  matrix_sum_func(matrix_pair_list, fileNames, file_count);

  //  diving the total number of matrix multiplications pairs to the number of threads almost equally
  int *sliceList = (int *)malloc(sizeof(int) * threadNum);
  int remainder_values = multiplicationNum % threadNum;

  //  equally distribute the computations among the threads
  for (int i = 0; i < threadNum; i++)
  {
    sliceList[i] = multiplicationNum / threadNum;
  }

  //  to distibute the remaining computations from first to second-last
  for (int i = 0; i < remainder_values; i++)
  {
    sliceList[i] = sliceList[i] + 1;
  }

  //to equally distribute almost equal values for the threads for smooth computation
  int *startList = (int *)malloc(sizeof(int) * threadNum);
  int *finishList = (int *)malloc(sizeof(int) * threadNum);

  for (int i = 0; i < threadNum; i++)
  {
    if (i == 0)
    {
      startList[i] = 0;
    }
    else
    {
      startList[i] = finishList[i - 1] + 1;
    }
    finishList[i] = startList[i] + sliceList[i] - 1;
  }


   struct threadVars *mainStruct = (struct threadVars *)malloc(sizeof(struct threadVars) * threadNum);

   for (int i = 0; i < threadNum; i++)
   {
     mainStruct[i].thread_id = i;
     mainStruct[i].slice_value= sliceList[i];
     mainStruct[i].start = startList[i];
     mainStruct[i].finish = finishList[i];
     mainStruct[i].matrix_AB = matrix_pair_list;


   }



  // creating threads
   pthread_t threads[threadNum];
   
   
	// initiating pthread mutex lock
   pthread_mutex_init(&mutex, NULL);
	
   printf("Initiating %d threads........\n", threadNum);

   // creating and executing threads parallelly
   for (int i = 0; i < threadNum; i++)
   {
     pthread_attr_t attr;
     pthread_attr_init(&attr);

     pthread_create(&threads[i], &attr, matrix_mult_parallelly, (void *)&mainStruct[i]);
   }

   //  joining the threads
   for (int i = 0; i < threadNum; i++)
   {
     pthread_join(threads[i], NULL);
   }
   
   int successfulMatMultiplications= multiplicationNum-false_matrix_mult;

  if(false_matrix_mult >0){
  printf("%d false matrix multiplications",false_matrix_mult);
  }
  
  printf("\nProduct of the given matrices are saved in \"%s\" file...\n", outputName);

// destroying the mutex lock
pthread_mutex_destroy(&mutex);

  // freeing the allocated memory in heap memory
  for (int i = 0; i < multiplicationNum; i++)
  {
    for (int j = 0; j < 2; j++)
    {
      
      free(matrix_pair_list[i].matrix[j].value);
    }
    free(matrix_pair_list[i].matrix);
  }
  free(matrix_pair_list);

  free(sliceList);
  free(startList);
	free(finishList);
	free(mainStruct);
	

  return 0;
}
