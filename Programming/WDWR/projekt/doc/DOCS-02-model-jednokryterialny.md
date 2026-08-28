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


