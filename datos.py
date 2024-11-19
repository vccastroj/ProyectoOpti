import numpy as np

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

γ = np.zeros(len(Z), dtype=int) # Inicializar γ con ceros
num_zonas_seguras = 7
γ_zq = np.zeros((len(Z), len(Q))) # Zona z en cuadrante q

for q in range(len(Q)):
    zonas_seguras = np.random.choice(len(Z), num_zonas_seguras, replace=False)
    for z in zonas_seguras:
        γ[z] = q
        γ_zq[z][q] = 1

# Asignar las zonas restantes de manera aleatoria
zonas_restantes = [z for z in range(len(Z)) if γ[z] == 0]
for z in zonas_restantes:
    q = np.random.randint(0, len(Q))
    γ[z] = q
    γ_zq[z][q] = 1


        
        

d_zp = np.random.uniform(20, 106, (len(Z), len(P))) # Distancia persona p a zona z


v_p = np.random.uniform(0.95, 1.25, len(P)) # Velocidad de persona p

C_z = np.round(100 / 0.93 * 4, 0) # 100 m2 por piso, 4 pisos, 1 persona usa 0.93 m2. Se supone que todas las vías de evacuación serán verticales. 
# f_qj =     1# Tiempo de viaje entre cuadrantes q y j
M = 1e6         # Constante grande
# h_z =     1 # Si zona z es vertical
Φ_q = np.random.randint(1, len(Q)) # 1 si cuadrante q fue afectado
# T_max =    1  # Tiempo máximo permitido
# K = 1 #personas minimas a evacuar

print(γ_zq[10])