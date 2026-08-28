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


