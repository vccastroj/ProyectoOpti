#importar bibliotecas
from gurobipy import GRB, Model, quicksum
from datos import cargar_parametros
model = Model()

# Cargar parámetros
P, Z, Q, T, B, B_pq, γ, γ_zq, d_zp, v_p, C_z, f_qj, M, Φ_q, K, h_z, T_max = cargar_parametros()

# Variables
alpha = model.addVars(P, Z, T, vtype = GRB.BINARY, name = "alpha") #Indica si la persona p comienza a evacuar hacia la zona segura z en el instante de tiempo t.

X = model.addVars(Z, T, vtype = GRB.CONTINUOUS, name = "X") #Cantidad de personas en la zona segura z en el tiempo t.

w = model.addVars(P, Q, T, vtype = GRB.BINARY, name = "w") #Indica si la persona p se encuentra  en un cuadrante q en el tiempo t.

theta = model.addVars(P, Q, Q, T, vtype = GRB. BINARY, name = "theta") #Indica si la persona p decide viajar a un cuadrante j desde un cuadrante q en el tiempo t.

# FO
objetivo = quicksum(X[z, T] for z in Z)

model.setObjective (objetivo, GRB.MAXIMIZE)

# Restricciones
model.addConstrs((quicksum(alpha[p, z, t] for z in Z for t in T) <= 1 for p in P), name="r_2") #Restricción de evacuación única

#Restricción valor de alpha.

#Restricción a cambio de cuadrante.

model.addConstrs((w[p, q, 1] == B[p, q] - quicksum(theta[p, q, j, 1] for j in Q if j != q) for p in P for q in Q), name="r_5") #Condición inicial de cuadrante.

model.addConstrs((quicksum(w[p, q, t] for q in Q) == 1 for p in P for t in T), name="r_6") #Restricción de cuadrante único.

#Posicionamiento de cuadrante.

#Flujo de cuadrantes.

model.addConstr(quicksum(X[z, T[-1]] for z in Z) >= K, name="r_9") #Cantidad mínima a evacuar

#Restricción de zonas afectadas por tsunami

#Restricción de activación de theta.

#Restricción de inventario de personas de la zona segura.

model.addConstrs((X[z, 1] == quicksum(alpha[p, z, 1] for p in P) for z in Z), name="restriccion_13") #Condición inicial de inventario de las zonas.

model.addConstrs((X[z, t] <= c[z] for z in Z for t in T), name="restriccion_14") #Capacidad de zonas seguras.
