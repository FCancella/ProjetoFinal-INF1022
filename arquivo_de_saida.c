#include <stdio.h>
int main() {

// Declara��o de vari�veis
int A = 0;
int Y = 0;
int Z = 0;

// Execu��o do c�digo
A = 0;
Y = 2;
Z = Y;
if (A)
{
for (int i = 0; i < Y; i++)
{
Z = (Z * 2);
}
A = (A + 3);
}
else
{
Z = (Z * 3);
A = (A + 1);
}

// Exibindo valores das vari�veis
printf("A=%d, Y=%d, Z=%d", A, Y, Z);

return 0;
}