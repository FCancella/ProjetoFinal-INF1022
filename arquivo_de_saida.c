#include <stdio.h>
int main() {

// Declaração de variáveis
int Y = 0;
int A = 0;
printf("A = 0\n");
int Z = 0;
printf("Z = 0\n");

// Execução do código
Y = 2;
A = 0;
printf("A = %d\n",A);
Z = Y;
printf("Z = %d\n",Z);
if (A)
{
for (int i = 0; i < Y; i++)
{
Z = (Z * 2);
printf("Z = %d\n",Z);
}
A = (A + 3);
printf("A = %d\n",A);
}
else
{
Z = (Z * 3);
printf("Z = %d\n",Z);
A = (A + 1);
printf("A = %d\n",A);
}

// Exibindo valores das variáveis
printf("Y=%d, A=%d, Z=%d", Y, A, Z);

return 0;
}