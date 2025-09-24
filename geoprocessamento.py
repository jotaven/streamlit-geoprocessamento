from geopy.distance import geodesic

def calcular_distancia(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calcula a distância em quilômetros entre dois pontos geográficos.

    Args:
        lat1 (float): Latitude do ponto 1
        lon1 (float): Longitude do ponto 1
        lat2 (float): Latitude do ponto 2
        lon2 (float): Longitude do ponto 2

    Returns:
        float: Distância em quilômetros
    """
    try:
        return geodesic((lat1, lon1), (lat2, lon2)).kilometers
    except Exception as e:
        print(f"Erro ao calcular distância: {e}")
        return None


def locais_proximos(lat: float, lon: float, raio_km: float, locais: list) -> list:
    """
    Retorna os locais que estão dentro de um raio de distância de uma coordenada de referência.

    Args:
        lat (float): Latitude de referência
        lon (float): Longitude de referência
        raio_km (float): Raio em quilômetros
        locais (list): Lista de documentos vindos do MongoDB com campo 'coordenadas'

    Returns:
        list: Lista de locais próximos contendo distância calculada
    """
    proximos = []
    for local in locais:
        coord = local.get("coordenadas", {})
        lat2 = coord.get("latitude")
        lon2 = coord.get("longitude")

        if lat2 is not None and lon2 is not None:
            distancia = calcular_distancia(lat, lon, lat2, lon2)
            if distancia is not None and distancia <= raio_km:
                local["distancia_km"] = round(distancia, 2)
                proximos.append(local)

    return proximos
