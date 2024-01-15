# 1. Zbiory
set Samochody; 
set Ladowarki; 

# 2. Parametery 
# Najwczesniejszy mozliwy czas rozpoczecia ladowania samochodu s na ladowarce l
param E{s in Samochody, l in Ladowarki}; 
#  Czas ladowania samochodu s na ladowarce l
param D{s in Samochody, l in Ladowarki}; 
#  Czas odjazdu samochodu s
param O{s in Samochody}; 
#  Zysk z realizacji kursu przez samochd s
param Z{s in Samochody}; 
 
# Zmienna decyzyjna
# zmienna okreslajaca godzine rozpoczecia ladowania samochodu s na ladowarce l 
var u{s in Samochody, l in Ladowarki}, >= 0, <= 24; 
# zmienna binarna okreslajaca czy kurs zostanie wykonany 
var y{s in Samochody}, binary; 
#  zmienna binarna okreslajaca czy samochd i jest ladowany po samochodzie j na ladowarce l
var v{i in Samochody, j in Samochody, l in Ladowarki}, binary; 
#  zmienna binarna okreslajaca czy samochd s jest ladowany jako pierwszy na ladowarce l
var p{s in Samochody, l in Ladowarki}, binary;  
#  zmienna binarna okreslajacy czy samochd s jest ladowany na ladowarce l
var k{s in Samochody, l in Ladowarki}, binary; 
var z{i in Samochody, l in Ladowarki}, >= 0, <= 24; 
var x{i in Samochody, j in Samochody, l in Ladowarki}, >= 0, <= 24;
var a{i in Samochody, l in Ladowarki}, >= 0, <= 24;
# a = (u[s, l] + D[s, l]) * k[s, l]
# Funkcja celu
maximize Q: sum {s in Samochody} y[s]*Z[s]; 
 
# Ograniczenia
subject to 
  # Samochd nie moze rozpoczac swojego ladownia przed najwczesniejszym mozliwym czasie ladowania.
  Ogr_1{s in Samochody, l in Ladowarki}: 
    u[s,l] >= E[s, l]; 
  # Samochd moze byc ladowany maksymalnie na jednej ladowarce  
  Ogr_2{s in Samochody}: 
    sum {l in Ladowarki} k[s, l] = y[s];
  # Ladowanie danego samochodu na danej ladowarce moze rozpoczac sie tylko po zakonczeniu poprzedniego ladowania.
  Ogr_3{i in Samochody, j in Samochody, l in Ladowarki: (i != j)}:
     z[i,l] >= x[i, j, l];
     # k[i, l] * u[i, l] >= [u[j, l] + D[j, l]) * v[i, j, l])
  Ogr_4{i in Samochody, l in Ladowarki}:
     v[i, i, l] = 0;
     # k[i, l] * u[i, l] >= [u[j, l] + D[j, l]) * v[i, j, l])
  # Samochd realizujacy dostawe musi ukonczyc ladowanie przed godzina odjazdu
  Ogr_5{s in Samochody}: 
    sum {l in Ladowarki} a[s, l] <= O[s];
    # (u[s, l] + D[s, l]) * k[s, l] <= O[s];
  Ogr_6{j in Samochody}:
    sum {i in Samochody, l in Ladowarki} v[i, j, l] <= 1;
  Ogr_7{i in Samochody}:
    sum {j in Samochody, l in Ladowarki} v[i, j, l] <= 1;
  # Samochd musi byc albo ladowany jako pierwszy albo byc ktryms w kolejnosci ladowania albo nie byc w ogle ladowanym.
  Ogr_8{j in Samochody, l in Ladowarki}: 
    p[j, l] + sum {i in Samochody} v[i, j, l] = k[j, l];
  # Samochd w danej kolejnosci, moze byc tylko raz na wszystkich ladowarkach
  Ogr_9{l in Ladowarki}: 
    sum {s in Samochody} p[s, l] <= 1;
  ### Linearyzacja z
  Ogr_z1{i in Samochody, l in Ladowarki}:
    z[i,l] <= 24*k[i,l];
  Ogr_z2{i in Samochody, l in Ladowarki}:
    z[i,l] <= u[i,l];
  Ogr_z3{i in Samochody, j in Samochody, l in Ladowarki}:
    z[i,l] >= u[i,l]-24*(1-k[i,l]);
  ### Linearyzacja x
  Ogr_x1{i in Samochody, j in Samochody, l in Ladowarki}:
    x[i, j, l] <= 24*v[i, j, l];
  Ogr_x2{i in Samochody, j in Samochody, l in Ladowarki}:
    x[i, j, l] <= (u[j,l] + D[j, l]); 
  Ogr_x3{i in Samochody, j in Samochody, l in Ladowarki}:
    x[i, j, l] >= (u[j,l] + D[j, l])-24*(1-v[i, j, l]);
  ### Linearyzacja a
  Ogr_a1{s in Samochody, l in Ladowarki}:
    a[s, l] <= 24*k[s, l];
  Ogr_a2{s in Samochody, l in Ladowarki}:
    a[s, l] <= (u[s, l] + D[s, l]);
  Ogr_a3{s in Samochody, l in Ladowarki}:
    a[s, l] >= (u[s, l] + D[s, l]) - 24*(1-k[s, l]);
 
solve; 
display Q;
display {s in Samochody, l in Ladowarki: k[s, l] > 0}: u[s, l];
display {s in Samochody}: y[s];
display {i in Samochody, j in Samochody, l in Ladowarki: v[i, j, l] > 0}: v[i, j, l];
display {s in Samochody, l in Ladowarki}: k[s, l];

data;

set Samochody := s1, s2, s3, s4, s5;

set Ladowarki := l1, l2, l3;

param E :=
s1 l1 0 s1 l2 0 s1 l3 0
s2 l1 0 s2 l2 0 s2 l3 0
s3 l1 0 s3 l2 0 s3 l3 0
s4 l1 0 s4 l2 0 s4 l3 0
s5 l1 2 s5 l2 2 s5 l3 2;

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
s5 9;

param Z :=
s1 100
s2 10
s3 200
s4 20
s5 330;

end;