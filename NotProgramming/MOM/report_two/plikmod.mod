# PARAMETRY
# Stan poczatkowy
set Z;
# Zakupione surowce, s1 i s2
set S; set S1; set S2;
# Surowiec S1 zaladowany do wagonow
set G1;
# Surowce w przygotowywalni
set P; set P1; set P2;
# Surowiec S2 w zakladzie obrobki cieplnej
set O2;
# Polprodukty 
set D; set D1; set D2;
# Wyroby
set W; set W1; set W2;
# Stany surowcow, zakupione, wyroby, obrobka cieplna
set N; set Nz; set Nw; set Nzw;

# Cena sprzedazy wyrobu
param r{w in W};
# Przepustowosc przeplwyu z jednego stanu do drugiego
param u{i in N, j in N};
# Mnoznik definijujacy przepwy ze stanu surowiec
# w przygotowalni do stanu polprodukt
param m{p in P, d in D};

# ZMIENNE DECYZYJNE
# przeplyw pomiedzy stanem i a stanem j
var f{i in N, j in N}, >= 0, integer; # Ograniczenie 1

# Zmienne pomocnicze
# liczba zakupionego surowca S1 powyzej 2387 ton
var a1, >= 0, integer; # Ograniczenie 5
# liczba zakupionego surowca S1 powyzej 6659 ton
var a2, >= 0, integer; # Ograniczenie 6
# liczba zakupionego surowca S2 powyzej 2090 ton
var b1, >= 0, integer; # Ograniczenie 7
# liczba zakupionego surowca S2 powyzej 4349 ton
var b2, >= 0, integer; # Ograniczenie 8
# liczba wynajetych lokomotyw
var wl, >= 0, integer;
# liczba wagonow transportujacych surowiec S1 do przygotowalni
var cp1, >= 0, integer;
# liczba ciezarowek transportujacych surowiec S2 do przygotowalni
var ep2, >= 0, integer; 
# liczba ciezarowek transportujacych surowiec S2
# do zakladu obrobki cieplnej
var eo2, >= 0, integer;
var e1, >= 0, <=1, integer;
var e2, >= 0, <=1, integer;
# Liczba pracownikow
var l, >= 0, integer;

maximize Q: (sum {i in N, w in W} r[w] * f[i,w])
- (19* (sum {z in Z, s1 in S1} f[z, s1] )
- 5*a1 
- 4*a2 
+ 11*  sum {z in Z, s2 in S2} (f[z, s2])
+ 2*b1 
+ 2*b2
+ 1290*cp1
+ 1500*ep2 
+ 1500*eo2 
+ 160*l 
+ 10000*e1 
+ 40000*e2);

# OGRANICZENIA
subject to
  # Ogolne i Dostepne surowce
  Ogr_1_3_4{i in N, j in N}:
    f[i,j] <= u[i,j];
  Ogr_2{k in Nzw}:
    sum {i in Nz} f[k,i] = sum {j in Nw} f[j,k];    
  # Koszt zakupu surowcow
  Ogr_9{z in Z, s1 in S1}:
    a1 <= f[z,s1] - 2387;
  Ogr_10{z in Z, s1 in S1}:
    a2 <= f[z,s1] - 6659;
  Ogr_11{z in Z, s2 in S2}:
    b1 >= f[z,s2] - 2090;
  Ogr_l2{z in Z, s2 in S2}:
    b2 >= f[z,s2] - 4349;
  # Transport surowca S1
  Ogr_13{s1 in S1, g1 in G1}:
   cp1 >= f[s1,g1] / 18;
  # Transport surowca S2
  Ogr_14{s2 in S2, p2 in P2}:
    ep2 >= f[s2,p2] / 25;
  # Praca przygotowalni
  Ogr_15: 
    sum {i in N, p in P} f[i,p] <= 16000;
  Ogr_16{p in P, d in D}:
    (sum {i in N} f[i,p]) * m[p,d] = f[p,d];
  # Koszt pracy przygotowalni
  Ogr_17: 
    l >= (sum {i in N, p in P} f[i,p])/150;
  # Transprot S2 do obrobki cieplnej
  Ogr_18{s2 in S2, o2 in O2}:
    eo2 >= f[s2,o2] / 25;
  # Praca zakladu obrobki cieplnej
  Ogr_19{s2 in S2, o2 in O2}:
    f[s2,o2] <= 6000;
  # Minimalna dostarczona ilosc wyrobow
  Ogr_20{w in W}:
   	sum {i in N} f[i,w] >= 5000;
  # Na jedna lokomotywe przypada co najwyzej 12 wagonow
  Ogr_21:
   12 * wl >= cp1;
  
solve;
display {i in N, j in N: f[i,j] > 0}: f[i,j];
display: a1; display: a2; display: b1; display: b2; display: wl;
display: cp1; display: ep2; display: eo2; display: 
e1; display: l;