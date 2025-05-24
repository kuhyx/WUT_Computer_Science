int numberOfMachineTypes = ...;
int numberOfMonths = ...;
int numberOfProductsTypes = ...;

int numberOfHoursInFactory = ...;
int numberOfScenarios = ...;

{int} machines = asSet(1..numberOfMachineTypes);
{int} months = asSet(1..numberOfMonths);
{int} products = asSet(1..numberOfProductsTypes);
{int} scenarios = asSet(1..numberOfScenarios);

int machineCount[machines] = ...;
float timeToProduce[machines][products] = ...;
int maxProductsInMonth[months][products] = ...;

int storageMax[products] = ...;
int storageCost = ...;
int storageStart[products] = ...;

int mu[products] = ...;
int sigma[products][products] = ...;

float sellProfit[scenarios][products] = ...;

dvar int produce[months][products];
dvar int sell[months][products];
dvar int stock[months][products];

dvar float workTime[months][machines][products];

dvar boolean if80prec[months][products];

dvar float lowerProfit[scenarios][months][products];

dexpr float profit[i in scenarios] = sum(m in months, p in products) 
(sell[m][p]*sellProfit[i][p]-lowerProfit[i][m][p]- stock[m][p]*storageCost);

dexpr float averageProfit = sum(i in scenarios)(profit[i])/numberOfScenarios;

maximize averageProfit;

subject to {
  forall(i in scenarios, m in months, mc in machines, p in products) {
    workTime[m][mc][p] >= 0;
    produce[m][p] >= 0;
    sell[m][p] >= 0;
    stock[m][p] >= 0;
    lowerProfit[i][m][p] >= 0;
  }    
	forall(m in months, mc in machines) {
	  sum(p in products) (workTime[m][mc][p]) <= (machineCount[mc]*numberOfHoursInFactory);
  }
 	forall(m in months, p in products, mc in machines) {
 	  workTime[m][mc][p] == produce[m][p]*timeToProduce[mc][p];
  }
 	forall(m in months, p in products) {
 	  sell[m][p] <= maxProductsInMonth[m][p];
  }
    forall(m in months, p in products) {
  	  sell[m][p] <= 0.8*maxProductsInMonth[m][p] + 1000000 * if80prec[m][p];
  	  sell[m][p] >= 0.8*maxProductsInMonth[m][p] * if80prec[m][p];
     }
    forall (i in scenarios,m in months, p in products) {
        lowerProfit[i][m][p] <= 1000000 * if80prec[m][p];
        lowerProfit[i][m][p] <= 0.2 * sell[m][p]*sellProfit[i][p];
        0.2 * sell[m][p]*sellProfit[i][p] - lowerProfit[i][m][p] + 1000000 * if80prec[m][p] <= 1000000;
    }    
  	forall(m in months, p in products) {
  	  if(m == 1) { //pierwszy miesiac
  	   sell[m][p] <= produce[m][p]+storageStart[p];
  	   stock[m][p]==(produce[m][p] + storageStart[p])-sell[m][p];
     }else {	// kolejne miesiace 
       sell[m][p] <= produce[m][p] + stock[m-1][p];
       stock[m][p]==(produce[m][p] + stock[m-1][p])-sell[m][p];
     }
  }
  	forall(m in months, p in products) {
  	  stock[m][p] <= storageMax[p];
  	  if(m == 3) {
  	  	stock[m][p] >= 50;
    }  	  	
   }    	  	
}
