# UPBGE (0.36.1) - control game objects using OSC messages (SB Version)

This project is based on a study form Jose Padovani
Look at https://github.com/zepadovani/upbge_osc_gamemode

## Author: Sandro Benigno
This one here has few improvements and new resourses:
Improvement:
/move and /rotate commands are object agnostic, you can now send the obj_name in the OSC message

New resource:
/play executes an action of a given obj extracting it's animation start_frame and end_frame automaticaly

1. Download this repository:
```
git clone https://github.com/sandrobenigno/upbge_osc_gamemode
```

2. Download pythonosc to the same folder of the blend file, so that the standalone app can find the module there

```
cd upbge_osc_gamemode
pip install --target ./ python-osc
```

3. Run the game (press 'p' to play the embedded game or select the standalone version in render options)

4. Run the SuperCollider code to send messages to move, rotate and play actions of the objects by name

5. Run the /quit message to end the server, close the port and exit the game
