from djitellopy import tello

drone = tello.Tello()

drone.connect()

drone.takeoff()

drone.land()

drone.end()