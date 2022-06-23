#include <stdio.h>
#include <stdlib.h>

int main()
{
    int i_one, i_two;
    float f_one, f_two;
    char c_one, c_two;
    printf("Chris\n");
    printf("Write two integers then two float numbers then two characters:");
    scanf("%d %d %f %f %c %c", &i_one, &i_two, &f_one, &f_two, &c_one, &c_two);
    printf("%d %d %d %f %c %d", i_one, i_two, f_one, f_two, c_one, c_two);
    printf("\n%d", i_one + i_two);
    printf("\n%f", i_one / i_two);
    printf("\n%f", f_one / f_two);
    printf("\n%c%d", c_one, i_one);
    return 0;
}
