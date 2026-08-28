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

