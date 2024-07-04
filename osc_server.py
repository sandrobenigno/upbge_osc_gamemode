### This script is based on a study form Jose Padovani
### Look at https://github.com/zepadovani/upbge_osc_gamemode

### Author: Sandro Benigno
### Fork at: https://github.com/sandrobenigno/upbge_osc_gamemode

### This one here has few improvements and new resourses:
### Improvement:
### /move and /rotate are object agnostic, you can now send the obj_name in the OSC message
### New resource:
### /play executes an action of a given obj extracting it's animation start_frame and end_frame automaticaly

import bge
import bpy
from bge import logic
from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server
import threading
import time
import queue

#print("Starting osc_server.py script...")  # Debugging message

# Global variables and constants
ip = "127.0.0.1"  # OSC server IP address of the UPBGE game
port = 9999  # OSC server port

scene = logic.getCurrentScene()  # Get the current game scene
objects = scene.objects  # Get all objects in the scene
should_run = True  # Flag to control the server loop    
q = queue.Queue()  # Queue for communicating with the server thread
server_thread = None  # Reference to the server thread

# Check if the server is already running
if "server_started" not in bge.logic.globalDict:
    bge.logic.globalDict["server_started"] = False

# Functions
def move(unused_addr, obj_name, x, y, z):
    obj = objects.get(obj_name)  # Get the object by name
    if obj:
        print(f"-> Moving object '{obj_name}' with values: {x}, {y}, {z}")
        obj.applyMovement([x, y, z], True)  # Move the object
    else:
        print(f"Object '{obj_name}' not found.")

def rotate(unused_addr, obj_name, rx, ry, rz):
    obj = objects.get(obj_name)  # Get the object by name
    if obj:
        print(f"-> Rotating object '{obj_name}' with values: {rx}, {ry}, {rz}")
        obj.applyRotation([rx, ry, rz], True)  # Rotate the object
    else:
        print(f"Object '{obj_name}' not found.")

def get_action_frame_range(anim_name):
    """Get the start and end frame of the action with the given name."""
    action = bpy.data.actions.get(anim_name)
    if action:
        return action.frame_range[0], action.frame_range[1]
    return None, None

def play_action(unused_addr, obj_name, anim_name):
    obj = objects.get(obj_name)  # Get the object by name
    if obj:
        start_frame, end_frame = get_action_frame_range(anim_name)
        if start_frame is not None and end_frame is not None:
            try:
                print(f"-> Playing animation '{anim_name}' on object '{obj_name}' from frame {start_frame} to {end_frame}")
                obj.playAction(anim_name, start_frame=start_frame, end_frame=end_frame, layer=0, play_mode=bge.logic.KX_ACTION_MODE_PLAY)
            except Exception as e:
                print(f"Failed to play animation '{anim_name}' on object '{obj_name}': {e}")
        else:
            print(f"Animation '{anim_name}' not found or has no valid frame range.")
    else:
        print(f"Object '{obj_name}' not found.")

def quit(unused_addr, *args):
    global should_run
    should_run = False  # Stop the server loop
    print("Received /quit message, stopping the server.")
    quit_thread = threading.Thread(target=shutdown_thread, args=(q,))
    quit_thread.start()  # Start a thread to handle the clean shutdown

def server_thread_func(q):
    global ip, port
    server = osc_server.ThreadingOSCUDPServer((ip, port), dispatcher)  # Create the OSC server
    print("Serving on {}".format(server.server_address))
    q.put(server)  # Put the server reference on the queue
    server.serve_forever()  # Handle incoming OSC requests

def shutdown_thread(q):
    server = q.get()  # Retrieve the server object from the queue
    print("Shutting down server...")
    server.shutdown()  # Shut down the server
    time.sleep(0.5)
    print('... server shutdown!')
    print('Running server_close...')
    server.server_close()  # Close the server cleanly
    print('... finished server_close!')
    time.sleep(0.5)
    print("Ending game")
    logic.endGame()  # End the Blender Game Engine

def main():
    if not bge.logic.globalDict["server_started"]:
        print("Starting server")
        global server_thread
        server_thread = threading.Thread(target=server_thread_func, name="OSCserver", args=(q,))
        server_thread.start()
        bge.logic.globalDict["server_started"] = True

# OSC Setup
dispatcher = Dispatcher()
dispatcher.map("/move", move)      
dispatcher.map("/rotate", rotate)   
dispatcher.map("/play", play_action)
dispatcher.map("/quit", quit)

# Start the game loop
main()
#print("osc_server.py script ended.")  # Debugging message
