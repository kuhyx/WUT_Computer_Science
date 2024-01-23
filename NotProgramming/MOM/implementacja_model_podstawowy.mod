# 1. Zbiory
set Samochody; 
set Ladowarki; 

# 2. Parametery 
# Najwczesniejszy mozliwy czas rozpoczecia ladowania samochodu s na ladowarce l
param E{s in Samochody}; 
#  Czas ladowania samochodu s na ladowarce l
param D{s in Samochody, l in Ladowarki}; 
#  Czas odjazdu samochodu s
param O{s in Samochody}; 
#  Zysk z realizacji kursu przez samochod s
param Z{s in Samochody}; 
 
# Zmienna decyzyjna
# zmienna okreslajaca godzine rozpoczecia ladowania samochodu s
var u{s in Samochody}, >= 0, <= 24; 
# zmienna binarna okreslajaca czy kurs zostanie wykonany 
var y{s in Samochody}, binary; 
#  zmienna binarna okreslajaca czy samochod i jest ladowany po samochodzie j na ladowarce l
var v{i in Samochody, j in Samochody}, binary; 
#  zmienna binarna okreslajacy czy samochod s jest ladowany na ladowarce l
var k{s in Samochody, l in Ladowarki}, binary; 
# Funkcja celu
maximize Q: sum {s in Samochody} y[s]*Z[s]; 
 
# Ograniczenia
subject to 
  # Samochod nie moze rozpoczac swojego ladownia przed najwczesniejszym mozliwym czasie ladowania.
  Ogr_1{s in Samochody}: 
    u[s] >= E[s] * y[s]; 
  # Samochod moze byc ladowany maksymalnie na jednej ladowarce
  Ogr_2{s in Samochody}:
     sum {l in Ladowarki} k[s, l] = y[s];
  # Ladowanie danego samochodu na danej ladowarce moze rozpoczac sie tylko po zakonczeniu poprzedniego ladowania.
  Ogr_3{i in Samochody, j in Samochody, l in Ladowarki: i != j}:
     u[i] + 24 * (1 - v[i, j]) >= (u[j] + D[j, l] - 2 * 24 * (2 = k[j, l] - k[i, l]);
  Ogr_4{i in Samochody, j in Samochody, l in Ladowarki: i != j}: 
    v[i, j] + v[j, i] >= k[i, l] + k[j, l] - 1;  
  # Samochod realizujacy dostawe musi ukonczyc ladowanie przed godzina odjazdu
  Ogr_5{s in Samochody}:    
    u[s] + sum {l in Ladowarki} (D[s, l] * k[s, l]) <= O[s] * y[s];
    
solve; 
display Q;
display {s in Samochody, l in Ladowarki: k[s, l] > 0}: u[s];
display {s in Samochody}: y[s];
display {i in Samochody, j in Samochody: v[i, j] > 0}: v[i, j];
display {s in Samochody, l in Ladowarki: k[s, l] > 0}: k[s, l];