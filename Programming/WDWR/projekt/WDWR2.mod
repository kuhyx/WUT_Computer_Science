###########################################################
# WDWR 18042                                              #
# Planowanie produkcj w warunkach ryzyka.                 #
# MODEL                                                   #
# Autor: Krzysztof Rudnicki                                        #
###########################################################

##########
# Zbiory #
##########
# Produkty
set PRODUCTS = {"P1", "P2", "P3", "P4"};
# Narzedzia
set TOOLS;
# Miesiace
set MONTHS ordered;
# Scenariusze
param scenarioCount;
set SCENARIOS = {1..scenarioCount};

#############
# Parametry #
#############

# Liczba kazdego z narzedzi
param toolCount {TOOLS} >= 1;

# Dochody ze sprzedazy [pln/szt]
param expectedProfitPerUnit {PRODUCTS} >= 0;

# Scenarios
param scenarioProfitPerUnit {SCENARIOS, PRODUCTS};
	
# Czasy produkcji [godz]
param toolTimePerUnit {TOOLS, PRODUCTS} >= 0;

# Ograniczenia rynkowe liczby sprzedawanych produktow [szt]
param salesMarketLimit {MONTHS, PRODUCTS} >= 0;
			
# Ograniczeine liczby magazynowanych produktow [szt]
param storageLimit {PRODUCTS} >= 0;

# Koszt magazynowania produktow [pln/szt per msc]
param storageUnitCost >= 0;

# Aktualny stan magazynowy [szt]
param startingStorage {PRODUCTS} >= 0;
	
# Pozadany stan magazynowy na koniec symulacji [szt]
param desiredEndStorage {PRODUCTS} >= 0;

# Liczba dni roboczych w miesiacu [d]
param daysPerMonth >= 1;

# Liczba zmian w ciagu jednego dnia roboczego
param shiftsPerDay >= 1;

# Dlugosc zmiany [godz]
param hoursPerShift >= 1;

# Liczba roboczogodzin w miesi�cu [godz]
param workHoursPerMonth = daysPerMonth*shiftsPerDay*hoursPerShift;

# Czas pracy narzedzi w danym miesi�cu
param availableToolTime {t in TOOLS} = toolCount[t]*workHoursPerMonth;

###########
# Zmienne #
###########
# Produkcja produktow
var produced {MONTHS, PRODUCTS} >= 0 integer;

# Sprzedaz produktow w danym miesiacu
var sold {MONTHS,PRODUCTS} >= 0 integer;
var totalSold {p in PRODUCTS} = sum {m in MONTHS} sold[m, p];

# Sprzedaz z podziałem na normalną (do 80% limitu rynku) i z obniżonym zyskiem (powyżej 80% limitu)
var salesNormal {m in MONTHS, p in PRODUCTS} >= 0 integer;
var salesDiscounted {m in MONTHS, p in PRODUCTS} >= 0 integer;

# Iloosc produktow przekazanych do magazynu w danym miesiacu
var stored {m in MONTHS, p in PRODUCTS} = produced[m, p] - sold[m, p]; 

# Stan magazynowy na koniec danego miesiaca
var storage {m in MONTHS, p in PRODUCTS} =
	startingStorage[p] + sum {m2 in MONTHS: ord(m2) <= ord(m)} stored[m2, p];  

# Wykorzystany czas pracy
var usedToolTime {m in MONTHS, t in TOOLS} =
	sum {p in PRODUCTS} produced[m,p]*toolTimePerUnit[t,p];

# Koszt magazynowania
var monthlyStorageCost {m in MONTHS} =
	(sum {p in PRODUCTS} storage[m, p])*storageUnitCost;
var totalStorageCost = sum {m in MONTHS} monthlyStorageCost[m];

# Zysk dla warto�ci oczekiwanej 
var expectedSalesProfit	 =
	sum {m in MONTHS, p in PRODUCTS} (
		salesNormal[m, p] * expectedProfitPerUnit[p] +
		salesDiscounted[m, p] * 0.8 * expectedProfitPerUnit[p]
	);
var expectedNetProfit =
	expectedSalesProfit - totalStorageCost;

# Zysk w danym scenariuszu
var scenarioSalesProfit {s in SCENARIOS} =
	sum {m in MONTHS, p in PRODUCTS} (
		salesNormal[m, p] * scenarioProfitPerUnit[s, p] +
		salesDiscounted[m, p] * 0.8 * scenarioProfitPerUnit[s, p]
	);
var scenarioNetProfit {s in SCENARIOS} = 
	scenarioSalesProfit[s] - totalStorageCost;

# Odchylenie jako miara ryzyka - zlinearyzowana wartosc bezwzgledna
var deviation {s in SCENARIOS} =
	expectedNetProfit - scenarioNetProfit[s];
var P {SCENARIOS} >= 0;
var Q {SCENARIOS} >= 0;
subject to deviationLimit {s1 in SCENARIOS, s2 in SCENARIOS}:
	deviation[s1]-deviation[s2]+P[s1]-Q[s2] = 0;
	
#var maxDeviation = max {s in SCENARIOS} deviation[s];
var maxDeviation;
# Linearyzacja maksymalnego odchylenia jako miary ryzyka
param M = 10000;
var Z {SCENARIOS} binary;
subject to mdLimit {s in SCENARIOS}:
	maxDeviation >= deviation[s];
subject to mdWhere {s in SCENARIOS}:
	maxDeviation <= deviation[s] + M*(1-Z[s]);
subject to mdOS:
	sum{s in SCENARIOS} Z[s] = 1;

# Aliasy dla ocenianych warto�ci
var profit = expectedNetProfit;
var risk = maxDeviation;

#######################
# Ograniczenia modelu #
#######################

# Podział sprzedaży na normalną i z obniżonym zyskiem
subject to TotalSales {m in MONTHS, p in PRODUCTS}:
	sold[m, p] = salesNormal[m, p] + salesDiscounted[m, p];

# Ograniczenie normalnej sprzedaży do 80% limitu rynkowego
subject to NormalSalesLimit {m in MONTHS, p in PRODUCTS}:
	salesNormal[m, p] <= 0.8 * salesMarketLimit[m, p];

# Ograniczenie rynkowe sprzedazy produktow
subject to SalesMarketLimit {m in MONTHS, p in PRODUCTS}:
	sold[m, p] <= salesMarketLimit[m, p];
# Ograniczenie magazynowe sprzedazy produktow
subject to SalesLimit1 {p in PRODUCTS}:
	sold[first(MONTHS), p] <= produced[first(MONTHS), p];
subject to SalesLimit2 {m in MONTHS, p in PRODUCTS: m != first(MONTHS)}:
	sold[m, p] <= produced [m, p] + storage[m, p];
# Ograniczenie pojemno�ci magazynowej
subject to StorageLimit {m in MONTHS, p in PRODUCTS}:
	storage[m, p] <= storageLimit[p];
# Ograniczenie na po��dany stan magazynowy na koniec marca
subject to DesiredStorage {p in PRODUCTS}:
	storage[last(MONTHS), p] >= desiredEndStorage[p];
#Ograniczenie czasu pracy narzedzi w miesiacu
subject to ToolWorkTime {m in MONTHS, t in TOOLS}:
	usedToolTime[m, t] <= availableToolTime[t];

#############################
# Metoda punktu odniesienia #
#############################
# Skladniki wektora oceny
set RATED = {"PROFIT", "RISK"};
# Wektor oceny
var value {r in RATED} = 
	if r == "PROFIT" then profit
 	else if r == "RISK" then risk;
# Wektor aspiracji
param aspiration {RATED};
# Warto�ci utopii i nadiru
param utopia {RATED};
param nadir {RATED};
# Wspolczynniki normalizujace
param lambda {r in RATED} =
	1 / (utopia[r]-nadir[r]);
# Wspolczynnik skladnika regularyzacyjnego
param epsilon;
# Wspolczynnik pomniejszenia warto�ci ocen ponad poziomem aspiracji
param beta;
# Indywidualne funkcje osiagniec
var individualRating {RATED};
# Zmienna pomocnicza metody punktu odniesienia
var v;
# Skalaryzujaca funkcja osiagniecia
var rating = v + epsilon * (sum {r in RATED} individualRating[r]);
# Odleglo�c od punktu odniesienia
var distance {r in RATED} = value[r]-aspiration[r];
# Znormalizowana odleglo�c od punktu odniesienia
var normalizedDistance {r in RATED} = lambda[r]*distance[r];
# Ograniczenia zmiennej v przez indywidualne funkcje osiagniec
subject to VSubject {r in RATED}:
	v <= individualRating[r]; 
# Ograniczenia indywidualnych funkcji osiagniec
subject to IndividualRatingSubjectBeta {r in RATED}:
	individualRating[r] <= beta*normalizedDistance[r];
subject to IndividualRatingSubject {r in RATED}:
	individualRating[r] <= normalizedDistance[r];

################
# Funkcje celu #
################
minimize MinimizeProfit: profit;
maximize MaximizeProfit: profit;
minimize MinimizeRisk: risk;
maximize MaximizeRisk: risk;
maximize RPM: rating;