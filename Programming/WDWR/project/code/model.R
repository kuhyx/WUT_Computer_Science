# Biblioteki
library(lpSolveAPI)
library(mvtnorm)
library(ggplot2)

# Parametry problemu
set.seed(307585)  # Numer zadania jako ziarno

# 1. Definicja danych wejściowych
# ----------------------------
# Liczba produktów i miesięcy
n_products <- 4
n_months <- 3

# Czas produkcji (h/szt)
prod_time <- matrix(c(
  0.4, 0.6, 0, 0,       # Szlifowanie
  0.2, 0.1, 0, 0.6,     # Wiercenie pionowe
  0.1, 0, 0.7, 0,       # Wiercenie poziome
  0.06, 0.04, 0, 0.05,  # Frezowanie
  0, 0.05, 0.02, 0      # Toczenie
), nrow = 5, byrow = TRUE)

# Liczba maszyn
n_machines <- c(4, 2, 3, 1, 1)

# Dostępny czas na maszynę na miesiąc (h)
time_per_machine <- 24 * 8 * 2  # 24 dni * 8h * 2 zmiany

# Ograniczenia rynkowe
market_limits <- matrix(c(
  200, 0, 100, 200,  # Styczeń
  300, 100, 200, 200,  # Luty
  0, 300, 100, 200   # Marzec
), nrow = 3, byrow = TRUE)

# Parametry rozkładu t-Studenta
mu <- c(9, 8, 7, 6)
Sigma <- matrix(c(
  16, -2, -1, -3,
  -2, 9, -4, -1,
  -1, -4, 4, 1,
  -3, -1, 1, 1
), nrow = 4, byrow = TRUE)
df <- 5  # Stopnie swobody

# 2. Generowanie scenariuszy dla dochodów
# ---------------------------------------
n_scenarios <- 1000
# Generowanie próbek z rozkładu t-Studenta
raw_samples <- rmvt(n_scenarios, sigma = Sigma, df = df, delta = mu)

# Ograniczenie wartości do przedziału [5, 12]
truncated_samples <- pmin(pmax(raw_samples, 5), 12)

# Obliczenie oczekiwanych dochodów
expected_revenues <- colMeans(truncated_samples)

# 3. Tworzenie modelu jednokryterialnego (maksymalizacja zysku)
# -----------------------------------------------------------

# Funkcja tworząca model optymalizacyjny z danym wektorem wag dla kryteriów
create_lp_model <- function(price_weights) {
  # Indeksy zmiennych
  idx_prod <- function(i, t) (t-1) * n_products + i
  idx_sales <- function(i, t) n_months * n_products + (t-1) * n_products + i
  idx_inv <- function(i, t) 2 * n_months * n_products + (t-1) * n_products + i
  idx_over <- function(i, t) 3 * n_months * n_products + (t-1) * n_products + i
  
  # Liczba zmiennych: produkcja, sprzedaż, zapasy, flagi przekroczenia 80%
  n_vars <- 4 * n_months * n_products
  
  # Utworzenie modelu
  lp_model <- make.lp(0, n_vars)
  
  # Ustawienie typów zmiennych (over_i_t są binarne)
  set.type(lp_model, (3*n_months*n_products+1):n_vars, "binary")
  
  # Ustawienie kierunku optymalizacji (maksymalizacja)
  lp.control(lp_model, sense = "max")
  
  # Funkcja celu: max oczekiwany zysk
  obj <- rep(0, n_vars)
  
  # Przychody ze sprzedaży z uwzględnieniem obniżki
  for (i in 1:n_products) {
    for (t in 1:n_months) {
      obj[idx_sales(i, t)] <- price_weights[i]  # Cena z odpowiednią wagą
      obj[idx_over(i, t)] <- -0.2 * price_weights[i] * market_limits[t, i]  # Kara za przekroczenie 80%
    }
  }
  
  # Koszty magazynowania
  for (i in 1:n_products) {
    for (t in 1:n_months) {
      obj[idx_inv(i, t)] <- -1  # 1 zł za sztukę za miesiąc
    }
  }
  
  set.objfn(lp_model, obj)
  
  # Dodanie ograniczeń
  
  # 1. Ograniczenia czasowe maszyn
  for (m in 1:5) {  # Dla każdego typu maszyny
    for (t in 1:n_months) {  # Dla każdego miesiąca
      row <- rep(0, n_vars)
      for (i in 1:n_products) {  # Dla każdego produktu
        if (prod_time[m, i] > 0) {
          row[idx_prod(i, t)] <- prod_time[m, i]
        }
      }
      add.constraint(lp_model, row, "<=", n_machines[m] * time_per_machine)
    }
  }
  
  # 2. Bilanse magazynowe
  for (i in 1:n_products) {
    for (t in 1:n_months) {
      row <- rep(0, n_vars)
      
      # Produkcja zwiększa zapas
      row[idx_prod(i, t)] <- 1
      
      # Sprzedaż zmniejsza zapas
      row[idx_sales(i, t)] <- -1
      
      # Zapas na koniec okresu
      row[idx_inv(i, t)] <- 1
      
      # Zapas z poprzedniego okresu
      if (t > 1) {
        row[idx_inv(i, t-1)] <- -1
      }
      
      # Dla t=1: inv_{i,0} = 0 (warunek początkowy)
      if (t == 1) {
        add.constraint(lp_model, row, "=", 0)
      } else {
        add.constraint(lp_model, row, "=", 0)
      }
    }
  }
  
  # 3. Ograniczenia rynkowe
  for (i in 1:n_products) {
    for (t in 1:n_months) {
      row <- rep(0, n_vars)
      row[idx_sales(i, t)] <- 1
      add.constraint(lp_model, row, "<=", market_limits[t, i])
    }
  }
  
  # 4. Ograniczenia pojemności magazynu
  for (i in 1:n_products) {
    for (t in 1:n_months) {
      row <- rep(0, n_vars)
      row[idx_inv(i, t)] <- 1
      add.constraint(lp_model, row, "<=", 200)
    }
  }
  
  # 5. Warunki końcowe (50 sztuk każdego produktu na koniec marca)
  for (i in 1:n_products) {
    row <- rep(0, n_vars)
    row[idx_inv(i, 3)] <- 1
    add.constraint(lp_model, row, "=", 50)
  }
  
  # 6. Ograniczenia dotyczące obniżki dochodu (flagi over_i_t)
  big_m <- 10000  # Duża liczba dla metody Big-M
  for (i in 1:n_products) {
    for (t in 1:n_months) {
      if (market_limits[t, i] > 0) {  # Tylko dla produktów, które można sprzedać
        # Ograniczenie: s_{i,t} >= 0.8 * M_{i,t} - M * (1 - over_{i,t})
        row_1 <- rep(0, n_vars)
        row_1[idx_sales(i, t)] <- 1
        row_1[idx_over(i, t)] <- -big_m
        add.constraint(lp_model, row_1, ">=", 0.8 * market_limits[t, i] - big_m)
        
        # Ograniczenie: s_{i,t} <= 0.8 * M_{i,t} + M * over_{i,t}
        row_2 <- rep(0, n_vars)
        row_2[idx_sales(i, t)] <- 1
        row_2[idx_over(i, t)] <- -big_m
        add.constraint(lp_model, row_2, "<=", 0.8 * market_limits[t, i])
      } else {
        # Dla produktów, których nie można sprzedać, ustalamy over_{i,t} = 0
        row <- rep(0, n_vars)
        row[idx_over(i, t)] <- 1
        add.constraint(lp_model, row, "=", 0)
      }
    }
  }
  
  return(lp_model)
}

# Rozwiązanie modelu jednokryterialnego
print("Solving single-criterion model...")
lp_model_single <- create_lp_model(expected_revenues)
status <- solve(lp_model_single)
if(status != 0) {
  stop("Error solving model: ", status)
}

# Pobranie wyników
obj_value <- get.objective(lp_model_single)
solution <- get.variables(lp_model_single)

# Podział rozwiązania na produkcję, sprzedaż i zapasy
n_vars_per_group <- n_months * n_products
production <- matrix(solution[1:n_vars_per_group], nrow=n_months, byrow=TRUE)
sales <- matrix(solution[(n_vars_per_group+1):(2*n_vars_per_group)], nrow=n_months, byrow=TRUE)
inventory <- matrix(solution[(2*n_vars_per_group+1):(3*n_vars_per_group)], nrow=n_months, byrow=TRUE)
over_flags <- matrix(solution[(3*n_vars_per_group+1):(4*n_vars_per_group)], nrow=n_months, byrow=TRUE)

# 4. Model dwukryterialny (zysk-ryzyko)
# ------------------------------------

# Funkcja obliczająca średnią różnicę Giniego dla danego rozwiązania
calculate_gini_mean_difference <- function(solution, scenarios) {
  n_scenarios <- nrow(scenarios)
  n_vars_per_group <- n_months * n_products
  
  # Wyodrębnienie zmiennych decyzyjnych
  sales <- matrix(solution[(n_vars_per_group+1):(2*n_vars_per_group)], nrow=n_months, byrow=TRUE)
  inventory <- matrix(solution[(2*n_vars_per_group+1):(3*n_vars_per_group)], nrow=n_months, byrow=TRUE)
  over_flags <- matrix(solution[(3*n_vars_per_group+1):(4*n_vars_per_group)], nrow=n_months, byrow=TRUE)
  
  # Obliczenie zysku dla każdego scenariusza
  profits <- numeric(n_scenarios)
  
  for (s in 1:n_scenarios) {
    profit <- 0
    
    # Przychód ze sprzedaży
    for (t in 1:n_months) {
      for (i in 1:n_products) {
        # Uwzględnienie obniżki ceny o 20% gdy sprzedaż > 80% limitu rynkowego
        price_reduction <- ifelse(over_flags[t, i] > 0.5, 0.2, 0)
        profit <- profit + scenarios[s, i] * sales[t, i] * (1 - price_reduction)
      }
    }
    
    # Koszty magazynowania
    for (t in 1:n_months) {
      for (i in 1:n_products) {
        profit <- profit - inventory[t, i]
      }
    }
    
    profits[s] <- profit
  }
  
  # Obliczenie średniej różnicy Giniego
  gini <- 0
  for (i in 1:n_scenarios) {
    for (j in 1:n_scenarios) {
      gini <- gini + abs(profits[i] - profits[j]) * (1/n_scenarios) * (1/n_scenarios)
    }
  }
  gini <- gini / 2
  
  return(list(gini = gini, expected_profit = mean(profits)))
}

# Generowanie punktów na krzywej efektywnej metodą ważonych kryteriów
generate_efficient_frontier <- function(scenarios, n_points = 20) {
  lambda_values <- seq(0, 1, length.out = n_points)
  results <- data.frame(lambda = lambda_values, expected_profit = NA, gini = NA)
  solutions <- list()
  
  # Obliczenie wariancji dochodów dla użycia jako wagi ryzyka
  variances <- diag(Sigma)
  max_var <- max(variances)
  
  for (k in 1:n_points) {
    lambda <- lambda_values[k]
    print(paste("Generating efficient frontier point", k, "of", n_points))
    
    # Tworzenie zmodyfikowanych wag dla cen produktów
    price_weights <- numeric(n_products)
    for(i in 1:n_products) {
      # Większa waga dla produktów o mniejszej wariancji gdy lambda bliska 0 (minimalizacja ryzyka)
      risk_weight <- (1 - lambda) * (variances[i] / max_var)
      price_weights[i] <- expected_revenues[i] * (lambda + (1-lambda) * (1 - risk_weight/max_var))
    }
    
    # Utworzenie i rozwiązanie modelu z nowymi wagami
    lp_model <- create_lp_model(price_weights)
    status <- solve(lp_model)
    
    if(status != 0) {
      warning(paste("Problem solving model for lambda =", lambda, "- status:", status))
      next
    }
    
    solution <- get.variables(lp_model)
    solutions[[k]] <- solution
    
    # Obliczenie metryki Giniego dla uzyskanego rozwiązania
    metrics <- calculate_gini_mean_difference(solution, scenarios)
    
    results$expected_profit[k] <- metrics$expected_profit
    results$gini[k] <- metrics$gini
  }
  
  return(list(results = results, solutions = solutions))
}

# Generowanie krzywej efektywnej
n_points <- 20
print("Generating efficient frontier...")
efficient_frontier <- generate_efficient_frontier(truncated_samples, n_points)

# Znalezienie rozwiązań o minimalnym ryzyku i maksymalnym zysku
min_risk_solution_idx <- which.min(efficient_frontier$results$gini)
max_profit_solution_idx <- which.max(efficient_frontier$results$expected_profit)

min_risk_solution <- efficient_frontier$solutions[[min_risk_solution_idx]]
max_profit_solution <- efficient_frontier$solutions[[max_profit_solution_idx]]

# Wartości w przestrzeni ryzyko-zysk
min_risk_metrics <- calculate_gini_mean_difference(min_risk_solution, truncated_samples)
max_profit_metrics <- calculate_gini_mean_difference(max_profit_solution, truncated_samples)

# 5. Analiza dominacji stochastycznej
# ---------------------------------

# Wybieramy 3 rozwiązania efektywne do analizy
solution_indices <- c(min_risk_solution_idx, 
                      round(n_points/2), 
                      max_profit_solution_idx)

selected_solutions <- efficient_frontier$solutions[solution_indices]

# Funkcja obliczająca empiryczne dystrybuanty zysków dla danych rozwiązań
calculate_profit_distributions <- function(solutions, scenarios) {
  n_solutions <- length(solutions)
  n_scenarios <- nrow(scenarios)
  
  profit_distributions <- list()
  
  for (s in 1:n_solutions) {
    solution <- solutions[[s]]
    n_vars_per_group <- n_months * n_products
    
    # Wyodrębnienie zmiennych decyzyjnych
    sales <- matrix(solution[(n_vars_per_group+1):(2*n_vars_per_group)], nrow=n_months, byrow=TRUE)
    inventory <- matrix(solution[(2*n_vars_per_group+1):(3*n_vars_per_group)], nrow=n_months, byrow=TRUE)
    over_flags <- matrix(solution[(3*n_vars_per_group+1):(4*n_vars_per_group)], nrow=n_months, byrow=TRUE)
    
    # Obliczenie zysku dla każdego scenariusza
    profits <- numeric(n_scenarios)
    
    for (sc in 1:n_scenarios) {
      profit <- 0
      
      # Przychód ze sprzedaży
      for (t in 1:n_months) {
        for (i in 1:n_products) {
          # Uwzględnienie obniżki ceny o 20% gdy sprzedaż > 80% limitu rynkowego
          price_reduction <- ifelse(over_flags[t, i] > 0.5, 0.2, 0)
          profit <- profit + scenarios[sc, i] * sales[t, i] * (1 - price_reduction)
        }
      }
      
      # Koszty magazynowania
      for (t in 1:n_months) {
        for (i in 1:n_products) {
          profit <- profit - inventory[t, i]
        }
      }
      
      profits[sc] <- profit
    }
    
    profit_distributions[[s]] <- sort(profits)
  }
  
  return(profit_distributions)
}

# Obliczenie dystrybuant zysków
print("Calculating profit distributions...")
profit_distributions <- calculate_profit_distributions(selected_solutions, truncated_samples)

# Sprawdzenie dominacji stochastycznej pierwszego rzędu
check_first_order_dominance <- function(dist1, dist2) {
  # Łączenie i sortowanie unikalnych wartości z obu rozkładów
  all_values <- sort(unique(c(dist1, dist2)))
  
  # Obliczanie empirycznych dystrybuant
  ecdf1 <- ecdf(dist1)
  ecdf2 <- ecdf(dist2)
  
  # Sprawdzenie warunku dominacji stochastycznej
  dominance_12 <- all(ecdf1(all_values) <= ecdf2(all_values))
  dominance_21 <- all(ecdf2(all_values) <= ecdf1(all_values))
  
  if (dominance_12 && !dominance_21) {
    return("1 dominuje 2")
  } else if (!dominance_12 && dominance_21) {
    return("2 dominuje 1")
  } else if (dominance_12 && dominance_21) {
    return("Rozkłady są identyczne")
  } else {
    return("Brak dominacji")
  }
}

# Sprawdzenie dominacji stochastycznej między wybranymi rozwiązaniami
dominance_results <- matrix("", nrow=3, ncol=3)
for (i in 1:3) {
  for (j in 1:3) {
    if (i != j) {
      dominance_results[i, j] <- check_first_order_dominance(
        profit_distributions[[i]], profit_distributions[[j]])
    } else {
      dominance_results[i, j] <- "-"
    }
  }
}

# Wyświetlenie wyników
print("=== Wyniki jednokryterialnego modelu optymalizacji ===")
print(paste("Oczekiwany zysk:", obj_value))
print("Plan produkcji:")
print(round(production, 2))
print("Plan sprzedaży:")
print(round(sales, 2))
print("Stan magazynu:")
print(round(inventory, 2))

print("=== Wyniki modelu dwukryterialnego ===")
print("Krzywa efektywna:")
print(head(efficient_frontier$results))
print("...")

print("Rozwiązanie o minimalnym ryzyku:")
print(paste("Zysk:", round(min_risk_metrics$expected_profit, 2)))
print(paste("Ryzyko (Gini):", round(min_risk_metrics$gini, 2)))

print("Rozwiązanie o maksymalnym zysku:")
print(paste("Zysk:", round(max_profit_metrics$expected_profit, 2)))
print(paste("Ryzyko (Gini):", round(max_profit_metrics$gini, 2)))

print("=== Analiza dominacji stochastycznej ===")
print(dominance_results)

# Wizualizacja wyników
ggplot(efficient_frontier$results, aes(x=gini, y=expected_profit)) +
  geom_point() +
  geom_line() +
  geom_point(data=efficient_frontier$results[c(min_risk_solution_idx, max_profit_solution_idx),], 
             aes(x=gini, y=expected_profit), color="red", size=4) +
  labs(title="Krzywa efektywna w przestrzeni ryzyko-zysk",
       x="Ryzyko (średnia różnica Giniego)",
       y="Oczekiwany zysk") +
  theme_minimal()

# Zapisanie wykresu
ggsave("efficient_frontier.png", width=8, height=6, dpi=300)

print("Obliczenia zakończone.")