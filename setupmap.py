from modules import gui
from modules.config import res,simstep
import time

### --- CONFIG --- ###
image_path = "tracks/default.png"
track_path = "newtrack.track"
### -END-OF-CONFIG- ###

### screen initialization
screen = gui.Init(res)
### load map image
image = gui.LoadImage(image_path)
### draw image on screen
gui.DrawImage(screen,image)

### prepare trajectory list
track = []

### capture trajectory
while True:
    # refresh GUI and check for mouse click
    event = gui.CaptureClick(screen)
    # handle program exit
    if event == 0: break
    # continue if there was no click
    if event == 1: continue
    # save new track point
    click = event
    track.append(click)
    print(click)
    # show track on map
    gui.DrawDot(screen, click[0], click[1], size=2, color=(0, 180, 0))
    if len(track)>1:
        gui.DrawLine(screen, track[-1][0], track[-1][1], track[-2][0], track[-2][1])
        
### prepare camera list
cams = []

### setup cameras
map = screen.surface.copy()
cam = ()
while True:
    # get mouse position
    pointer = gui.MousePosition(screen)
    # draw FOV line
    if len(cam)>=2:
        gui.ClrScr(screen)
        gui.DrawSurface(screen,map)
        gui.DrawLine(screen, cam[0], cam[1], pointer[0], pointer[1], color=(255, 0, 0))
    # refresh GUI and check for mouse click
    event = gui.CaptureClick(screen)
    # continue if there was no click
    if event == 1: continue
    # handle program exit
    if event == 0: break
    # save cam coordinates
    cam += event
    # draw cam position
    if len(cam)==2: gui.DrawDot(screen, cam[0], cam[1], size=3, color=(255, 0, 0))
    # save completed coordinates to list
    if len(cam)==6:
        # draw complete FOV polygon
        gui.DrawLine(screen, cam[2], cam[3], cam[4], cam[5], color=(255, 255, 0))
        # add cam to list
        cams.append(cam)
        cam = ()
        print(cams[-1])
    # save map surface
    map = screen.surface.copy()
    
### close map screen
gui.CloseScreen(screen)

### save results to file
with open(track_path,"w",encoding="utf-8") as f:
    f.write("# Map image file: \n")
    f.write(image_path + "\n")
    f.write("# Map size: \n")
    f.write(str(res[0])+" "+str(res[1])+"\n")
    f.write("# Track coordinates: \n")
    for coords in track:
        f.write(str(coords[0])+" "+str(coords[1])+"\n")
    f.write("# Cam coordinates: \n")
    for coords in cams:
        f.write(" ".join([str(c) for c in coords])+"\n")
        
### print info
print("\nTrack saved to file '"+track_path+"'")
print("\nTrack coordinates:",track)
print("\nCam coordinates:",cams)
time.sleep(2)
input("\nPres enter to exit...")
