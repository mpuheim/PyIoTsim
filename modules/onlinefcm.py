import fcmlib
from modules import requests

class FCMcontroller():

    # FCM controller class
    def __init__(self, modeldir, server):
        self.server=server
        self.request=requests.Communicator(workers=10)
        print("FCM controller initialization")
        with open(modeldir,"r",encoding="utf8") as f:
            #load model from file
            model=f.read()
            map=fcmlib.FCM(model)
            model=map.serialize(indent=0)
            name=map.name
            #register model on server
            print("- Registering "+name+" on server "+server)
            url=server+name+"/login/"
            f=self.request.post(url)
            f.result()
            #upload model
            url=server+name+"/run/"
            cmd=name+".deserialize('"+model+"')"
            f=self.request.post(url,data = {'command':cmd})
            f.result()
            #set model name
            self.map=name

    # Control method
    def control(self, distance, angle): #return [acceleration, turn]
        url = self.server+self.map+"/run/"
        # activations of input concepts
        cmd = self.map+'["Angle"] = '+self.map+'["Angle"].inputMF.evaluate('+str(angle)+')'
        self.request.post(url,data = {'command':cmd})
        cmd = self.map+'["Distance"] = '+self.map+'["Distance"].inputMF.evaluate('+str(distance)+')'
        self.request.post(url,data = {'command':cmd})
        # update activations of output concepts
        cmd = self.map+'.update()'
        f=self.request.post(url,data = {'command':cmd})
        f.result()
        # process outputs
        cmd = self.map+'["Acceleration"].outputMF.evaluate('+self.map+'["Acceleration"].value)'
        fa = self.request.post(url,data = {'command':cmd})
        cmd = self.map+'["Turn"].outputMF.evaluate('+self.map+'["Turn"].value)'
        fv = self.request.post(url,data = {'command':cmd})
        # get outputs
        acceleration = float(fa.result().text)
        turn = float(fv.result().text)
        return [acceleration,turn]
    