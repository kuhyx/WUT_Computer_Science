set BudynkiNaStart; 
set Budynki; 
set Elektrownie; 
 
param c{i in BudynkiNaStart, j in Budynki}; 
param p{i in BudynkiNaStart, j in Budynki}; 
param Z{e in Elektrownie}; 
 
var f{i in BudynkiNaStart, j in Budynki}, >= 0; 
 
minimize Q: sum {i in Budynki, j in Budynki} c[i,j] * f[i,j]; 
 
subject to 
  Ograniczenie_1{i in BudynkiNaStart, j in Budynki}: 
    f[i,j] >= 0; 
  Ograniczenie_2{i in BudynkiNaStart, j in Budynki}: 
    f[i,j] <= p[i,j]; 
  Ograniczenie_3{e in Elektrownie}: 
      sum {n in BudynkiNaStart} f[n,e] >= Z[e]; 
  Ograniczenie_4{n in Budynki}: 
    sum {i in Budynki} f[n,i] <= sum {j in BudynkiNaStart} f[j,n]; 
 
solve; 
display {i in Budynki, j in Budynki: f[i,j] > 0}: f[i,j]; 