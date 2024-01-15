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
#  Zysk z realizacji kursu przez samochód s
param Z{s in Samochody}; 
 
# Zmienna decyzyjna
# zmienna okreslajaca godzine rozpoczecia ladowania samochodu s
var u{s in Samochody}, >= 0, <= 24; 
# zmienna binarna okreslajaca czy kurs zostanie wykonany 
var y{s in Samochody}, binary; 
#  zmienna binarna okreslajaca czy samochód i jest ladowany po samochodzie j na ladowarce l
var v{i in Samochody, j in Samochody}, binary; 
#  zmienna binarna okreslajacy czy samochód s jest ladowany na ladowarce l
var k{s in Samochody, l in Ladowarki}, binary; 
# Funkcja celu
maximize Q: sum {s in Samochody} y[s]*Z[s]; 
 
# Ograniczenia
subject to 
  # Samochód nie moze rozpoczac swojego ladownia przed najwczesniejszym mozliwym czasie ladowania.
  Ogr_1{s in Samochody}: 
    u[s] >= E[s] * y[s]; 
  # Samochód moze byc ladowany maksymalnie na jednej ladowarce
  Ogr_2{s in Samochody}:
     sum {l in Ladowarki} k[s, l] = y[s];
  # Ladowanie danego samochodu na danej ladowarce moze rozpoczac sie tylko po zakonczeniu poprzedniego ladowania.
  Ogr_3{i in Samochody, j in Samochody, l in Ladowarki: i != j}:
     u[i] + 24 * (1 - v[i, j]) >= (u[j] + D[j, l] * v[i, j]);
  # ??? 
  Ogr_4{i in Samochody, j in Samochody, l in Ladowarki: i != j}: 
    v[i, j] + v[j, i] >= k[i, l] + k[j, l] - 1;  
  # Samochód realizujacy dostawe musi ukonczyc ladowanie przed godzina odjazdu
  Ogr_6{s in Samochody}:    
    u[s] + sum {l in Ladowarki} (D[s, l] * k[s, l]) <= O[s] * y[s];
  # Ladowanie samochodu nie bedzie nastepowalo po ladowaniu dowolnego samochodu wiecej niz raz na danej ladowarce
  #Ogr_7_temp{j in Samochody}:
  #  sum {i in Samochody} v[i, j] <= 1;
  # Ladowanie samochodu nie bedzie poprzedzalo ladowania dowolnego samochodu wiecej niz raz na danej ladowarce
  #Ogr_8_temp{i in Samochody}:
  #  sum {j in Samochody} v[i, j] <= 1;
  Ogr_temp:
    u['s4'] = 0;
  Ogr_temp_2:
    k['s4', 'l2'] = 1;
    
solve; 
display Q;
display {s in Samochody, l in Ladowarki: k[s, l] > 0}: u[s];
display {s in Samochody}: y[s];
display {i in Samochody, j in Samochody: v[i, j] > 0}: v[i, j];
display {s in Samochody, l in Ladowarki: k[s, l] > 0}: k[s, l];

data;

set Samochody := s1, s2, s3, s4, s5;

set Ladowarki := l1, l2, l3;

param E :=
s1 0 
s2 0 
s3 0 
s4 0 
s5 2;

param D :=
s1 l1 4 s1 l2 4 s1 l3 8
s2 l1 1 s2 l2 1 s2 l3 2
s3 l1 5 s3 l2 5 s3 l3 10
s4 l1 3 s4 l2 3 s4 l3 6
s5 l1 6 s5 l2 6 s5 l3 12;

param O :=
s1 8
s2 5
s3 6
s4 4
s5 8;

param Z :=
s1 100
s2 10
s3 200
s4 20
s5 330;

end;