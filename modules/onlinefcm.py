import fcmlib

class FCMcontroller():

    # FCM controller class
    def __init__(self, map, server):
        self.map = None #init from url

    # Control method
    def control(self, distance, angle): #return [acceleration, turn]
        # activations of input concepts
        self.map["Angle"] = self.map["Angle"].inputMF.evaluate(angle)
        self.map["Distance"] = self.map["Distance"].inputMF.evaluate(distance)
        # activations of output concepts
        self.map.update()
        # return outputs
        acceleration = self.map["Acceleration"].value
        acceleration = self.map["Acceleration"].outputMF.evaluate(acceleration)
        turn = self.map["Turn"].value
        turn = self.map["Turn"].outputMF.evaluate(turn)
        #print('input = ' + str(distance) + ' ' + str(angle))
        #print('output = ' + str(acceleration) + ' ' + str(turn))
        return [acceleration,turn]

def _initMapTemplate():
    #create model
    map = fcmlib.FCM()
    map.name = "Controller"
    #set default relation
    map.config.defaultRelation = fcmlib.relations.R3Term
    #add & connect concepts
    for inputs in ["Angle","Distance"]:
        for outputs in ["Turn","Acceleration"]:
            map.connect(inputs,outputs)
    #initialize membership functions
    for inputs in ["Angle","Distance"]:
        map[inputs].inputMF = fcmlib.functions.PiecewiseLinear()
    for outputs in ["Turn","Acceleration"]:
        map[outputs].outputMF = fcmlib.functions.Predefined()
    #set concept membership functions
    map["Angle"].inputMF.set("-91:0 -90:0 90:1 91:1")
    map["Distance"].inputMF.set("-1:0 0:0 40:1 41:1")
    map["Turn"].outputMF.set("90*x-45")
    map["Acceleration"].outputMF.set("20*(x-0.5)")
    #check proper serialization
    s = map.serialize()
    m = fcmlib.FCM(s)
    #return template
    return m.serialize()

    