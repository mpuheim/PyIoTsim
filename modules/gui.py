# This Python file uses the following encoding: utf-8

import pygame, os, sys
from math import sin, cos, sqrt
from modules.config import zoomin, zoomout
from modules.simulation import pointToPointDist, Car
from modules.utils import struct

degree_to_radian = 0.0174532925
radian_to_degree = 57.2957795

def Init(res):
    # Open a display window
    pygame.init()
    screen=struct()
    screen.surface=pygame.display.set_mode((res[0],res[1]))
    screen.res = res
    screen.zoom_mode = 0
    screen.car_size = res[0]/50
    pygame.display.set_caption('PyIoTsim')
    pygame.font.init()
    return screen
    
def InitMultiscreen(res,screens):
    # Open new multiscreen display window
    pygame.init()
    # Set subwindow sizes
    col_count = int(sqrt(screens))
    row_count = int(screens/col_count)
    height = int(res[1]*zoomout) + 20
    width = int(res[0]*zoomout)
    # Init main screen
    screen=struct()
    screen.res = (10+row_count*width,10+col_count*height)
    screen.surface=pygame.display.set_mode(screen.res,pygame.FULLSCREEN)
    screen.zoom_mode = 0
    screen.car_size = res[0]/50
    screen.mesh = pygame.Surface(screen.res)
    screen.mesh.fill((255, 255, 255))
    pygame.display.set_caption('PyIoTsim')
    pygame.font.init()
    # Init subscreens
    screen.subscreen = []
    i = 0
    for y in range(col_count):
        for x in range(row_count):
            i += 1
            x_pos = 5+x*width
            y_pos = 5+y*height
            screen.subscreen.append(InitSubscreen(i,(x_pos,y_pos),(width,height)))
            pygame.draw.rect(screen.mesh,(0, 0, 0),(x_pos,y_pos,width-1,height-1),1)
    screen.mesh.set_colorkey((255, 255, 255))
    return screen

def InitSubscreen(id,pos,res):
    # Open a display window
    subscreen=struct()
    subscreen.surface=pygame.Surface((res[0],res[1]))
    subscreen.position = pos
    subscreen.res = res
    subscreen.id = id
    subscreen.zoom_mode = 2
    subscreen.car_size = res[0]/50
    ClrScr(subscreen)
    return subscreen

# static sound variables
sounds = None
silent = False

def PlaySound(sound):
    global sounds
    if sounds == None or silent == True or pygame.mixer.get_busy():
        return
    else:
        sound.play()
        
def EnableSound():
    global silent
    silent = False
    
def MuteSound():
    global silent
    silent = True

def InitSound():
    global sounds
    if sounds == None:
        sounds=struct()
        try:
            next_path = os.path.normpath(os.getcwd()+'/media/continue.wav')
            sounds.next = pygame.mixer.Sound(next_path)
        except:
            print("Warning - Could not load sound from \'" + next_path + "\'.")
        try:
            wait_path = os.path.normpath(os.getcwd()+'/media/waiting.wav')
            sounds.wait = pygame.mixer.Sound(wait_path)
        except:
            print("Warning - Could not load sound from \'" + wait_path + "\'.")
        try:
            end_path = os.path.normpath(os.getcwd()+'/media/applause.wav')
            sounds.end = pygame.mixer.Sound(end_path)
        except:
            print("Warning - Could not load sound from \'" + end_path + "\'.")
    
def ClrScr(screen):
    # Change entire screen to white color
    screen.surface.fill((255, 255, 255))
    
def DrawDot(screen, x, y, size=1, color=(0, 0, 0), fill=0):
    # Draw dot on screen
    pygame.draw.circle(screen.surface, color, (x,y), size, fill)
    
def DrawLine(screen, x1, y1, x2, y2, color=(0, 0, 0), width=1):
    # Draw line on screen
    if width > 1: pygame.draw.line(screen.surface, color, (x1, y1), (x2, y2), width)
    else: pygame.draw.aaline(screen.surface, color, (x1, y1), (x2, y2), 1)
    
def DrawImage(screen, image, x1=None, y1=None, x2=None, y2=None):
    # Draw image on screen
    if (x1 == None) and (y1 == None) and (x2 == None) and (y2 == None):
        x1 = 0; y1 = 0; x2 = screen.res[0]; y2 = screen.res[1]
    image = pygame.transform.scale(image, (x2-x1, y2-y1))
    screen.surface.blit(image, (x1,y1))
    
def LoadImage(path):
    # Load image from file
    return pygame.image.load(path)

def DrawPolygon(screen, points, color=(0, 0, 0), width=0):
    # Draw polygon on screen
    pygame.draw.polygon(screen.surface, color, points, width)
    
def DrawSurface(screen,surface,x=0,y=0):
    # Draw surface on screen
    screen.surface.blit(surface,(x,y))
    
def DrawCar(screen, car, navigator = None, color=(0, 0, 255)):
    # Draw car on screen
    if screen.zoom_mode == 0:
        # Normal mode draw
        C_x = int(round(car.x_pos))
        C_y = int(round(car.y_pos))
        radian = car.direction*degree_to_radian
        F_x = int(round(car.x_pos + screen.car_size * cos(radian)))
        F_y = int(round(car.y_pos + screen.car_size * sin(radian)))
        radian = ((car.direction+90)%360) * degree_to_radian
        L_x = int(round(car.x_pos + 0.4 * screen.car_size * cos(radian)))
        L_y = int(round(car.y_pos + 0.4 * screen.car_size * sin(radian)))
        radian = ((car.direction+270)%360) * degree_to_radian
        R_x = int(round(car.x_pos + 0.4 * screen.car_size * cos(radian)))
        R_y = int(round(car.y_pos + 0.4 * screen.car_size * sin(radian)))
        DrawPolygon(screen,[[L_x,L_y], [R_x,R_y], [F_x,F_y]], color)
        if (navigator != None):
            C_x = int(round(navigator.car.x_pos))
            C_y = int(round(navigator.car.y_pos))
            radian = navigator.car.direction*degree_to_radian
            F_x = int(round(navigator.car.x_pos + screen.car_size * cos(radian)))
            F_y = int(round(navigator.car.y_pos + screen.car_size * sin(radian)))
            radian = ((navigator.car.direction+90)%360) * degree_to_radian
            L_x = int(round(navigator.car.x_pos + 0.4 * screen.car_size * cos(radian)))
            L_y = int(round(navigator.car.y_pos + 0.4 * screen.car_size * sin(radian)))
            radian = ((navigator.car.direction+270)%360) * degree_to_radian
            R_x = int(round(navigator.car.x_pos + 0.4 * screen.car_size * cos(radian)))
            R_y = int(round(navigator.car.y_pos + 0.4 * screen.car_size * sin(radian)))
            DrawPolygon(screen,[[L_x,L_y], [R_x,R_y], [F_x,F_y]], color=[channel//2 for channel in color])
            next = navigator.next_gate
            G_x = int(round(navigator.track.point[next].x))
            G_y = int(round(navigator.track.point[next].y))
            L_dist = pointToPointDist(G_x,G_y,L_x,L_y)
            R_dist = pointToPointDist(G_x,G_y,R_x,R_y)
            if abs(navigator.last_angle) > 10:
                if L_dist < R_dist: DrawLine(screen, L_x, L_y, F_x, F_y, (255, 100, 100),3)
                else: DrawLine(screen, R_x, R_y, F_x, F_y, (255, 100, 100),3)
            if navigator.lost == True:
                color = (255, 0, 0)
            else:
                color = (255, 255, 0)
            if navigator.finished == False:
                DrawLine(screen, F_x, F_y, G_x, G_y, color)
                DrawDot(screen, G_x, G_y, 3, color)
    elif screen.zoom_mode == 1:
        # Zoom mode draw (car is always in center of screen)     
        C_x = screen.surface.get_width()/2
        C_y = screen.surface.get_height()/2
        radian = car.direction*degree_to_radian
        F_x = int(round(C_x+zoomin*screen.car_size*cos(radian)))
        F_y = int(round(C_y+zoomin*screen.car_size*sin(radian)))
        radian = ((car.direction+90)%360) * degree_to_radian
        L_x = int(round(C_x+zoomin*0.4*screen.car_size*cos(radian)))
        L_y = int(round(C_y+zoomin*0.4*screen.car_size*sin(radian)))
        radian = ((car.direction+270)%360) * degree_to_radian
        R_x = int(round(C_x+zoomin*0.4*screen.car_size*cos(radian)))
        R_y = int(round(C_y+zoomin*0.4*screen.car_size*sin(radian)))
        DrawPolygon(screen,[[L_x,L_y], [R_x,R_y], [F_x,F_y]], color)
        if (navigator != None):
            next = navigator.next_gate
            G_x_real = navigator.track.point[next].x
            G_y_real = navigator.track.point[next].y
            G_x = int(round(C_x-zoomin*(car.x_pos-G_x_real)))
            G_y = int(round(C_y-zoomin*(car.y_pos-G_y_real)))
            L_dist = pointToPointDist(G_x,G_y,L_x,L_y)
            R_dist = pointToPointDist(G_x,G_y,R_x,R_y)
            if abs(navigator.last_angle) > 10:
                if L_dist < R_dist: DrawLine(screen, L_x, L_y, F_x, F_y, (255, 100, 100),6)
                else: DrawLine(screen, R_x, R_y, F_x, F_y, (255, 100, 100),6)
            if navigator.lost == True:
                color = (255, 0, 0)
            else:
                color = (255, 255, 0)
            if navigator.finished == False:
                DrawLine(screen, F_x, F_y, G_x, G_y, color, 4)
                DrawDot(screen, G_x, G_y, 6, color)
    elif screen.zoom_mode == 2:
        # Zoom mode draw (resized track)
        C_x = int(round(car.x_pos*zoomout))
        C_y = int(round(car.y_pos*zoomout))
        radian = car.direction*degree_to_radian
        F_x = int(round(C_x+zoomout*screen.car_size*cos(radian)))
        F_y = int(round(C_y+zoomout*screen.car_size*sin(radian)))
        radian = ((car.direction+90)%360) * degree_to_radian
        L_x = int(round(C_x+zoomout*0.4*screen.car_size*cos(radian)))
        L_y = int(round(C_y+zoomout*0.4*screen.car_size*sin(radian)))
        radian = ((car.direction+270)%360) * degree_to_radian
        R_x = int(round(C_x+zoomout*0.4*screen.car_size*cos(radian)))
        R_y = int(round(C_y+zoomout*0.4*screen.car_size*sin(radian)))
        DrawPolygon(screen,[[L_x,L_y], [R_x,R_y], [F_x,F_y]], color)
        if (navigator != None):
            next = navigator.next_gate
            G_x_real = navigator.track.point[next].x
            G_y_real = navigator.track.point[next].y
            G_x = int(round(C_x-zoomout*(car.x_pos-G_x_real)))
            G_y = int(round(C_y-zoomout*(car.y_pos-G_y_real)))
            L_dist = pointToPointDist(G_x,G_y,L_x,L_y)
            R_dist = pointToPointDist(G_x,G_y,R_x,R_y)
            if abs(navigator.last_angle) > 10:
                if L_dist < R_dist: DrawLine(screen, L_x, L_y, F_x, F_y, (255, 100, 100),1)
                else: DrawLine(screen, R_x, R_y, F_x, F_y, (255, 100, 100),1)
            if navigator.lost == True:
                color = (255, 0, 0)
            else:
                color = (255, 255, 0)
            if navigator.finished == False:
                DrawLine(screen, F_x, F_y, G_x, G_y, color, 1)
                DrawDot(screen, G_x, G_y, 2, color)
    else:
        raise ValueError('Error. Undefined zoom level.')
    
def DrawTrack(screen, track, car, navigator):
    # Draw track on screen
    if screen.zoom_mode == 0:
        # Normal mode draw
        if DrawTrack.surface_normal == None:
            DrawTrack.surface_normal = pygame.Surface(screen.surface.get_size())
            DrawTrack.surface_normal.fill((255, 255, 255))
            image = LoadImage(track.mapfile)
            image = pygame.transform.scale(image, track.res)
            DrawTrack.surface_normal.blit(image, (0,0))
            for point in track.point:
                pygame.draw.circle(DrawTrack.surface_normal, (0,180,0), (point.x,point.y), 2)
            for cam in track.cams:
                pygame.draw.circle(DrawTrack.surface_normal, (255,0,0), (cam[0],cam[1]), 2)
                pygame.draw.aaline(DrawTrack.surface_normal, (255, 0, 0), (cam[0],cam[1]), (cam[2],cam[3]))
                pygame.draw.aaline(DrawTrack.surface_normal, (255, 0, 0), (cam[0],cam[1]), (cam[4],cam[5]))
                pygame.draw.aaline(DrawTrack.surface_normal, (255, 255, 0), (cam[2],cam[3]), (cam[4],cam[5]))
        screen.surface.blit(DrawTrack.surface_normal,(0,0))
    elif screen.zoom_mode == 1:
        # zoomin mode draw
        if DrawTrack.surface_zoom == None:
            width = zoomin * screen.surface.get_width()
            height = zoomin * screen.surface.get_height()
            DrawTrack.surface_zoom = pygame.Surface((width, height))
            DrawTrack.surface_zoom.fill((255, 255, 255))
            count = len(track.gate)
            for current in range(0,count-1):
                next = current + 1
                x1 = int(round(zoomin*track.gate[current].left_x))
                y1 = int(round(zoomin*track.gate[current].left_y))
                x2 = int(round(zoomin*track.gate[current].right_x))
                y2 = int(round(zoomin*track.gate[current].right_y))
                pygame.draw.line(DrawTrack.surface_zoom, (0, 0, 0), (x1, y1), (x2, y2),3)
                x1 = int(round(zoomin*track.gate[current].left_x))
                y1 = int(round(zoomin*track.gate[current].left_y))
                x2 = int(round(zoomin*track.gate[next].left_x))
                y2 = int(round(zoomin*track.gate[next].left_y))
                pygame.draw.line(DrawTrack.surface_zoom, (255, 0, 0), (x1, y1), (x2, y2),3)
                x1 = int(round(zoomin*track.gate[current].right_x))
                y1 = int(round(zoomin*track.gate[current].right_y))
                x2 = int(round(zoomin*track.gate[next].right_x))
                y2 = int(round(zoomin*track.gate[next].right_y))
                pygame.draw.line(DrawTrack.surface_zoom, (255, 0, 0), (x1, y1), (x2, y2),3)
            x1 = int(round(zoomin*track.gate[navigator.start_gate].left_x))
            y1 = int(round(zoomin*track.gate[navigator.start_gate].left_y))
            x2 = int(round(zoomin*track.gate[navigator.start_gate].right_x))
            y2 = int(round(zoomin*track.gate[navigator.start_gate].right_y))
            pygame.draw.line(DrawTrack.surface_zoom, (0, 255, 0), (x1, y1), (x2, y2),6)
        screen.surface.blit(DrawTrack.surface_zoom, (int(round(screen.surface.get_width()/2-zoomin*car.x_pos)), int(round(screen.surface.get_height()/2-zoomin*car.y_pos))))
    elif screen.zoom_mode == 2:
        # Resized mode draw
        if DrawTrack.surface_resized == None:
            DrawTrack.surface_resized = pygame.Surface(screen.surface.get_size())
            DrawTrack.surface_resized.fill((255, 255, 255))
            image = LoadImage(track.mapfile)
            image = pygame.transform.scale(image, screen.surface.get_size())
            DrawTrack.surface_resized.blit(image, (0,0))
            for point in track.point:
                x = int(zoomout*point.x)
                y = int(zoomout*point.y)
                pygame.draw.circle(DrawTrack.surface_resized, (0,180,0), (x,y), 2)
            for cam in track.cams:
                x1 = int(zoomout*cam[0])
                y1 = int(zoomout*cam[1])
                x2 = int(zoomout*cam[2])
                y2 = int(zoomout*cam[3])
                x3 = int(zoomout*cam[4])
                y3 = int(zoomout*cam[5])
                pygame.draw.circle(DrawTrack.surface_resized, (255,0,0), (x1,y1), 2)
                pygame.draw.aaline(DrawTrack.surface_resized, (255, 0, 0), (x1,y1), (x2,y2))
                pygame.draw.aaline(DrawTrack.surface_resized, (255, 0, 0), (x1,y1), (x3,y3))
                pygame.draw.aaline(DrawTrack.surface_resized, (255, 255, 0), (x2,y2), (x3,y3))
        screen.surface.blit(DrawTrack.surface_resized,(0,0))
    else:
        raise ValueError('Error. Undefined zoom level.')

# Static variables of function DrawTrack()
DrawTrack.surface_normal = None
DrawTrack.surface_zoom = None
DrawTrack.surface_resized = None

def DrawTrajectory(screen, simulator, statistics, results):
    # Set mode
    rs = 1.0
    if screen.zoom_mode == 1: rs = float(zoomin)
    elif screen.zoom_mode == 2: rs = float(zoomout)
    # Clear screen
    ClrScr(screen)
    # Draw tracks
    DrawTrack(screen, simulator.track, simulator.car, simulator.navigator)
    # Draw car trajectory
    time = 1
    prev_stat = statistics[0]
    for stat in statistics:
        if stat.time > time:
            # Draw trajectory
            x1 = int(round(rs*prev_stat.x))
            y1 = int(round(rs*prev_stat.y))
            x2 = int(round(rs*stat.x))
            y2 = int(round(rs*stat.y))
            DrawLine(screen, x1, y1, x2, y2, (0, 0, 255))
            # Draw car position
            car = Car(x_pos=stat.x,y_pos=stat.y,direction=stat.direction)
            DrawCar(screen, car)
            # Show next position
            prev_stat = stat
            time += 1
    # Draw initial car position
    car = Car(x_pos=statistics[0].x,y_pos=statistics[0].y,direction=statistics[0].direction)
    DrawCar(screen, car, color = (0, 255, 0))
    # Draw last car position
    last_stat = statistics[-1]
    x1 = int(round(rs*prev_stat.x))
    y1 = int(round(rs*prev_stat.y))
    x2 = int(round(rs*last_stat.x))
    y2 = int(round(rs*last_stat.y))
    DrawLine(screen, x1, y1, x2, y2, (0, 0, 255))
    car = Car(x_pos=last_stat.x,y_pos=last_stat.y,direction=last_stat.direction)
    # Draw goal info for lost car
    if results.lost == True:
        DrawCar(screen, car, simulator.navigator, color = (255, 0, 0))
    else:
        DrawCar(screen, car, color = (255, 0, 0))
    # Show info
    font = pygame.font.SysFont("Courier",10)
    string = 'STATISTICS:'
    screen.surface.blit(font.render(string, True, (0,0,0)), (10,screen.surface.get_height() - 80))
    string = 'AVG Speed: ' + str(results.avg_speed) + ' px/s'
    screen.surface.blit(font.render(string, True, (0,0,0)), (10,screen.surface.get_height() - 70))
    string = 'AVG Acc:   ' + str(results.avg_acc) + ' px/s^2'
    screen.surface.blit(font.render(string, True, (0,0,0)), (10,screen.surface.get_height() - 60))
    string = 'AVG Turn:  ' + str(results.avg_turn) + ' degrees'
    screen.surface.blit(font.render(string, True, (0,0,0)), (10,screen.surface.get_height() - 50))
    string = 'Runtime:   ' + str(results.time) + ' sec'
    screen.surface.blit(font.render(string, True, (0,0,0)), (10,screen.surface.get_height() - 40))
    string = 'Distance:  ' + str(results.distance) + ' px'
    screen.surface.blit(font.render(string, True, (0,0,0)), (10,screen.surface.get_height() - 30))
    string = 'Remaining: ' + str(results.remaining) + ' px'
    screen.surface.blit(font.render(string, True, (0,0,0)), (10,screen.surface.get_height() - 20))

def ShowInfo(screen,string,pos=None,fontsize=20,color=(0,0,0)):
    if pos == None: pos = (screen.res[0]/5,screen.res[1]/3)
    font = pygame.font.SysFont("Courier",fontsize)
    lines = string.split("\n")
    for line in lines:
        screen.surface.blit(font.render(line, True, color), pos)
        pos = (pos[0],pos[1]+fontsize+5)
    
def saveScreen(screen,filename):
    pygame.image.save(screen.surface, filename)
    
def HandleEvents(screen,car):
    # Handle events
    while 1:
        # get event from event poll
        event = pygame.event.poll()
        # stop handling if event poll is empty
        if event.type == pygame.NOEVENT:
            return 1
        # return 0 if exit button is pressed
        if event.type == pygame.QUIT:
            return 0
        # return 0 if ESC is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return 0
        # handle car speed and turn parameters
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                car.update(turn = car.turn - 5)
            elif event.key == pygame.K_RIGHT:
                car.update(turn = car.turn + 5)
            elif event.key == pygame.K_UP:
                car.update(speed = car.speed + 10)
            elif event.key == pygame.K_DOWN:
                car.update(speed = car.speed - 10)
            elif event.key == pygame.K_s:
                car.update(speed = 0)
            elif event.key == pygame.K_z:
                if screen.zoom_mode == 0: screen.zoom_mode = 1
                else:                     screen.zoom_mode = 0 
    
def ShowSimulation(screen, simulator):
    # Handle events
    if HandleEvents(screen, simulator.car) == 0:
        return 0
    # Clear screen
    ClrScr(screen)
    # Show tracks
    DrawTrack(screen, simulator.track, simulator.car, simulator.navigator)
    # Show car on screen
    DrawCar(screen, simulator.car, simulator.navigator)
    # Show info
    font = pygame.font.SysFont("Courier",12)
    string = "Speed=" + str(int(simulator.car.speed)) + "  Turn=" + str(int(simulator.car.turn)) + "  Direction=" + str(int(simulator.car.direction)) + "  Pos: X=" + str(int(simulator.car.x_pos)) + " Y=" + str(int(simulator.car.y_pos))+ " Goal=" + str(int(simulator.navigator.last_angle))
    screen.surface.blit(font.render(string, True, (0,0,0)), (5,5))
    string = "Simulation time=" + str(int(simulator.timer.getSimTime())) + "  Real time=" + str(int(simulator.timer.getRealTime()))
    screen.surface.blit(font.render(string, True, (0,0,0)), (5,screen.surface.get_height() - 20))
    # Screen refresh
    pygame.display.flip()
    return 1
    
def MousePosition(screen):
    return pygame.mouse.get_pos()
    
def CaptureClick(screen):
    # Screen refresh
    pygame.display.flip()
    # Handle events
    while 1:
        # get event from event poll
        event = pygame.event.poll()
        # stop handling if event poll is empty
        if event.type == pygame.NOEVENT:
            return 1
        # capture mouse clicks
        if event.type == pygame.MOUSEBUTTONUP:
            return pygame.mouse.get_pos()
        # return 0 if exit button is pressed
        if event.type == pygame.QUIT:
            return 0
        # Return 0 if ESC is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return 0
    
def Refresh(screen):
    # Screen refresh
    pygame.display.flip()
    # Handle events
    while 1:
        # get event from event poll
        event = pygame.event.poll()
        # stop handling if event poll is empty
        if event.type == pygame.NOEVENT:
            return 1
        # Return 2 if F is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                return 2
        # return 0 if exit button is pressed
        if event.type == pygame.QUIT:
            return 0
        # Return 0 if ESC is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return 0
            
def ShowMultiScreen(screen):
    # Play initial sound
    PlaySound(sounds.next)
    # Multiscreen refresh
    font = pygame.font.SysFont("Courier",20)
    while 1:
        # Play sound
        PlaySound(sounds.wait)
        # Clear screen
        ClrScr(screen)
        # Draw subscreens
        for s in screen.subscreen:
            s.surface.blit(font.render("S"+str(s.id), True, (0,0,0)), (s.res[0]-30,s.res[1]-30))
            screen.surface.blit(s.surface,s.position)
        # Draw mesh
        screen.surface.blit(screen.mesh,(0,0))
        # Refresh screen
        pygame.display.flip()
        # Get event from event poll
        event = pygame.event.poll()
        # Return 0 if exit button is pressed
        if event.type == pygame.QUIT:
            return 0
        # Handle keyboard input
        if event.type == pygame.KEYDOWN:
            # Return 0 if ESC is pressed
            if event.key == pygame.K_ESCAPE:
                return 0
            # Return if right arrow key is pressed
            if event.key == pygame.K_RIGHT:
                return len(screen.subscreen)+1
            # Return if left arrow key is pressed
            if event.key == pygame.K_LEFT:
                return len(screen.subscreen)+2
            # Return if Carriage Return or Enter is pressed
            if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                return len(screen.subscreen)+3
        # Return ID of subscreen clicked
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            for s in screen.subscreen:
                if pos[0] > s.position[0] and pos[0] < s.position[0]+s.res[0]:
                    if pos[1] > s.position[1] and pos[1] < s.position[1]+s.res[1]:
                        # left button
                        if event.button == 1:
                            return s.id
                        # right button
                        if event.button == 3:
                            return -s.id
                            
def CloseScreen(screen):
    pygame.font.quit()
    pygame.quit()
