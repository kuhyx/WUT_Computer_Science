# 1. Zbiory
set Samochody; 
set Ladowarki; 

# 2. Parametery 
# Najwczesniejszy mozliwy czas rozpoczecia ladowania samochodu s na ladowarce l [x]
param E{s in Samochody}; 
#  Czas ladowania samochodu s na ladowarce l [x]
param D{s in Samochody, l in Ladowarki}; 
#  Czas odjazdu samochodu s [x]
param O{s in Samochody}; 
#  Zysk z realizacji kursu przez samochd s [x]
param Z{s in Samochody}; 
 
# Zmienna decyzyjna
# zmienna okreslajaca godzine rozpoczecia ladowania samochodu s na ladowarce l [x]
var u{s in Samochody}, >= 0, <= 24; 
# zmienna binarna okreslajaca czy kurs zostanie wykonany  [x]
var y{s in Samochody}, binary; 
#  zmienna binarna okreslajaca czy samochd i jest ladowany po samochodzie j na ladowarce l 
var v{i in Samochody, j in Samochody}, binary; 
#  zmienna binarna okreslajacy czy samochd s jest ladowany na ladowarce l [x]
var k{s in Samochody, l in Ladowarki}, binary; 
# a = (u[s, l] + D[s, l]) * k[s, l]
# Funkcja celu [x]
maximize Q: sum {s in Samochody} y[s]*Z[s]; 
 
# Ograniczenia
subject to 
  # Samochód nie moze rozpoczac swojego ladownia przed najwczesniejszym mozliwym czasie ladowania. [x]
  Ogr_1{s in Samochody, l in Ladowarki}: 
    u[s] >= E[s] * y[s]; 
  # Samochód moze byc ladowany maksymalnie na jednej ladowarce   [x]
  Ogr_2{s in Samochody}: 
    sum {l in Ladowarki} k[s, l] = y[s];
  # Ladowanie danego samochodu na danej ladowarce moze rozpoczac sie tylko po zakonczeniu poprzedniego ladowania. [x]
  Ogr_3{i in Samochody, j in Samochody, l in Ladowarki: i != j}:
	u[i] + 2400 * (1 - v[i, j]) >= (u[j] + D[j, l] * v[i, j]) - 4800 * (1 - k[j, l]);
 Ogr_4{i in Samochody, j in Samochody, l in Ladowarki: i != j}: 
   v[i, j] + v[j, i]  >= k[i, l] + k[j, l] - 1;
  # Samochód realizujacy dostawe musi ukonczyc ladowanie przed godzina odjazdu [x]
  Ogr_5{s in Samochody}:    
    u[s] + sum {l in Ladowarki} (D[s, l] * k[s, l]) <= O[s] * y[s];
 
solve; 
display Q;
display {s in Samochody, l in Ladowarki: k[s, l] > 0}: u[s];
#display {s in Samochody}: y[s];
display {i in Samochody, j in Samochody: v[i, j] > 0}: v[i, j];
display {s in Samochody, l in Ladowarki: k[s, l] > 0}: k[s, l];

data;

set Samochody := s1, s2, s3, s4, s5, s6, s7;

set Ladowarki := l1, l2, l3, l4;

param E :=
s1 6 
s2 6 
s3 6 
s5 6
s4 6 
s6 6 
s7 6;

param D :=
s1 l1 4 s1 l2 2 s1 l3 2 s1 l4 1
s2 l1 6 s2 l2 3 s2 l3 3 s2 l4 1.5 
s3 l1 1 s3 l2 0.5 s3 l3 0.5 s3 l4 0.25
s4 l1 8 s4 l2 4 s4 l3 4 s4 l4 2
s5 l1 10 s5 l2 5 s5 l3 5 s5 l4 2.5
s6 l1 18 s6 l2 9 s6 l3 9 s6 l4 4.5 
s7 l1 12 s7 l2 6 s7 l3 6 s7 l4 3;

param O :=
s1 10
s2 10
s3 12
s4 14
s5 12
s6 12
s7 10;

param Z :=
s1 25
s2 25
s3 50
s4 100
s5 25
s6 50
s7 100;

end;
