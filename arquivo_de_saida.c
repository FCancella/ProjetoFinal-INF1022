#include <stdio.h>
int main() {

// Declara��o de vari�veis
int A = 0;
int Y = 0;
int Z = 0;
printf("Z = 0\n");

// Execu��o do c�digo
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

// Exibindo valores das vari�veis
printf("A=%d, Y=%d, Z=%d", A, Y, Z);

return 0;
}