#!/usr/bin/python
# This Python file uses the following encoding: utf-8

from modules import gui
from modules import onlinesim as simulation

# set online FCMs URLS
server = "http://127.0.0.1:5000/"
# init track
track = simulation.Track("tracks/default.track")
# set initial car position
start = 0
x = track.point[start].x
y = track.point[start].y
angle = track.gate[start].angle-110
# init car
car = simulation.Car(x_pos=x, y_pos=y, direction=angle)
# init navigator
navdist = 30
stopdist = 100
detector = simulation.Detector("models/cams",track.cams,server)
navigator = simulation.Navigator(track, detector, car, start, navdist, stopdist)
# init controller
controller = simulation.SimpleController()
# init timer
timer = simulation.Timer()
# init simulator
simulator = simulation.Simulator(track, car, detector, navigator, controller, timer)
# init gui screen
screen = gui.Init(track.res)
# run control loop
run = 1
while (run):
    # run simulation step
    simulator.runSimulationStep()
    # refresh gui screen
    run = gui.ShowSimulation(screen, simulator)
    # reset simulator on finish
    if navigator.lost or navigator.finished:
        car = simulation.Car(x_pos=x, y_pos=y, direction=angle)
        navigator = simulation.Navigator(track, detector, car, start, navdist, stopdist)
        controller = simulation.SimpleController()
        timer = simulation.Timer()
        simulator = simulation.Simulator(track, car, detector, navigator, controller, timer)
