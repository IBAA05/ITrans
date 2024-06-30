import requests
from daos.ConfigDao import ConfigDao 
from entities.fliterApi import *

def initialize_config():
    
    config_dao = ConfigDao()
    ms_server_port = config_dao.get_value_by_key('msServerPort')
    ms_server_ip = config_dao.get_value_by_key('msServerIp')
    ms_server_protocol = config_dao.get_value_by_key('msServerProtocol')

    url = f"{ms_server_protocol}://{ms_server_ip}:{ms_server_port}"
    return url
def get_stations():
    
    url = initialize_config()
    line_number = 2
    station_url = f"{url}/infra/line/{line_number}"

    try:
        response = requests.get(station_url)
        response.raise_for_status()  # Raise error for bad status codes
        data = response.json()
        return data         
    except requests.exceptions.RequestException as e:
            print('Error fetching data:', str(e))
        

def get_interstations():
    url = initialize_config()
    line_number = 2
    interstation_url = f"{url}/infra/interstation/line/{line_number}"

    try:
        response = requests.get(interstation_url)
        response.raise_for_status()  # Raise error for bad status codes
        data = response.json()
        return data         
    except requests.exceptions.RequestException as e:
        print('Error fetching data:', str(e))

def main():
    
    stations = get_stations()
    interstations = get_interstations()

   
    return stations , interstations 

if __name__ == "__main__":
    main()