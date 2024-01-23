#1. Zbiory
set Samochody;
set Ladowarki;
set Kwanty; # 1 kwant czasu - 15 min = 1/4 h

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
# zmienna binarna okreslajaca czy kurs zostanie wykonany 
var y{s in Samochody}, binary;
#  zmienna binarna okreslajaca czy samochód i jest ladowany  na ladowarce l w kwancie czasu k
var v{i in Samochody, l in Ladowarki, k in Kwanty}, binary;
# zmienna  służąca do minimalizowania ogolnego czasu ladowania w symulacji (na wszystkich ladowarkach)
var z;
maximize Q: sum {s in Samochody} y[s]*Z[s] - test * 0.01;

#3. Ograniczenia
subject to 
 # Samochód nie moze rozpoczac swojego ladownia przed najwczesniejszym mozliwym czasie ladowania.
  Ogr_1{s in Samochody, l in Ladowarki, k in Kwanty}: #
    v[s, l, k] * k >= E[s] * 4 * v[s, l, k];
  # Ladowanie danego samochodu na danej ladowarce moze rozpoczac sie tylko po zakonczeniu poprzedniego ladowania.
  Ogr_2{s in Samochody, k in Kwanty}:
     sum {l in Ladowarki} v[s, l, k] <=1;
   # Ladowanie danego samochodu na danej ladowarce moze rozpoczac sie tylko po zakonczeniu poprzedniego ladowania.
  Ogr_3{l in Ladowarki, k in Kwanty}:
     sum {s in Samochody} v[s, l, k] <=1;
  # Uzależnienie k od v 
  Ogr_4{s in Samochody}:
    sum {l in Ladowarki, k in Kwanty} v[s, l, k] * 1/(D[s, l]*4) >= y[s];
  # Samochód realizujący dostawę musi ukończyć ładowanie przed godziną odjazdu
  Ogr_5{s in Samochody, l in Ladowarki, k in Kwanty}:
    v[s, l, k] * k <= (O[s]*4 -1) * y[s];
  # 
  Ogr_6{s in Samochody, l in Ladowarki, k in Kwanty}:
    z >= v[s, l, k] * k;

solve;
display Q;

display {s in Samochody}: y[s];
display {l in Ladowarki, s in Samochody, k in Kwanty}: v[s, l, k];
