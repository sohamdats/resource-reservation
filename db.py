import redis
 

class DB:
    def __init__(self,host='localhost',port=6379):
        self.r = redis.Redis(host=host,port=port)
        
    def store_devices(self,devicelist):
        for device in devicelist:
            self.r.rpush('devices',device)

    def decode(self,device):
        return device.decode('utf-8') if device else None
    
    def get_devices(self,devicelist):
        l = []
        for device in self.r.lrange('devices',0,-1):
            d = self.decode(device)
            if d == None :break
            l.append(d)
    
    def get_device_states(self):
        devices_dict = {}
        for device in self.r.lrange('devices',0,-1):
            device = self.decode(device)
            devices_dict[device]={}
            devices_dict[device]['user'] = self.decode(self.r.hget(device,'user'))
            devices_dict[device]['minutes'] = self.decode(self.r.hget(device,'minutes'))
            devices_dict[device]['time'] = self.decode(self.r.hget(device,'time'))

        return devices_dict

    def is_reserved(self,device):
        return False if self.r.hget(device,'user')==None else True 

    def store(self,device,user,minutes,time):
        self.r.hmset(device,{'user':user,'minutes':minutes,'time':time})

    

            
        
