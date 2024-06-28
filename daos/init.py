from Dao import Dao 
from ConfigDao import ConfigDao
from StationDao import StationDao
from InterstationDao import InterstationDao
from LogDao import LogDao

def main() :
    config = [
    
            { key: 'msServerPort', value: '8080' },
            { key: 'msServerIp', value: '41.111.178.14' },
            { key: 'msServerProtocol', value: 'http' },
            { key: 'busNumber', value: '1234' } ,
            { key: 'wsServerPort', value: '9999' }, 
]  
        
    
    Dao().createSchema()
    ConfigDao().insert_data("wsServerPort","9999")
    # StationDao().insert_data()
    # InterstationDao().insert_data()
    
main()  