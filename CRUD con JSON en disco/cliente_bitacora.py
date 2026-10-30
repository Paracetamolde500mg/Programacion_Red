import requestse

BASE = "http://localhost:8001"

print("1. Creando incidencias (POST)...")
# Crear: Los datos van en el cuerpo (json=)
r1 = requests.post(f"{BASE}/incidencias", json={"tipo": "alerta", "descripcion": "Intento de acceso SSH"}, timeout=10)
print("POST 1:", r1.status_code, r1.json()) # 201

r2 = requests.post(f"{BASE}/incidencias", json={"tipo": "vulnerabilidad", "descripcion": "Puerto expuesto"}, timeout=10)
creada2 = r2.json()

print("\n2. Consultando filtros combinados (GET)...")
# Consultar: el filtro va en la URL (params=)
r_filtro = requests.get(f"{BASE}/incidencias", params={"tipo": "alerta", "estado": "abierta"}, timeout=10)
print("GET con filtros:", r_filtro.json())

print("\n3. Validando vocabulario controlado (PATCH)...")
# Modificar: id en la ruta, cambios en el cuerpo
r_patch_error = requests.patch(f"{BASE}/incidencias/{creada2['id']}", json={"estado": "archivada"}, timeout=10)
print("PATCH Error Esperado (400):", r_patch_error.status_code, r_patch_error.json())

print("\n4. Probando PUT (Reemplazo completo)...")
r_put = requests.put(f"{BASE}/incidencias/{creada2['id']}", json={"tipo": "incidente", "descripcion": "Puerto comprometido"}, timeout=10)
print("PUT:", r_put.status_code, r_put.json()) # 200

print("\n5. Auditoría del servidor...")
# La auditoría del servidor, desde fuera
print("Contadores:", requests.get(f"{BASE}/contadores", timeout=10).json())
