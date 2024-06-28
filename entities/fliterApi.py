from entities import Station , InterStation 

def filter_station_json(json_stations):
    
    line_stations = json_stations['lineStations']

    going_stations = []
    return_stations = []

    for station in line_stations:
        go_geopoint = station['station']['goingGeopoint']
        ret_geopoint = station['station']['returningGeopoint']

        if station['direction'] == 'GOING':
            going_data = Station(
                station['station']['id'],
                station['station']['nameAR'],
                station['station']['nameEN'],
                station['station']['nameFR'],
                go_geopoint['lng'],
                go_geopoint['lat'],
                station['order']
            )
            going_stations.append(going_data)
        else:
            returning_data = Station(
                station['station']['id'],
                station['station']['nameAR'],
                station['station']['nameEN'],
                station['station']['nameFR'],
                ret_geopoint['lng'],
                ret_geopoint['lat'],
                station['order']
            )
            return_stations.append(returning_data)

    return going_stations, return_stations

def filter_inter_station_json(json_inter_stations):
    
    going_interstations = []
    return_interstations = []

    for interstation in json_inter_stations:
        if interstation['fromStation'] < interstation['toStation']:
            going_interstations.append(InterStation(
                interstation['lat'],
                interstation['long'],
                interstation['fromStation'],
                interstation['toStation'],
                interstation['order']
            ))
        else:
            return_interstations.append(InterStation(
                interstation['lat'],
                interstation['long'],
                interstation['fromStation'],
                interstation['toStation'],
                interstation['order']
            ))

    return going_interstations, return_interstations