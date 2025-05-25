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

float minimalAverageProfit = ...; //wymagany poziom zysku

dvar int produce[months][products];
dvar int sell[months][products];
dvar int stock[months][products];

dvar float workTime[months][machines][products];

dvar boolean if80prec[months][products];

dvar float lowerProfit[scenarios][months][products];

dexpr float profit[i in scenarios] = sum(m in months, p in products) 
(sell[m][p]*sellProfit[i][p]-lowerProfit[i][m][p]- stock[m][p]*storageCost);

dexpr float averageProfit = sum(i in scenarios)(profit[i])/numberOfScenarios;

dexpr float riskMeasureGini = sum (t1 in scenarios, t2 in scenarios ) (
			0.5 * abs(profit[t1] - profit[t2]) * 1/numberOfScenarios * 1/numberOfScenarios
		);

minimize riskMeasureGini;

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
  	averageProfit>=minimalAverageProfit;
  
}
 
main {
   var file = new IloOplOutputFile("result-minimalAverageProfit.txt");
   
   var mod  = thisOplModel;
   var def  = mod.modelDefinition;
   var data = mod.dataElements;
   var maxAvgProfit = 10048;
   var i = 1;
  
   file.writeln("i;minimalAverageProfit;averageProfit;riskMeasureGini;m1_prod_P1;m1_prod_P2;m1_prod_P3;m1_prod_P4;m2_prod_P1;m2_prod_P2;m2_prod_P3;m2_prod_P4;m3_prod_P1;m3_prod_P2;m3_prod_P3;m3_prod_P4;m1_stock_P1;m1_stock_P2;m1_stock_P3;m1_stock_P4;m2_stock_P1;m2_stock_P2;m2_stock_P3;m2_stock_P4;m3_stock_P1;m3_stock_P2;m3_stock_P3;m3_stock_P4");
   
	 data.minimalAverageProfit = -600.0;
     
     	while (data.minimalAverageProfit <= maxAvgProfit) {
       		mod = new IloOplModel (def, cplex);
       		mod.addDataSource(data);
       		mod.generate();
       		cplex.tilim = 10;
       		cplex.solve();
       		file.writeln(i,";",data.minimalAverageProfit,";",mod.averageProfit,";",mod.riskMeasureGini,";",mod.produce[1][1],";",mod.produce[1][2],";",mod.produce[1][3],";",mod.produce[1][4], ";",mod.produce[2][1],";",mod.produce[2][2],";",mod.produce[2][3],";",mod.produce[2][4],";",mod.produce[3][1],";",mod.produce[3][2], ";",mod.produce[3][3],";",mod.produce[3][4],";",mod.stock[1][1],";",mod.stock[1][2],";",mod.stock[1][3],";",mod.stock[1][4], ";",mod.stock[2][1],";",mod.stock[2][2],";",mod.stock[2][3],";",mod.stock[2][4],";",mod.stock[3][1],";",mod.stock[3][2], ";",mod.stock[3][3],";",mod.stock[3][4]);
       		writeln(i," minimalAverageProfit: ",data.minimalAverageProfit," averageProfit: ",mod.averageProfit,", riskMeasureGini: ",mod.riskMeasureGini);
       		mod.end();
       		data.minimalAverageProfit = data.minimalAverageProfit + 532.41;
       		i = i+1;
     	};
  
   
   file.close();
}