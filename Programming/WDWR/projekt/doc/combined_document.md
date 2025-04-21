## **Politechnika Warszawska Instytut Automatyki i Informatyki Stosowanej**

**Sprawozdanie z projektu na przedmiot Wspomaganie Decyzji w Warunkach Ryzyka**

Krzysztof Rudnicki 307585


## **Spis treści**

| 1 | Treść zadania                                                                                                                                                                                                                                                                                                        | 2                          |
|---|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------|
| 2 | Jednokryterialny model wyboru w warunkach ryzyka z wartością oczekiwaną jako miarą<br>zysku<br>2.1<br>Zbiory indeksowe<br>.<br>2.2<br>Parametry<br>2.3<br>Zmienne<br>2.4<br>Ograniczenia<br>.<br>2.5<br>Funkcja celu                                                                                                 | 3<br>3<br>3<br>4<br>4<br>4 |
| 3 | Dwukryterialny model zysku i ryzyka z wartoscią oczekiwaną jako miarą zysku i od<br>chyleniem maksymalnym jako miarą ryzyka<br>3.1<br>Zbiory indeksowe<br>.<br>3.2<br>Parametry<br>3.3<br>Zmienne<br>3.4<br>Ograniczenia<br>.<br>3.5<br>Metoda punktu odniesienia<br>.                                               | 5<br>5<br>5<br>5<br>5<br>6 |
| 4 | Wyznaczenie parametrów zadania z rozkładu t-Studenta                                                                                                                                                                                                                                                                 | 6                          |
| 5 | Model dla programu AMPL<br>5.1<br>Plik z modelem (.mod)<br>5.2<br>Plik z danymi (.dat)<br>5.3<br>Skrypty uruchomieniowe (.run)                                                                                                                                                                                       | 8<br>8<br>11<br>14         |
| 6 | Rozwiązanie zadania optymalizacji<br>6.1<br>Wyniki dla modelu jednokryterialnego<br>.<br>6.2<br>Wyniki dla modelu dwukryterialnego<br>6.2.1<br>Obraz zbioru rozwiązań efektywnych w przestrzeni ryzyko-zysk<br>.<br>6.2.2<br>Analiza relacji dominacji stochastycznej dla trzech wybranych rozwiązań efek<br>tywnych | 16<br>16<br>19<br>19<br>21 |


## **WDWR 18402**

Rozważamy następujące zagadnienie planowania produkcji:

• Przedsiębiorstwo wytwarza 4 produkty P1,. . . ,P4 na następujących maszynach: 4 szlifierkach, 2 wiertarkach pionowych, 3 wiertarkach poziomych, 1 frezarce i 1 tokarce. Wymagane czasy produkcji 1 sztuki produktu (w godzinach) w danym procesie obróbki zostały przedstawione w poniższej tabeli:

|                   | P1   | P2   | P3   | P4   |
|-------------------|------|------|------|------|
| Szlifowanie       | 0,4  | 0,6  | —    | —    |
| Wiercenie pionowe | 0,2  | 0,1  | —    | 0,6  |
| Wiercenie poziome | 0,1  | —    | 0,7  | —    |
| Frezowanie        | 0,06 | 0,04 | —    | 0,05 |
| Toczenie          | —    | 0,05 | 0,02 | —    |

• Dochody ze sprzedaży produktów (w zł/sztukę) określają składowe wektora losowego **R** = (*R*1*, . . . , R*4) *T* . Wektor losowy **R** opisuje 4-wymiarowy rozkład *t*-Studenta z 5 stopniami swobody, którego wartości składowych zostały zawężone do przedziału [5; 12]. Parametry *µ* oraz **Σ** niezawężonego rozkładu *t*-Studenta są następujące:

$$
\mu = \begin{pmatrix} 9 \\ 8 \\ 7 \\ 6 \end{pmatrix}, \qquad \Sigma = \begin{pmatrix} 16 & -2 & -1 & -3 \\ -2 & 9 & -4 & -1 \\ -1 & -4 & 4 & 1 \\ -3 & -1 & 1 & 1 \end{pmatrix}.
$$

• Istnieją ograniczenia rynkowe na liczbę sprzedawanych produktów w danym miesiącu:

|         | P1  | P2  | P3  | P4  |
|---------|-----|-----|-----|-----|
| Styczeń | 200 | 0   | 100 | 200 |
| Luty    | 300 | 100 | 200 | 200 |
| Marzec  | 0   | 300 | 100 | 200 |

- Jeżeli w danym miesiącu jest sprzedawany produkt P1 lub P2, to musi być również sprzedawany produkt P4 w ilości nie mniejszej niż suma sprzedawanych produktów P1 i P2.
- Istnieje możliwość składowania do 200 sztuk każdego produktu w danym czasie w cenie 1 zł/sztukę za miesiąc. Aktualnie firma nie posiada żadnych zapasów, ale jest pożądane mieć po 50 sztuk każdego produktu pod koniec marca.
- Przedsiębiorstwo pracuje 6 dni w tygodniu w systemie dwóch zmian. Każda zmiana trwa 8 godzin. Można założyć, że każdy miesiąc składa się z 24 dni roboczych.
- 1. Zaproponować jednokryterialny model wyboru w warunkach ryzyka z wartością oczekiwaną jako miarą zysku. Wyznaczyć rozwiązanie optymalne.
- 2. Jako rozszerzenie powyższego zaproponować dwukryterialny model zysku i ryzyka z wartością oczekiwaną jako miarą zysku i odchyleniem maksymalnym jako miarą ryzyka. Dla decyzji **x** *∈ Q* odchylenie maksymalne jest definiowane jako *D*(**x**) = max*t*=1*,...,T |µ*(**x**) *− rt*(**x**)*|*, gdzie *µ*(**x**) oznacza wartość oczekiwaną, *rt*(**x**) realizację dla scenariusza *t*.
	- a. Wyznaczyć obraz zbioru rozwiązań efektywnych w przestrzeni ryzyko–zysk.
	- b. Wskazać rozwiązania efektywne minimalnego ryzyka i maksymalnego zysku. Jakie odpowiadają im wartości w przestrzeni ryzyko–zysk?
	- c. Wybrać trzy dowolne rozwiązania efektywne. Sprawdzić czy zachodzi pomiędzy nimi relacja dominacji stochastycznej pierwszego rzędu. Wyniki skomentować, odnieść do ogólnego przypadku.


## **2 Jednokryterialny model wyboru w warunkach ryzyka z wartością oczekiwaną jako miarą zysku**

W celu rozwiązania postawionego zadania dokonano sformułowania modelu programowania liniowego całkowitoliczbowego. Poniżej przedstawiono zapis matematyczny modelu.

## **2.1 Zbiory indeksowe**

| Zbiór             | Opis                                                 |
|-------------------|------------------------------------------------------|
| P =<br>P1, , P4   | Zbiór wytwarzanych produktów                         |
| T =<br>T1, , T5   | Zbiór typów narzędzi wykorzystywanych przy produkcji |
| M =<br>M1, M2, M3 | Zbiór kolejnych miesięcy produkcji                   |

## **2.2 Parametry**

| Parametr                   | Opis                                                                  |
|----------------------------|-----------------------------------------------------------------------|
| tct                        | Liczba narzędzi typu t [szt]                                          |
| eppup                      | Oczekiwany zysk ze sprzedaży jednej sztuki produktu<br>p [zł]         |
| ttputp                     | Czas wykorzystania maszyny typu<br>t przy produkcji jednej sztuki pro |
|                            | duktu<br>p [godz]                                                     |
| smlmp                      | Limit sprzedaży produktu<br>p w miesiącu<br>m [szt]                   |
| stlp                       | Limit pojemności magazynu na produkt<br>p [szt]                       |
| stcpu                      | Koszt magazynowania jednej sztuki dowolnego produktu [zł]             |
| st0p                       | Początkowy stan magazynowy produktu<br>p [szt]                        |
| dstp                       | Porządany końcowy stan magazynowy produktu<br>p [szt]                 |
| dpm                        | Liczba dni roboczych w każdym miesiącu [d]                            |
| spd                        | Liczba zmian w każdym dniu roboczym [j]                               |
| whps                       | Liczba godzin roboczych w ciągu każdej zmiany [godz]                  |
| whpm =<br>dpm · spd · hps  | Liczba godzin roboczych w ciągu każdego miesiąca [godz]               |
| =<br>attt<br>tct<br>∗ whpm | Dostępna liczba godzin roboczych maszyn typu<br>t w ciągu każdego     |
|                            | miesiąca [godz]                                                       |


## **2.3 Zmienne**

| Zmienna                                            | Opis                                                               |
|----------------------------------------------------|--------------------------------------------------------------------|
| pmp                                                | Liczba sztuk produktu<br>p wyprodukowanych w miesiącu<br>m [szt]   |
| smp                                                | Liczba sztuk produktu<br>p sprzedanych w miesiącu<br>m [szt]       |
| X<br>=<br>tsp<br>smp                               | Całkowita liczba sprzedanych sztuk produktu<br>p                   |
| m∈M                                                |                                                                    |
| =<br>stdmp<br>pmp<br>− smp                         | Liczba sztuk produktu<br>p zmagazynowanych w miesiącu<br>m [szt]   |
| Xm<br>=<br>st0p<br>+<br>stgmp<br>stdm2p<br>m2=1    | Stan magazynowy produktu<br>p na koniec miesiąca<br>m [szt]        |
| X<br>uttmt<br>=<br>pmp<br>∗ ttputp<br>p∈P          | Wykorzystanie czasu pracy maszyny typu<br>t w miesiącu<br>m [godz] |
| X<br>X<br>tstc =<br>stcpu ·<br>stgmp<br>m∈M<br>p∈P | Całkowity koszt wykorzystania magazynów [zł]                       |
| ep = (X<br>tsp<br>· eppup)<br>− tstc               | Wartość zysku całkowitego dla wartości oczekiwanych zysku ze       |
| p∈P                                                | sprzedaży produktów [zł]                                           |

## **2.4 Ograniczenia**

Ograniczenie rynkowe sprzedawanych produktów:

*<sup>s</sup>mp* <sup>6</sup> *smlmp, <sup>∀</sup><sup>m</sup> <sup>∈</sup> M, <sup>∀</sup><sup>p</sup> <sup>∈</sup> <sup>P</sup>*

Ograniczenie sprzedaży produktów w pierszym miesiącu:

$$s\_{1p} \leqslant p\_{1p}, \quad \forall p \in P$$

Ograniczenie sprzedaży produktów w kolejnych miesiącach:

$$s\_{mp} \leqslant p\_{mp} + stg\_{mp}, \quad \forall m \in M \backslash \{1\}$$

Ograniczenie na powiązanie sprzedaży produktu 4 ze sprzedażą produktów 1 i 2:

*<sup>s</sup>m*<sup>4</sup> <sup>&</sup>gt; *<sup>s</sup>m*<sup>1</sup> <sup>+</sup> *<sup>s</sup>m*2*, <sup>∀</sup><sup>m</sup> <sup>∈</sup> <sup>M</sup>*

Ograniczenie pojemności magazynów:

$$stg\_{mp} \leqslant stl\_p, \quad \forall p \in P$$

Ograniczenie na pożądany stan magazynowy na koniec miesiąca 3:

$$stg\_{3p} \geqslant dst\_p, \quad \forall p \in P$$

Ograniczenie wykorzystania czasu pracy narzędzi w danym miesiącu:

*uttmt* 6 *att<sup>t</sup> , ∀t ∈ T, ∀m ∈ M*

## **2.5 Funkcja celu**

Jako funkcję celu przyjęto maksymalizację wartości oczekiwanej zysku: *maximize ep*


# **3 Dwukryterialny model zysku i ryzyka z wartoscią oczekiwaną jako miarą zysku i odchyleniem maksymalnym jako miarą ryzyka**

Model ten został zrealizowany jako rozszerzenie modelu jednokryterialnego o dodatkowe zbiory, parametry, zmienne, ograniczenia i nową funkcję celu.

#### **3.1 Zbiory indeksowe**

| Zbiór              | Opis                                                   |
|--------------------|--------------------------------------------------------|
| S =<br>S1, , S1000 | Zbiór scenariuszy wygenerowanych z rozkładu t-Studenta |

### **3.2 Parametry**

| Parametr | Opis                                                                  |
|----------|-----------------------------------------------------------------------|
| sppups   | Zysk ze sprzedaży jednej sztuki produktu<br>p w scenariuszu<br>s [zł] |

### **3.3 Zmienne**

| Zmienna                                   | Opis                                                                   |
|-------------------------------------------|------------------------------------------------------------------------|
| = (X<br>· sppups)<br>sps<br>tsp<br>− tstc | Wartość zysku całkowitego dla scenariusza<br>s zysku ze sprzedaży      |
| p∈P                                       | produktów [zł]                                                         |
| devs<br>=<br> ep − sps                    | Odchylenie zysku w danym scenariuszu [zł]. Jako, że funkcja            |
|                                           | wartości bezwzględnej jest nieliniowa zmienna została poddana          |
|                                           | linearyzacji z użyciem zmiennych<br>ldevs,<br>Ps,<br>Qs                |
| =<br>ldevs<br>ep − sps                    | Zmienna pomocnicza wykorzystana w linearyzacji odchylenia              |
|                                           | zysku w scenariuszu<br>s                                               |
| Ps                                        | Zmienna pomocnicza wykorzystana w linearyzacji zmiennejk               |
|                                           | devs                                                                   |
| Qs                                        | Zmienna pomocnicza wykorzystana w linearyzacji zmiennej<br>devs        |
| mdev = maxs∈S<br>devs                     | Maksymalne odchylenie zysu [zł]. Jako, że funkcja max jest nie         |
|                                           | liniowa, zmienna została poddana linearyzacji z użyciem zmien          |
|                                           | nych<br>M,<br>Zs                                                       |
| M                                         | Zmienna<br>pomocnicza<br>wykorzystana<br>w<br>linearyzacji<br>zmiennej |
|                                           | mdev                                                                   |
| Zs                                        | Zmienna<br>pomocnicza<br>binarna<br>wykorzystana<br>w<br>linearyzacji  |
|                                           | zmiennej<br>mdev                                                       |
| r =<br>mdev                               | Miara ryzyka, równa maksymalnemu odchyleniu zysku                      |

## **3.4 Ograniczenia**

Ograniczenie związane z linearyzacją zmiennej *devs*:

$$lde v\_{s1} - lde v\_{s2} + P\_{s1} - Q\_{s2} = 0, \quad \forall s\_1, s\_2 \in S$$

Ograniczenie związane z linearyzację zmiennej *mdev*:


$$mdev \geqslant dev\_s, \quad \forall s \in S$$

$$mdev \leqslant dev\_s + M(1 - Z\_s), \quad \forall s \in S$$

$$\sum\_{s \in S} Z\_s = 1$$

## **3.5 Metoda punktu odniesienia**

Jako model preferencji dla modelu dwukryterialnego została wybrana metoda punktu odniesienia. Wprowadza ona zestaw dodatkowych parametrów i zmiennych:

| Parametr  | Opis                                                                            |
|-----------|---------------------------------------------------------------------------------|
| aspep     | Poziom aspiracji oczekiwanego zysku                                             |
| aspr      | Poziom aspiracji ryzyka                                                         |
| λep, λr   | Współczynniki normalizujące, odpowiednio dla zysku i ryzyka. Ze względu na ogól |
|           | ne sformułowanie metody punktu odniesienia jako problemu maksymalizacji,<br>λep |
|           | przyjmie wartość dodatnią, a<br>ujemną.<br>λr                                   |
| β         | Współczynnik pomniejszający wartość ocen wykraczających powyżej poziomu aspi    |
|           | racji                                                                           |
| ε         | Współczynnik składnika regularyzacyjnego                                        |
| Zmienne   | Opis                                                                            |
| ocep, ocr | Wartości indywidualnych funkcji osiągnięć dla zysku i ryzyka                    |
| v         | Zmienna pomocnicza metody punktu odniesienia                                    |

Ograniczenia zmiennej *v* przez wartości indywidualnych funkcji osiągnięć:

*v* 6 *ocep* oraz *v* 6 *oc<sup>r</sup>*

Ograniczenia indywidualnych funkcji osiągnięć:

$$oc\_r \leqslant \lambda\_r (r - asp\_r)$$

$$oc\_r \leqslant \beta \lambda\_r (r - asp\_r)$$

$$oc\_{ep} \leqslant \lambda\_p (ep - asp\_{ep})$$

$$oc\_{ep} \leqslant \beta \lambda\_p (ep - asp\_{ep})$$

Funkcja celu metody punktu odniesienia w postaci dla programowania liniowego:

$$\max \quad v + \varepsilon (oc\_{ep} + oc\_r)$$

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
**5.2 Plik z danymi (**.dat**)**


```
załączniku.
1 # ##########################################################
2 # WDWR 18042 #
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

## **6.2 Wyniki dla modelu dwukryterialnego**

## **6.2.1 Obraz zbioru rozwiązań efektywnych w przestrzeni ryzyko-zysk**

Obraz zbioru rozwiązań efektywnch w przestrzeni ryzyko-zysk został uzyskany poprzez rozwiązanie zadania metody punktu odniesienia dla różnych wartości aspiracji dla zysku oraz ryzyka. Do wykonania obliczeń posłużono się skryptem przedstawionym na [Listing 7.](#page--1-0) Obliczenia przeprowadzono ustalając poziomy aspiracji w wyznaczonych granicach zmienności zysku i ryzyka (wektory nadiru i utopii wyznaczone w kolejnej sekcji). Dla każdego poziomu aspiracji wykorzystano po 10 równoodległych wartości znajdujących się w przedziałach definiowanych przez wektory nadiru i utopii.

Ze względu na duży rozmiar zadania, a przez długi czas obliczeń przy 1000 scenariuszach, zdecydowano się ograniczyć ich liczbę do 50. Niestety nie jest to liczba wystarczająca do przeprowadzenia dokładnych obliczeń, jednak uzyskane wyniki powinny być wystarczające do przedstawienia działania metody.

Fragment wyników działania skryptu obliczeniowego przedstawia [Listing 8.](#page-0-0) Obraz zbioru rozwiązań efektywnych w przestrzeni ryzyko-zysk pokazuje [Rysunek 1.](#page-0-1)

<span id="page-0-0"></span>Listing 8: Skrypt obliczający wartości do wyznaczenia obrazu zbioru rozwiązań efektywnych w przestrzeni ryzyko-zysk. Pełne wyniki dostępne w załączniku.

```
1 ### 39: Solving model for aspirations : 2395 .666667 , 312 .777778
2 CPLEX 12 .8.0.0 : optimal integer solution within mipgap or absmipgap ; ←-
      objective 5 .427722957e -07
3 39 MIP simplex iterations
4 0 branch -and - bound nodes
5 absmipgap = 7 .81092e -07 , relmipgap = 1 .43881
```


```
6 Profit : 2417 .827519
7 Risk : 311 .250020
8 RPM : 0 .000001
9 ### 40: Solving model for aspirations : 2395 .666667 , 0 .000000
10 CPLEX 12 .8.0.0 :
11 < BREAK > ( cplex )
12 CPLEX solution status 13 with fixed integers :
13 aborted in phase II
14 aborted , integer solution exists ; objective -0 .06697476417
15 116486 MIP simplex iterations
16 103313 branch -and - bound nodes
17 absmipgap = 6 .93933e -05 , relmipgap = 0 .00103611
18 Profit : 1432 .148909
19 Risk : 188 .510726
20 RPM : -0 .066975
```
Rozwiązania efektywne minimalnego ryzyka i maksymalnego zysku

Rozwiązania efektywne dla minimalnego ryzyka i maksymalnego zysku wyznaczono wykorzystując skrypt przedstawiony na listingu [Listing 4.](#page--1-0) Na podstwaie wyników jego działania, które przedstawia [Listing 9](#page-0-0) można podać następujące rozwiązania:

- Minimalne ryzyko: *ep* = *−*1000, przy *r* = 0,
- Maksymalny zysk: *ep* = 11987, przy *r* = 2569

Dodatkowo poza zakresem zadania wyznaczonon pozostałe elementy potrzebne do wyznaczenia wektorów nadiru i utopii:

- Maksymalne ryzyko: *ep* = 9193, przy *r* = 2815,
- Minimalny zysk: *ep* = *−*2400*.*00, przy *r* = 0*.*00

```
Wektor nadiru: (−2400, 2815)
```
Wektor utopii: (0*,* 11987)

Listing 9: Skrypt wyznaczający rozwiązania optymalne modelu dwukryterialnego.

```
1 # ########################
2 ### Minimizing profit ###
3 # ########################
4 CPLEX 12 .8.0.0 : optimal integer solution ; objective -2400
5 7 MIP simplex iterations
6 0 branch -and - bound nodes
7 Profit : -2400
8 Risk : 0
9
10 # ########################
11 ### Maximizing profit ###
12 # ########################
13 CPLEX 12 .8.0.0 : optimal integer solution ; objective 11987 .41899
14 32 MIP simplex iterations
15 0 branch -and - bound nodes
16 Profit : 11987
17 Risk : 2569
18
```


```
19 # ######################
20 ### Minimizing risk ###
21 # ######################
22 CPLEX 12 .8.0.0 : optimal integer solution ; objective 0
23 0 MIP simplex iterations
24 0 branch -and - bound nodes
25 Profit : -1000
26 Risk : 0
27
28 # #######################
29 ### Maximizing risk k###
30 # #######################
31 CPLEX 12 .8.0.0 : optimal integer solution ; objective 2815 .995263
32 21837 MIP simplex iterations
33 705 branch -and - bound nodes
34 Profit : 9193
35 Risk : 2815
```
## **6.2.2 Analiza relacji dominacji stochastycznej dla trzech wybranych rozwiązań efektywnych**

Do analizy wybrano następujące scenariusze:

- 1. Maksymalny zysk *ep* = 11987*.*42,
- 2. Poziomy aspiracji *aspep* = 8789*.*89 oraz *asp<sup>r</sup>* = 1876*.*67,
- 3. Poziomy aspiracji *aspep* = 10388*.*44 oraz *asp<sup>r</sup>* = 938*.*33.

Dane do analizy zostały wygenerowane w trakcie przeprowadzania obliczeń do poprzednich podpunktów i są dostępne w załącznikach.

Dystrybuanty zysku przedstawia [Rysunek 2.](#page--1-0)

Na podstawie wykresów możemy stwierdzić, że rozwiązanie dla scenariusza z maksymalnym zyskiem dominuje w sensie FSD pozostałe rozwiązania. Dodatkowo widzimy, że rozwiązanie ze scenariusza 3 dominuje w sensie FSD rozwiązanie scenariusza 2.


![](_page_0_Figure_0.jpeg)

Rysunek 2: Wykres dystrybuant zysku dla poszczególnych rozwiązań


