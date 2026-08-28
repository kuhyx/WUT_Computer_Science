## **4 Wyznaczenie parametrów zadania z rozkładu t-Studenta**

W celu wyznaczenia wartości oczekiwanej wektora *R* (odpowiadającą parametrowi modelu *eppup*) wykorzystano następującą zależność:

$$E(R) = \mu + \sigma \cdot \frac{\Gamma(\frac{\nu - 1}{2})((\nu + a^2)^{-\frac{\nu - 1}{2}} - (\nu + b^2)^{\frac{\nu - 1}{2}})\nu^{\frac{\nu}{2}}}{2(F\_{\nu}(b) - F\_{\nu}(a))\Gamma(\frac{\nu}{2})\Gamma(\frac{1}{2})}$$

gdzie:


- *µ* wartość oczekiwana dla *R*,
- Γ funkcja gamma Eulera,
- *ν* liczba stopni swobody,
- *F* dystrybuanta standardowego rozkładu t-Studenta *t*(0*,* 1; *ν*) z *ν* stopniami swobody,
- *a* = *α−µ σ* , gdzie *α* to lewy kraniec przedziału,
- *b* = *β−µ σ* , gdzie *β*to prawy kraniec przedziału.

Otrzymano wartości:

*E*(*R*) *<sup>T</sup>* = [8*.*5094*,* 8*.*4710*,* 8*.*1319*,* 6*.*3944]

Do obliczenia wartości oczekiwanej oraz wyznaczenia scenariuszy wykorzystano skrypt napisany w języku *R*. Wygenerowano 1000 scenariuszy testowtych. Użyty skrypt przedstawia Listing 1.

Listing 1: Skrypt w języku *R* do obliczania wartości oczekiwanej wektora *R* i generowania scenariuszy z rozkładu t-Studenta.

```
1 library ( tmvtnorm )
2
3 # t- Stutdet parameters
4 Mu = c(9 , 8 , 7 , 6)
5 Sigma = matrix (c(16 , -2 , -1 , -3 ,
6 -2 , 9 , -4 , -1 ,
7 -1 , -4 , 4 , 1 ,
8 -3 , -1 , 1 , 1) ,
9 nrow =4 , ncol =4)
10 lower _ bound = 5
11 upper _ bound = 12
12
13 # Generate scenarios
14 data <- rtmvt ( n =10000 , mean = mu , sigma = sigma , df =5 , lower =rep ( lower _←-
       bound , 4) , upper =rep ( upper _bound , 4) )
15 write . table ( format (data , digits =15 , drop0trailing = F ) , " data10000 .txt"←-
       , quote =F , sep ="\t", eol ="\n\t", col . names = F , row . names = T )
16 mean <- colMeans ( data )
17
18 E <- function ( idx , Mu , Sigma , v , alfa , beta ) {
19 mu = Mu [ idx ]
20 sigma = Sigma [ idx , idx ]
21 a = ( alfa - mu )/ sigma
22 b = ( beta - mu )/ sigma
23 nom = gamma (( v -1)/2) *
24 (( v + a ^2) ^( -1*(v -1) /2) -
25 ( v + b ^2) ^( -1*(v -1)/2) ) *
26 v ^( v/2)
27 den = 2 * (pt(b , v ) - pt(a , v ) ) * gamma ( v/2) * gamma (1/2)
28 return ( mu + sigma *( nom /den ) )
29 }
30
31 ER1 <- E (1 , Mu , Sigma , 5 , 5 , 12)
32 ER2 <- E (2 , Mu , Sigma , 5 , 5 , 12)
33 ER3 <- E (3 , Mu , Sigma , 5 , 5 , 12)
34 ER4 <- E (4 , Mu , Sigma , 5 , 5 , 12)
```


```
45
46 # Aktualny stan magazynowy [szt]
47 param startingStorage { PRODUCTS } >= 0;
48
49 # Pozadany stan magazynowy na koniec symulacji [szt]
50 param desiredEndStorage { PRODUCTS } >= 0;
51
52 # Liczba dni roboczych w miesiacu [d]
53 param daysPerMonth >= 1;
54
55 # Liczba zmian w ciagu jednego dnia roboczego
56 param shiftsPerDay >= 1;
57
58 # Dlugosc zmiany [ godz ]
59 param hoursPerShift >= 1;
60
61 # Liczba roboczogodzin w miesiacu [ godz ]
62 param workHoursPerMonth = daysPerMonth * shiftsPerDay * hoursPerShift ;
63
64 # Czas pracy narzedzi w danym miesiacu
65 param availableToolTime { t in TOOLS } = toolCount [ t ]* workHoursPerMonth←-
       ;
66
67 # ##########
68 # Zmienne #
69 # ##########
70 # Produkcja produktow
71 var produced { MONTHS , PRODUCTS } >= 0 integer ;
72
73 # Sprzedaz produktow w danym miesiacu
74 var sold { MONTHS , PRODUCTS } >= 0 integer ;
75 var totalSold { p in PRODUCTS } = sum { m in MONTHS } sold [m , p ];
76
77 # Ilosc produktow przekazanych do magazynu w danym miesiacu
78 var stored { m in MONTHS , p in PRODUCTS } = produced [m , p ] - sold [m , p←-
       ];
79
80 # Stan magazynowy na koniec danego miesiaca
81 var storage { m in MONTHS , p in PRODUCTS } =
82 startingStorage [ p ] + sum { m2 in MONTHS : ord( m2 ) <= ord( m ) } ←-
               stored [ m2 , p ];
83
84 # Wykorzystany czas pracy
85 var usedToolTime { m in MONTHS , t in TOOLS } =
86 sum { p in PRODUCTS } produced [m , p ]* toolTimePerUnit [t , p ];
87
88 # Koszt magazynowania
89 var monthlyStorageCost { m in MONTHS } =
90 (sum { p in PRODUCTS } storage [m , p ]) * storageUnitCost ;
91 var totalStorageCost = sum { m in MONTHS } monthlyStorageCost [ m ];
92
93 # Zysk dla wartosci oczekiwanej
94 var expectedSalesProfit =
95 sum { p in PRODUCTS } totalSold [ p ]* expectedProfitPerUnit [ p ];
96 var expectedNetProfit =
97 expectedSalesProfit - totalStorageCost ;
```


```
98
99 # Zysk w danym scenariuszu
100 var scenarioSalesProfit { s in SCENARIOS } =
101 sum { p in PRODUCTS } totalSold [ p ]* scenarioProfitPerUnit [s , p ];
102 var scenarioNetProfit { s in SCENARIOS } =
103 scenarioSalesProfit [ s ] - totalStorageCost ;
104
105 # Odchylenie jako miara ryzyka - zlinearyzowana wartosc bezwzgledna
106 var deviation { s in SCENARIOS } =
107 expectedNetProfit - scenarioNetProfit [ s ];
108 var P { SCENARIOS } >= 0;
109 var Q { SCENARIOS } >= 0;
110 subject to deviationLimit { s1 in SCENARIOS , s2 in SCENARIOS }:
111 deviation [ s1 ] - deviation [ s2 ]+ P [ s1 ] - Q [ s2 ] = 0;
112
113 #var maxDeviation = max {s in SCENARIOS } deviation [s];
114 var maxDeviation ;
115 # Linearyzacja maksymalnego odchylenia jako miary ryzyka
116 param M = 10000;
117 var Z { SCENARIOS } binary ;
118 subject to mdLimit { s in SCENARIOS }:
119 maxDeviation >= deviation [ s ];
120 subject to mdWhere { s in SCENARIOS }:
121 maxDeviation <= deviation [ s ] + M *(1 - Z [ s ]) ;
122 subject to mdOS :
123 sum { s in SCENARIOS } Z [ s ] = 1;
124
125 # Aliasy dla ocenianych wartosci
126 var profit = expectedNetProfit ;
127 var risk = maxDeviation ;
128
129 # ######################
130 # Ograniczenia modelu #
131 # ######################
132
133 # Ograniczenie rynkowe sprzedazy produktow
134 subject to SalesMarketLimit { m in MONTHS , p in PRODUCTS }:
135 sold [m , p ] <= salesMarketLimit [m , p ];
136 # Ograniczenie magazynowe sprzedazy produktow
137 subject to SalesLimit1 { p in PRODUCTS }:
138 sold [ first ( MONTHS ) , p ] <= produced [ first ( MONTHS ) , p ];
139 subject to SalesLimit2 { m in MONTHS , p in PRODUCTS : m != first ( MONTHS←-
       ) }:
140 sold [m , p ] <= produced [m , p ] + storage [m , p ];
141 # Powiazanie sprzedazy produktu P4 ze sprzedaza produktow P1 i P2
142 subject to P4SalesConstraint { m in MONTHS }:
143 sold [m , "P4"] >= sold [m , "P1"] + sold [m , "P2"];
144 # Ograniczenie pojemnosci magazynowej
145 subject to StorageLimit { m in MONTHS , p in PRODUCTS }:
146 storage [m , p ] <= storageLimit [ p ];
147 # Ograniczenie na pozadany stan magazynowy na koniec marca
148 subject to DesiredStorage { p in PRODUCTS }:
149 storage [ last ( MONTHS ) , p ] >= desiredEndStorage [ p ];
150 # Ograniczenie czasu pracy narzedzi w miesiacu
151 subject to ToolWorkTime { m in MONTHS , t in TOOLS }:
152 usedToolTime [m , t ] <= availableToolTime [ t ];
```


```
153
154 # ############################
155 # Metoda punktu odniesienia #
156 # ############################
157 # Skladniki wektora oceny
158 set RATED = {" PROFIT ", " RISK "};
159 # Wektor oceny
160 var value { r in RATED } =
161 if r == " PROFIT " then profit
162 else if r == " RISK " then risk ;
163 # Wektor aspiracji
164 param aspiration { RATED };
165 # Wartosci utopii i nadiru
166 param utopia { RATED };
167 param nadir { RATED };
168 # Wspolczynniki normalizujace
169 param lambda { r in RATED } =
170 1 / ( utopia [r] - nadir [r]);
171 # Wspolczynnik skladnika regularyzacyjnego
172 param epsilon ;
173 # Wspolczynnik pomniejszenia wartosci ocen ponad poziomem aspiracji
174 param beta ;
175 # Indywidualne funkcje osiagniec
176 var individualRating { RATED };
177 # Zmienna pomocnicza metody punktu odniesienia
178 var v;
179 # Skalaryzujaca funkcja osiagniecia
180 var rating = v + epsilon * (sum {r in RATED } individualRating [r]);
181 # Odleglosc od punktu odniesienia
182 var distance {r in RATED } = value [r] - aspiration [r];
183 # Znormalizowana odleglosc od punktu odniesienia
184 var normalizedDistance {r in RATED } = lambda [r]* distance [r];
185 # Ograniczenia zmiennej v przez indywidualne funkcje osiagniec
186 subject to VSubject {r in RATED }:
187 v <= individualRating [r];
188 # Ograniczenia indywidualnych funkcji osiagniec
189 subject to IndividualRatingSubjectBeta {r in RATED }:
190 individualRating [r] <= beta * normalizedDistance [r];
191 subject to IndividualRatingSubject {r in RATED }:
192 individualRating [r] <= normalizedDistance [r];
193
194 ################
195 # Funkcje celu #
196 ################
197 minimize MinimizeProfit : profit ;
198 maximize MaximizeProfit : profit ;
199 minimize MinimizeRisk : risk ;
200 maximize MaximizeRisk : risk ;
201 maximize RPM: rating ;
```
