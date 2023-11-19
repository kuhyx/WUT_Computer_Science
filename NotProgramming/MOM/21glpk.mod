set Wyjscie; 
set Wezly; 
set StartWezly; 
set WyjscieWezly; 
set StartWyjscieWezly; 
set Projekty; 
set Zespoly; 
 
param u{z in Zespoly, p in Projekty}; 
 
var f{i in StartWyjscieWezly, j in StartWyjscieWezly}, >= 0; 
 
maximize Q: sum {p in Projekty, t in Wyjscie} f[p,t]; 
 
  Ograniczeni_jeden{i in StartWyjscieWezly, j in StartWyjscieWezly}: 
    f[i,j] >= 0; 
  Ograniczeni_dwa{i in StartWyjscieWezly, j in StartWyjscieWezly}: 
    f[i,j] <= 1; 
  Ograniczeni_trzy{p in Projekty, z in Zespoly}: 
    f[z,p] <= u[z,p]; 
  Ograniczeni_cztery{p in Projekty}: 
    sum {z in Zespoly} f[z,p] = 1; 
  Ograniczeni_piec{z in Zespoly}: 
    sum {p in Projekty} f[z,p] = 1; 
  Ograniczeni_szesc{n in Wezly}: 
    sum {i in WyjscieWezly} f[n,i] = sum {j in StartWezly} f[j,n]; 
	solve; 
display {i in Wezly, j in Wezly: f[i,j] > 0}: f[i,j]; 
display: Q;
