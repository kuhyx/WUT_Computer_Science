#include <stdio.h>
#include <stdlib.h>
char P1,P2; int m,n; int peng;

void welcome()
{
    printf("Heyy there!! I know you don't wanna do your assignment. Lets play HEY THAT'S MY FISH \n");
}
void generate()
{
    printf("Hello again! Please enter the number of rows and columns \n");
    scanf("%d",&m); scanf("%d",&n);
    int a[m][n];
    for (int i=0;i<m;i++)
    {
        for(int j=0;j<n;j++)
        {
            a[i][j]=rand()%4;
            if(a[i][j]==1)
                peng=peng+1;
        }

    }
    printf("The board's been set up! \n");
    for (int i=0;i<m;i++)
    {
        for (int j=0;j<n;j++)
        {
            printf("%d ",a[i][j]);

          }
        printf("\n");
    }
}
int main()
{
    welcome();
    generate();
    return 0;

}


