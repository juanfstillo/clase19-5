def traslado_aeropuerto(medio):
    if medio == "auto":
        return "Tomá un taxi o un remis, es lo más directo."
    elif medio == "bus":
        return "Podés tomar el bus 45, te deja cerca del aeropuerto."
    elif medio == "tren":
        return "El tren Roca te lleva directo al aeropuerto, es económico."
    elif medio == "bicicleta":
        return "¡Genial! Podés usar la ciclovía hasta el aeropuerto, es ecológico."
    elif medio == "a pie":
        return "¡Wow! El aeropuerto está bastante lejos, mejor considerá otro medio."