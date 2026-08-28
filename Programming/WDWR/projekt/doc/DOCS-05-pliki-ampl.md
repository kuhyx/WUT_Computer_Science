**5.2 Plik z danymi (**.dat**)**


```
załączniku.
1 # ##########################################################
2 # WDWR 25406 #
3 # Planowanie produkcj w warunkach ryzyka. #
4 # DANE #
5 # Autor : Jan Kumor #
6 # ##########################################################
7
8 # Narzedzia
9 set TOOLS := GRINDER VDRILL HDRILL MILLER LATHE ;
10
11 # Miesiace
12 set MONTHS := JAN FEB MAR ;
13
14 # Liczba narzedzi
15 param toolCount :=
16 GRINDER 4
17 VDRILL 2
18 HDRILL 3
19 MILLER 1
20 LATHE 1
21 ;
22
23 # Czasy produkcji h
24 param toolTimePerUnit :
25 P1 P2 P3←-
                               P4 :=
26 GRINDER 0 .4 0 .6 0 ←-
             0
27 VDRILL 0 .2 0 .1 0 ←-
             0 .6
28 HDRILL 0 .1 0 0 .7 ←-
             0
29 MILLER 0 .06 0 .04 0 0 .05
30 LATHE 0 0 .05 0 .02 0
31 ;
32
33 # Ograniczenia rynkowe liczby sprzedawanych produktow pcs
34 param salesMarketLimit :
35 P1 P2 P3 ←-
                       P4 :=
36 JAN 200 0 100 ←-
             200
37 FEB 300 100 200 ←-
             200
38 MAR 0 300 100 ←-
             200
39 ;
40
41 # Ograniczeine liczby magazynowanych produktow pcs
42 param storageLimit :=
43 P1 200
44 P2 200
45 P3 200
46 P4 200
```
Listing 3: Dane dla modelu AMPL - pominięto scenariusze, pełny zestaw danych dostępny w


```
47 ;
48
49 # Koszt magazynowania produktow pln/pcs per month
50 param storageUnitCost := 1;
51
52 # Aktualny stan magazynowy pcs
53 param startingStorage :=
54 P1 0
55 P2 0
56 P3 0
57 P4 0
58 ;
59
60 # Pozadany stan magazynowy na koniec marca pcs
61 param desiredEndStorage :=
62 P1 50
63 P2 50
64 P3 50
65 P4 50
66 ;
67
68 # Liczba dni roboczych w miesiacu d
69 param daysPerMonth := 24;
70
71 # Liczba zmian w ciagu jednego dnia roboczego
72 param shiftsPerDay := 2;
73
74 # Dlugosc zmiany h
75 param hoursPerShift := 8;
76
77 # Zyski wartosc oczekiwana
78 param expectedProfitPerUnit :=
79 P1 8 .50944172786882
80 P2 8 .47100593224391
81 P3 8 .1319049712769
82 P4 6 .39446520538826
83 ;
84
85 # Metoda punktu odniesienia
86 param epsilon = 0 .000025 ;
87
88 param beta = 0 .001 ;
89
90 param utopia :=
91 PROFIT 11987
92 RISK 1000
93 ;
94
95 param nadir :=
96 PROFIT -2400
97 RISK 2815
98 ;
99
100 param aspiration :=
101 PROFIT 10000
102 RISK 0
```


*smp* oraz wartość wyznaczonego rozwiązania optymalnego:

*ep* = 11987*.*42[*z*]

Listing 7: Wynik działania skryptu wyznaczającego rozwiązanie optymalne modelu jednokryterialnego.

| 1  |                                                                        |                                    | # ################################################ |         |  |         |  |            |  |  |           |              |  |  |  |
|----|------------------------------------------------------------------------|------------------------------------|----------------------------------------------------|---------|--|---------|--|------------|--|--|-----------|--------------|--|--|--|
| 2  | ###<br>Maximize<br>profit<br>for<br>expected<br>profit<br>value<br>### |                                    |                                                    |         |  |         |  |            |  |  |           |              |  |  |  |
| 3  | # ################################################                     |                                    |                                                    |         |  |         |  |            |  |  |           |              |  |  |  |
| 4  | CPLEX                                                                  |                                    | 12 .8.0.0 :                                        | optimal |  | integer |  | solution ; |  |  | objective | 11987 .41899 |  |  |  |
| 5  |                                                                        | 11<br>MIP<br>simplex<br>iterations |                                                    |         |  |         |  |            |  |  |           |              |  |  |  |
| 6  |                                                                        | 0<br>branch -and - bound<br>nodes  |                                                    |         |  |         |  |            |  |  |           |              |  |  |  |
| 7  |                                                                        | produced                           | :=                                                 |         |  |         |  |            |  |  |           |              |  |  |  |
| 8  | JAN                                                                    | P1                                 | 200                                                |         |  |         |  |            |  |  |           |              |  |  |  |
| 9  | JAN                                                                    | P2                                 | 0                                                  |         |  |         |  |            |  |  |           |              |  |  |  |
| 10 | JAN                                                                    | P3                                 | 100                                                |         |  |         |  |            |  |  |           |              |  |  |  |
| 11 | JAN                                                                    | P4                                 | 200                                                |         |  |         |  |            |  |  |           |              |  |  |  |
| 12 | FEB                                                                    | P1                                 | 200                                                |         |  |         |  |            |  |  |           |              |  |  |  |
| 13 | FEB                                                                    | P2                                 | 0                                                  |         |  |         |  |            |  |  |           |              |  |  |  |
| 14 | FEB                                                                    | P3                                 | 200                                                |         |  |         |  |            |  |  |           |              |  |  |  |
| 15 | FEB                                                                    | P4                                 | 200                                                |         |  |         |  |            |  |  |           |              |  |  |  |
| 16 | MAR                                                                    | P1                                 | 50                                                 |         |  |         |  |            |  |  |           |              |  |  |  |
| 17 | MAR                                                                    | P2                                 | 250                                                |         |  |         |  |            |  |  |           |              |  |  |  |
| 18 | MAR                                                                    | P3                                 | 150                                                |         |  |         |  |            |  |  |           |              |  |  |  |
| 19 | MAR                                                                    | P4                                 | 250                                                |         |  |         |  |            |  |  |           |              |  |  |  |
| 20 | ;                                                                      |                                    |                                                    |         |  |         |  |            |  |  |           |              |  |  |  |
| 21 |                                                                        |                                    |                                                    |         |  |         |  |            |  |  |           |              |  |  |  |
| 22 | sold                                                                   | :=                                 |                                                    |         |  |         |  |            |  |  |           |              |  |  |  |
| 23 | JAN                                                                    | P1                                 | 200                                                |         |  |         |  |            |  |  |           |              |  |  |  |
| 24 | JAN                                                                    | P2                                 | 0                                                  |         |  |         |  |            |  |  |           |              |  |  |  |
| 25 | JAN                                                                    | P3                                 | 100                                                |         |  |         |  |            |  |  |           |              |  |  |  |
| 26 | JAN                                                                    | P4                                 | 200                                                |         |  |         |  |            |  |  |           |              |  |  |  |
| 27 | FEB                                                                    | P1                                 | 200                                                |         |  |         |  |            |  |  |           |              |  |  |  |
| 28 | FEB                                                                    | P2                                 | 0                                                  |         |  |         |  |            |  |  |           |              |  |  |  |
| 29 | FEB                                                                    | P3                                 | 200                                                |         |  |         |  |            |  |  |           |              |  |  |  |
| 30 | FEB                                                                    | P4                                 | 200                                                |         |  |         |  |            |  |  |           |              |  |  |  |
| 31 | MAR                                                                    | P1                                 | 0                                                  |         |  |         |  |            |  |  |           |              |  |  |  |
| 32 | MAR                                                                    | P2                                 | 200                                                |         |  |         |  |            |  |  |           |              |  |  |  |
| 33 | MAR                                                                    | P3                                 | 100                                                |         |  |         |  |            |  |  |           |              |  |  |  |
| 34 | MAR                                                                    | P4                                 | 200                                                |         |  |         |  |            |  |  |           |              |  |  |  |
| 35 | ;                                                                      |                                    |                                                    |         |  |         |  |            |  |  |           |              |  |  |  |
| 36 |                                                                        |                                    |                                                    |         |  |         |  |            |  |  |           |              |  |  |  |
| 37 | stored                                                                 | :=                                 |                                                    |         |  |         |  |            |  |  |           |              |  |  |  |
| 38 | JAN                                                                    | P1                                 | 0                                                  |         |  |         |  |            |  |  |           |              |  |  |  |
| 39 | JAN                                                                    | P2                                 | 0                                                  |         |  |         |  |            |  |  |           |              |  |  |  |
| 40 | JAN                                                                    | P3                                 | 0                                                  |         |  |         |  |            |  |  |           |              |  |  |  |
| 41 | JAN                                                                    | P4                                 | 0                                                  |         |  |         |  |            |  |  |           |              |  |  |  |
| 42 | FEB                                                                    | P1                                 | 0                                                  |         |  |         |  |            |  |  |           |              |  |  |  |
| 43 | FEB                                                                    | P2                                 | 0                                                  |         |  |         |  |            |  |  |           |              |  |  |  |
| 44 | FEB                                                                    | P3                                 | 0                                                  |         |  |         |  |            |  |  |           |              |  |  |  |
| 45 | FEB                                                                    | P4                                 | 0                                                  |         |  |         |  |            |  |  |           |              |  |  |  |
| 46 | MAR                                                                    | P1                                 | 50                                                 |         |  |         |  |            |  |  |           |              |  |  |  |
| 47 | MAR                                                                    | P2                                 | 50                                                 |         |  |         |  |            |  |  |           |              |  |  |  |
| 48 | MAR                                                                    | P3                                 | 50                                                 |         |  |         |  |            |  |  |           |              |  |  |  |
| 49 | MAR                                                                    | P4                                 | 50                                                 |         |  |         |  |            |  |  |           |              |  |  |  |


52 Profit: 11987.418989


![](_page_0_Figure_0.jpeg)

<span id="page-0-1"></span>Rysunek 1: Obraz zbioru rozwiązań efektywnych w przestrzeni ryzyko-zysk

