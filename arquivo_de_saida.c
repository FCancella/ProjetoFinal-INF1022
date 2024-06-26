#include <stdio.h>
int main() {

// Declaração de variáveis
int A = 0;
int Y = 0;
int Z = 0;
printf("Z = 0\n");

// Execução do código
Y = 2;
A = 0;
Z = Y;
printf("Z = %d\n",Y);
if (A)
{
for (int i = 0; i < Y; i++)
{
Z = (Z * 2);
printf("Z = %d\n",(Z * 2));
}
A = (A + 3);
}
else
{
Z = (Z * 3);
printf("Z = %d\n",(Z * 3));
A = (A + 1);
}

// Exibindo valores das variáveis
printf("A=%d, Y=%d, Z=%d", A, Y, Z);

return 0;
}