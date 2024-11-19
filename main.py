#importar bibliotecas
from gurobipy import GRB, Model, quicksum
import numpy as np
import random

model = Model()

# Conjuntos
P = np.arange(1, 42001)
Z = np.arange(1, 32*7)
Q = np.arange(1,32)
T = np.arange(1,int(14/(7/9)))

# Parametros
B = np.random.randint(1, len(Q), len(P)) # A qué cuadrante pertenece cada persona, es aleatorio.
B_pq = np.zeros((len(P), len(Q))) # Persona p en cuadrante q
for i in range(len(P)):
    for j in range(len(Q)):
        if B[i] == Q[j]:
            B_pq[i][j] = 1

γ = np.random.randint(1, len(Q), len(Z)) # a que cuadramte pertenece cada zona, es aleatorio        
γ_zq = np.zeros((len(Z), len(Q))) # Zona z en cuadrante q
for i in range(len(Z)):
    for j in range(len(Q)):
        if γ[i] == Q[j]:
            γ_zq[i][j] = 1           
        
# d_zp = 1() # Distancia persona p a zona z
v_p = np.random.uniform(0.95, 1.25, len(P)) # Velocidad de persona p

C_z = np.round(100 / 0.93 * 4, 0) # 100 m2 por piso, 4 pisos, 1 persona usa 0.93 m2. Se supone que todas las vías de evacuación serán verticales. 
# f_qj =     1# Tiempo de viaje entre cuadrantes q y j
M = 1e6         # Constante grande
# h_z =     1 # Si zona z es vertical
Φ_q = np.random.randint(1, len(Q)) # 1 si cuadrante q fue afectado
# T_max =    1  # Tiempo máximo permitido
# K = 1 #personas minimas a evacuar

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
