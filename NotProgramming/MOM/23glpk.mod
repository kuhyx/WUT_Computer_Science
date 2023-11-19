set Wyjscie; 
set Wezly; 
set StartWezly; 
set WyjscieWezly; 
set StartWyjscieWezly; 
set Projekty; 
set Zespoly; 
 
param c{z in Zespoly, p in Projekty}; 
 
var f{i in StartWyjscieWezly, j in StartWyjscieWezly}, >= 0, integer; 
var cmax, >= 0; 
 
minimize Q: cmax; 
 
subject to
  Ograniczenie_jeden{i in StartWyjscieWezly, j in StartWyjscieWezly}: 
    f[i,j] >= 0; 
  Ograniczenie_dwa{i in StartWyjscieWezly, j in StartWyjscieWezly}: 
    f[i,j] <= 1; 
  Ograniczenie_trzy{p in Projekty}: 
    sum {z in Zespoly} f[z,p] = 1; 
  Ograniczenie_cztery{z in Zespoly}: 
    sum {p in Projekty} f[z,p] = 1; 
  Ograniczenie_piec{n in Wezly}: 
    sum {i in WyjscieWezly} f[n,i] = sum {j in StartWezly} f[j,n]; 
	Ograniczenie_szesc{z in Zespoly, p in Projekty}: 
		c[z,p] * f[z,p] <= cmax;
solve;
display {i in Wezly, j in Wezly: f[i,j] > 0}: f[i,j]; 
display: Q;
