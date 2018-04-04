import fcmlib as fcm
from random import random

### CONFIGURATION
file_path = "tracks/default.track"
training_iterations = 30000

### LOAD CAMS
print("\nLoading cameras from file ("+file_path+")... ",end="")
cams = []
res = None
with open(file_path) as f:
    #read simulation setup file
    lines = [line for line in f]
    #get map resolution
    res = [int(dim) for dim in lines[3].split()]
    #skip track points
    i=5
    while lines[i][0] != "#": 
        i+=1
    #read cameras
    i=i+1
    for line in lines[i:]:
        if line == "": break 
        cams.append([int(coord) for coord in line.split()])
print("OK")

### SETUP FCM MODELS
print("Creating FCM models... ",end="")
models=[]
# inputs: object detection, object coordinates on camera
# outputs: object coordinates in space, confidence
for i,cam in enumerate(cams):
    #create model
    model = fcm.FCM()
    model.name = "Camera"+str(i)
    #set model relations & functions
    model.config.defaultRelation = fcm.relations.RNeural
    model.config.defaultInputMF = fcm.functions.Predefined
    model.config.defaultOutputMF = fcm.functions.Predefined
    #add & connect concepts
    for c_in in ["Detection","CamX","CamY"]:
        for c_out in ["Confidence","OutputX","OutputY"]:
            model.connect(c_in,c_out)
    #setup concept membership functions
    for concept in ["Detection","Confidence"]:
        #identity functions f(x)=x
        model[concept].inputMF.set("x")
        model[concept].outputMF.set("x")
    for concept in ["CamX","OutputX"]:
        #rescale to map resolution
        model[concept].inputMF.set("x/"+str(res[0]))
        model[concept].outputMF.set("x*"+str(res[0]))
    for concept in ["CamY","OutputY"]:
        #rescale to map resolution
        model[concept].inputMF.set("x/"+str(res[1]))
        model[concept].outputMF.set("x*"+str(res[1]))    
    #add model to the list
    models.append(model)
print("OK")

### CHECK FOR SERIALIZATION ERRORS
print("Checking proper model serialization... ", end="")
for model in models:
    s = model.serialize()
    m = fcm.FCM(s)
    m.serialize()
print("OK")

### TRAIN MODELS
print("\nTraining models... ")

#auxiliary functions: https://stackoverflow.com/questions/2049582/how-to-determine-if-a-point-is-in-a-2d-triangle 
def sign(p1,p2,p3):
    return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])
def oncam (pt,v1,v2,v3):
    b1 = sign(pt, v1, v2) < 0.01
    b2 = sign(pt, v2, v3) < 0.01
    b3 = sign(pt, v3, v1) < 0.01
    if (b1 == b2) and (b2 == b3): return 1
    else: return 0
#model training
for iteration in range(training_iterations):
    #generate inputs
    rx = random()*res[0]
    ry = random()*res[1]            
    for cam, model in zip(cams,models):
        #detect on camera
        detection=oncam((rx,ry),(cam[0],cam[1]),(cam[2],cam[3]),(cam[4],cam[5]))        
        #fuzzyfi inputs
        model["CamX"] = model["CamX"].inputMF.evaluate(rx)
        model["CamY"] = model["CamY"].inputMF.evaluate(ry)
        model["Detection"] = model["Detection"].inputMF.evaluate(detection)
        #produce outputs
        model.update()
        #get error
        d_x = model["CamX"].value - model["OutputX"].value
        d_y = model["CamY"].value - model["OutputY"].value
        d_d = model["Detection"].value - model["Confidence"].value
        #update weights
        model["OutputX"].relation.adapt(d_x,1)
        model["OutputY"].relation.adapt(d_y,1)
        model["Confidence"].relation.adapt(d_d,1)
    if iteration % (training_iterations/10) == 0:
        print(" -",int(100*iteration/training_iterations),"%, error =", (abs(d_x)+abs(d_y)+abs(d_d))/3)
print(" - 100%\nDone.")

### TESTING
print("\nTesting models... ")
for model in models:
    #generate inputs
    rx = random()*res[0]
    ry = random()*res[1]
    #detect on camera
    detection=oncam((rx,ry),(cam[0],cam[1]),(cam[2],cam[3]),(cam[4],cam[5]))        
    #fuzzyfi inputs
    model["CamX"] = model["CamX"].inputMF.evaluate(rx)
    model["CamY"] = model["CamY"].inputMF.evaluate(ry)
    model["Detection"] = model["Detection"].inputMF.evaluate(detection)
    #produce outputs
    model.update()
    #get error
    d_x = model["CamX"].value - model["OutputX"].value
    d_y = model["CamY"].value - model["OutputY"].value
    d_d = model["Detection"].value - model["Confidence"].value
    print(" - "+model.name+":",model,"error =", (abs(d_x)+abs(d_y)+abs(d_d))/3)
print("Done.")

### SAVE TO FILE
print("\nSaving models to files... ")
for model in models:
    print("- "+model.name+".fcm")
    with open(model.name+".fcm","w",encoding="utf-8") as f:
        f.write(model.serialize())
print("Done.")
input("\nPress enter to exit...")
        