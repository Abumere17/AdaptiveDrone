"""
    Daniel Diep
    TellControlMain.py

    Finalized class holding all functions required to communicate with the Tello drone. Also holds the GUI to help user set up a new drone
    
    TODO:
    - Setup walkthrough
    - Add all control functions 
    - All photography functions
    - Automated functions

"""
# Imports

# Drone class with all functions required for drone comms
class TelloControl:
    # Most likely just empty values? What do you need from other modules to make this object work? 
    def __init__(self):
        pass

    # GUI to help a user setup a new drone
    def setup_new_drone(self):
        print("Setting up new drone...")
        pass

    # Transmit drone FPV (just return as a frame, run.py will take care of actually displaying it)
    def get_drone_FPV(self):
        print("got drone!")
        pass

    # All control functions here

    # All camera functions here
    def take_photo(self):
        pass

    def take_vid(self):
        pass


# Test class here
if __name__ == "__main__":
    drone = TelloControl()
