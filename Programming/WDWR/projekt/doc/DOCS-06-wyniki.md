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


