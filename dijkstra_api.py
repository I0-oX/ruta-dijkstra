import json
import sys

class Grafo:
    INF = float('inf')
    
    def __init__(self, primero=None):
        self._grafo = {}
        self._primero = primero
        if primero:
            self._grafo[primero] = {}

    def agregar_nodo(self, nombre):
        self._grafo.setdefault(nombre, {})

    def agregar_aristas(self, *args):
        if len(args) == 3:
            o, d, p = args
            self._grafo.setdefault(o, {})[d] = p
            self._grafo.setdefault(d, {})[o] = p
        elif len(args) == 1:
            for o, d, p in args[0]:
                self.agregar_aristas(o, d, p)

    def dijkstra(self, origen=None):
        if origen is None:
            origen = self._primero
        nodos = list(self._grafo)
        n = len(nodos)
        if n == 0:
            return [], [], {}, {}, [], origen
            
        idx = {nom: i + 1 for i, nom in enumerate(nodos)}
        nombre = {i + 1: nom for i, nom in enumerate(nodos)}

        A = [[self.INF] * (n + 1) for _ in range(n + 1)]
        for i in range(1, n + 1):
            A[i][i] = 0
        for nom in nodos:
            for vecino, p in self._grafo[nom].items():
                A[idx[nom]][idx[vecino]] = p

        C = [1] * (n + 1)
        S = [self.INF] * (n + 1)
        P = [-1] * (n + 1)
        o = idx[origen]

        for j in range(1, n + 1):
            S[j] = A[o][j]
            if j != o and A[o][j] != self.INF:
                P[j] = o
        C[o] = 0

        t = []

        for _ in range(1, n):
            minimo = self.INF
            x = -1
            for v in range(1, n + 1):
                if C[v] and S[v] < minimo:
                    minimo = S[v]
                    x = v
            if x == -1:
                break
            C[x] = 0

            updates = []
            for j in range(1, n + 1):
                if C[j] and A[x][j] != self.INF and S[j] > S[x] + A[x][j]:
                    ant = S[j]
                    S[j] = S[x] + A[x][j]
                    P[j] = x
                    updates.append((j, ant, S[j]))
            t.append((x, updates))

        return S, P, nombre, idx, t, origen

    def _camino(self, P, destino, nombre):
        camino = []
        actual = destino
        while actual != -1:
            camino.append(nombre[actual])
            actual = P[actual]
        return " -> ".join(reversed(camino))

def run_dijkstra(data):
    g = Grafo()
    aristas = data.get("aristas", [])
    
    if not aristas:
        # Handle case where no edges are provided but maybe nodes are implied? 
        # For now, if no edges, we can't do much unless origin is enough for single node
        pass
        
    for item in aristas:
        if len(item) >= 3:
            origen, destino, peso = item[0], item[1], item[2]
            g.agregar_aristas(origen, destino, float(peso))
    
    origen = data.get("origen")
    if not origen and g._grafo:
        origen = list(g._grafo.keys())[0]
    
    if not origen:
        return {"error": "No origin provided"}
        
    S, P, nombre, idx, t, origen_calc = g.dijkstra(origen)
    
    traza = []
    for i, (x, updates) in enumerate(t, 1):
        step_updates = []
        for j, ant, nuevo in updates:
            step_updates.append({
                "nodo": nombre[j],
                "ant": None if ant == Grafo.INF else ant,
                "nuevo": nuevo,
                "via": nombre[x]
            })
        traza.append({
            "iteracion": i,
            "vertice": nombre[x],
            "distancia": S[x],
            "updates": step_updates
        })
        
    resultados = []
    for i in range(1, len(nombre) + 1):
        if S[i] != Grafo.INF:
            resultados.append({
                "destino": nombre[i],
                "distancia": S[i],
                "camino": g._camino(P, i, nombre)
            })
        
    return {
        "origen": origen_calc,
        "traza": traza,
        "resultados": resultados
    }

if __name__ == "__main__":
    try:
        raw = sys.stdin.read()
        data = json.loads(raw) if raw.strip() else {}
    except Exception:
        print(json.dumps({"error": "Invalid JSON"}))
        sys.exit(1)

    result = run_dijkstra(data)
    print(json.dumps(result))
