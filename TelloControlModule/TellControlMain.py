"""
    Daniel Diep
    TellControlMain.py

    Finalized class holding all functions required to communicate with the Tello drone
    
    TODO:
    - Setup functions
    - Add all control functions 
    - All photography functions
    - Automated functions
    - Design this class so that functions can be called easily in "AppMainAndGUI\run.py"

"""
# Imports

class TellControl:
    # Set up a new drone
    def __init__(self):
        pass

    # Transmit drone FPV (just return as a frame, run.py will take care of actually displaying it)
    def get_drone_FPV(self):
        pass

    # All control functions here

    def take_photo(self):
        pass

    def take_vid(self):
        pass


# Test class here
if __name__ == "__main__":
    drone = TellControl()
