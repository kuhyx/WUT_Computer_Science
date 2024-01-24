import pulp
import sys

# Create a problem variable:
model = pulp.LpProblem("Optimal_Distribution", pulp.LpMinimize)
# Zdefiniowanie dostawcy (fabryki and magazyny)
fabryki = ['F1', 'F2']
magazyny = ['M1', 'M2', 'M3', 'M4']
dostawcy = fabryki + magazyny  # Combining both lists
# Zdefiniowanie klientów
klienci = ['K1', 'K2', 'K3', 'K4', 'K5', 'K6']
koszt = {
    'F1': {'M1': 0.3, 'M2': 0.5, 'M3': 1.2, 'M4': 0.8, 'K1': 1.2, 'K2': 999, 
    'K3': 1.2, 'K4': 2.0, 'K5': 999, 'K6': 1.1},
    'F2': {'M1': 999, 'M2': 0.4, 'M3': 0.5, 'M4': 0.3, 'K1': 1.8, 'K2': 999, 
    'K3': 999, 'K4': 999, 'K5': 999, 'K6': 999},
    'M1': {'K1': 999, 'K2': 1.2, 'K3': 0.2, 'K4': 1.7, 'K5': 999, 'K6': 2.0},
    'M2': {'K1': 1.4, 'K2': 0.3, 'K3': 1.8, 'K4': 1.3, 'K5': 0.5, 'K6': 999},
    'M3': {'K1': 999, 'K2': 1.3, 'K3': 2.0, 'K4': 999, 'K5': 0.3, 'K6': 1.4},
    'M4': {'K1': 999, 'K2': 999, 'K3': 0.4, 'K4': 2.0, 'K5': 0.5, 'K6': 1.6}
}
P = pulp.LpVariable.dicts("P", [(i, j) for i in dostawcy for j in klienci], cat='Binary')
maksymalne_zamowienie = 60
poziom_satysfakcji = {'K1': 50 / maksymalne_zamowienie, 'K2': 10 / maksymalne_zamowienie, 'K3': 40 / maksymalne_zamowienie, 'K4': 35 / maksymalne_zamowienie, 'K5': 60 / maksymalne_zamowienie, 'K6': 20 / maksymalne_zamowienie}
preferencja_klienta = {'K1': ['F2'], 'K2': ['M1'], 'K3': ['M2', 'M3'], 'K4': ['F1'], 'K5': [], 'K6': ['M3', 'M4']}
suma_satysfakcji = pulp.lpSum([poziom_satysfakcji[j] * P[(i, j)] for i in dostawcy for j in klienci])


# Zmienne decyzyjne
x = pulp.LpVariable.dicts("x", [(i, j) for i in dostawcy for j in klienci], lowBound=0, cat='Integer')
y = pulp.LpVariable.dicts("y", [(i, k) for i in fabryki for k in magazyny], lowBound=0, cat='Integer')
# Funkcje Celu
koszt_dystrybucji = pulp.lpSum([koszt[i][j] * x[(i, j)] for i in dostawcy for j in klienci])
koszt_magazynowania = pulp.lpSum([koszt[i][k] * y[(i, k)] for i in fabryki for k in magazyny])
alpha = 0.5
beta = 0.5
model += alpha * (koszt_dystrybucji + koszt_magazynowania) - beta * suma_satysfakcji
mozliwosci_fabryki = {'F1': 150, 'F2': 200}
pojemnosc_magazynu = {'M1': 70, 'M2': 50 , 'M3': 100, 'M4': 40 }
zamowienia_klientow = {'K1': 50, 'K2': 10, 'K3': 40, 'K4': 35, 'K5': 60, 'K6': 20}
for i in fabryki:
    model += pulp.lpSum([x[(i, j)] for j in klienci] + [y[(i, k)] for k in magazyny]) <= mozliwosci_fabryki[i]

for k in magazyny:
    model += pulp.lpSum([x[(k, j)] for j in klienci]) <= pojemnosc_magazynu[k]

for j in klienci:
    model += pulp.lpSum([x[(i, j)] for i in dostawcy]) == zamowienia_klientow[j]

model.solve()
for v in model.variables():
    print(v.name, "=", v.varValue)

koszt_wyniki = []
zadowolenie_wyniki = []
wyniki_funkcji = []
maksymalny_wynik = 0;
for alpha in range(0, 11):
    beta = 10 - alpha + sys.float_info.epsilon
    alpha /= 10.0
    beta /= 10.0
    # Update objective function
    model.objective = alpha * koszt_dystrybucji - beta * suma_satysfakcji

    # Solve the model
    model.solve()
    print(alpha)

    # Record the wyniki
    calkowity_koszt = pulp.value(koszt_dystrybucji)
    calkowite_zadowolenie = pulp.value(suma_satysfakcji)
    wynik_funkcji = pulp.value(alpha * koszt_dystrybucji - beta * suma_satysfakcji)
    koszt_wyniki.append(calkowity_koszt)
    zadowolenie_wyniki.append(calkowite_zadowolenie)
    if wynik_funkcji > maksymalny_wynik:
        maksymalny_wynik = wynik_funkcji
    wyniki_funkcji.append(wynik_funkcji)
    
print("maksymalny_wynik", maksymalny_wynik, wyniki_funkcji)

# Pseudo-code, assuming model setup as previously discussed
scemariusze = [(1.0, sys.float_info.epsilon), (0.8, 0.2), (0.5, 0.5), (0.2, 0.8), (sys.float_info.epsilon, 1.0)]
wyniki = []

for alpha, beta in scemariusze:
    model.objective = alpha * koszt_dystrybucji - beta * suma_satysfakcji

    model.solve()

    calkowity_koszt = pulp.value(koszt_dystrybucji)
    calkowite_zadowolenie = pulp.value(suma_satysfakcji)
    wyniki.append((alpha, beta, calkowity_koszt, calkowite_zadowolenie))

for idx, (alpha, beta, koszt, zadowolenie) in enumerate(wyniki):
    print(f"Krok {idx+1}:")
    print(f"  koszt: {alpha}, zadowolenie: {beta}")
    print(f"  Calkowity koszt: {koszt}, zadowolenie klienta: {zadowolenie}\n")

