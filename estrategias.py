def estrategia_impacto(zona):
    return zona.riesgo * zona.poblacion

def estrategia_costo(zona):
    return (zona.riesgo * zona.poblacion) / zona.costo

def estrategia_visibilidad(zona):
    return zona.poblacion

catalogo_estrategias = {
    "impacto": estrategia_impacto,
    "eficiencia": estrategia_costo,
    "visibilidad": estrategia_visibilidad,
}