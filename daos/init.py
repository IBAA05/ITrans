from Dao import Dao 
from ConfigDao import ConfigDao
from StationDao import StationDao
from InterstationDao import InterstationDao
from LogDao import LogDao
from RideDao import RideDao
from controllers.control import get_interstations , get_stations 
from entities.fliterApi import filter_station_json , filter_inter_station_json 

def initialize() :

    dao  = Dao()
    dao.createSchema()
    dao.close()
    
    config = [
        { 'key': 'msServerPort', 'value': '8080' },
        { 'key': 'msServerIp', 'value': '41.111.178.14' },
        { 'key': 'msServerProtocol', 'value': 'http' },
        { 'key': 'busNumber', 'value': '1234' } ,
        { 'key': 'wsServerPort', 'value': '9999' },
        {'key' : "stationBorder" , 'value' :  '100'} ,
        {'key': "interstationBorder", 'value': '50'},
]
 

    cf = ConfigDao()
    for c in config  :
        cf.insert_data(c['key'],c['value'])
    cf.close()
    
    station_going , station_returning = filter_station_json(get_stations ()) 
    interstation_going , interstation_returning = filter_inter_station_json(get_interstations ())
    
    station_dao = StationDao () 
    interstation_dao = InterstationDao() 
    
    for (station,interstation) in zip(station_going,interstation_going) : 
        
        interstation_dao.insert_data("interstation_going",interstation.lat, interstation.lng, interstation.from_station, interstation.to_station ) 
        station_dao.insert_data("station_going",station.id,station.name_ar,station.name_en,station.name_fr,station.lat, station.lng, station.order)


    for (station,interstation) in zip(station_returning,interstation_returning) : 
        
        interstation_dao.insert_data("interstation_returning",interstation.lat, interstation.lng, interstation.from_station, interstation.to_station ) 
        station_dao.insert_data("station_returning",station.id,station.name_ar,station.name_en,station.name_fr,station.lat, station.lng, station.order)

    # r = RideDao ()
    # r.insert_data(2,"going",1222,None)
    # r.insert(2,"going",1222,None)
    #r.finished_the_ride()
    # r.insert(2,"going",1222,None)
    # r.get_current_direction()
    # StationDao().insert_data()
    # InterstationDao().insert_data()
    
