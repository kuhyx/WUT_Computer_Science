import pulp
import matplotlib.pyplot as plt
import sys

# Create a problem variable:
model = pulp.LpProblem("Optimal_Distribution", pulp.LpMinimize)
# Define providers (Factories and Warehouses)
factories = ['F1', 'F2']
warehouses = ['M1', 'M2', 'M3', 'M4']
providers = factories + warehouses  # Combining both lists

# Define customers
customers = ['K1', 'K2', 'K3', 'K4', 'K5', 'K6']

cost = {
    'F1': {'M1': 0.3, 'M2': 0.5, 'M3': 1.2, 'M4': 0.8, 'K1': 1.2, 'K2': 999, 'K3': 1.2, 'K4': 2.0, 'K5': 999, 'K6': 1.1},
    'F2': {'M1': 999, 'M2': 0.4, 'M3': 0.5, 'M4': 0.3, 'K1': 1.8, 'K2': 999, 'K3': 999, 'K4': 999, 'K5': 999, 'K6': 999},
    'M1': {'K1': 999, 'K2': 1.2, 'K3': 0.2, 'K4': 1.7, 'K5': 999, 'K6': 2.0},
    'M2': {'K1': 1.4, 'K2': 0.3, 'K3': 1.8, 'K4': 1.3, 'K5': 0.5, 'K6': 999},
    'M3': {'K1': 999, 'K2': 1.3, 'K3': 2.0, 'K4': 999, 'K5': 0.3, 'K6': 1.4},
    'M4': {'K1': 999, 'K2': 999, 'K3': 0.4, 'K4': 2.0, 'K5': 0.5, 'K6': 1.6}
}


# Decision variables
x = pulp.LpVariable.dicts("x", [(i, j) for i in providers for j in customers], lowBound=0, cat='Integer')
y = pulp.LpVariable.dicts("y", [(i, k) for i in factories for k in warehouses], lowBound=0, cat='Integer')
# Objective function components
cost_distribution = pulp.lpSum([cost[i][j] * x[(i, j)] for i in providers for j in customers])
cost_warehouse = pulp.lpSum([cost[i][k] * y[(i, k)] for i in factories for k in warehouses])

alpha = 0.5
beta = 0.5
# Binary variables for meeting preferences
P = pulp.LpVariable.dicts("P", [(i, j) for i in providers for j in customers], cat='Binary')
max_order = 60
satisfaction_scores = {'K1': 50 / max_order, 'K2': 10 / max_order, 'K3': 40 / max_order, 'K4': 35 / max_order, 'K5': 60 / max_order, 'K6': 20 / max_order}
customer_preferences = {'K1': ['F2'], 'K2': ['M1'], 'K3': ['M2', 'M3'], 'K4': ['F1'], 'K5': [], 'K6': ['M3', 'M4']}
# Satisfaction component
satisfaction_component = pulp.lpSum([satisfaction_scores[j] * P[(i, j)] for i in providers for j in customers])

# Define objective
model += alpha * (cost_distribution + cost_warehouse) - beta * satisfaction_component
# Factory production capacity constraints
factory_capacity = {'F1': 150, 'F2': 200}
warehouse_capacity = {'M1': 70, 'M2': 50 , 'M3': 100, 'M4': 40 }
customer_demand = {'K1': 50, 'K2': 10, 'K3': 40, 'K4': 35, 'K5': 60, 'K6': 20}
for i in factories:
    model += pulp.lpSum([x[(i, j)] for j in customers] + [y[(i, k)] for k in warehouses]) <= factory_capacity[i]

# Warehouse handling capacity constraints
for k in warehouses:
    model += pulp.lpSum([x[(k, j)] for j in customers]) <= warehouse_capacity[k]

# Customer demand fulfillment constraints
for j in customers:
    model += pulp.lpSum([x[(i, j)] for i in providers]) == customer_demand[j]

# Other constraints like preferences can be added similarly
# Solve the problem
# Output results
for v in model.variables():
    print(v.name, "=", v.varValue)

# Assuming definitions of the model as previously discussed
cost_results = []
satisfaction_results = []

# Varying alpha and beta
for alpha in range(10):
    beta = 10 - alpha + sys.float_info.epsilon
    alpha /= 10.0
    beta /= 10.0

    # Update objective function
    model.objective = alpha * cost_distribution - beta * satisfaction_component

    # Solve the model
    model.solve()
    print(alpha)

    # Record the results

    # Record the results
    total_cost = pulp.value(cost_distribution)
    total_satisfaction = pulp.value(satisfaction_component)
    cost_results.append(total_cost)
    satisfaction_results.append(total_satisfaction)

print(cost_results, satisfaction_results)
# Plotting the results
plt.plot(cost_results, satisfaction_results, marker='o')
plt.xlabel('Total Cost')
plt.ylabel('Customer Satisfaction')
plt.title('Trade-off between Cost and Customer Satisfaction')
plt.show()