set BudynkiNaStart; 
set Budynki; 
set Elektrownie; 
 
param p{i in BudynkiNaStart, j in Budynki}; 
 
var f{i in BudynkiNaStart, j in Budynki}, >= 0; 
 
maximize Q: sum {i in Budynki, e in Elektrownie} f[i,e]; 
 
subject to 
  Ogr_1{i in BudynkiNaStart, j in Budynki}: 
    f[i,j] >= 0; 
  Ogr_2{i in BudynkiNaStart, j in Budynki}: 
    f[i,j] <= p[i,j]; 
  Ogr_3{n in Budynki}: 
    sum {i in Budynki} f[n,i] <= sum {j in BudynkiNaStart} f[j,n]; 
 
solve; 
display {i in Budynki, j in Budynki: f[i,j] > 0}: f[i,j]; 
display: Q;