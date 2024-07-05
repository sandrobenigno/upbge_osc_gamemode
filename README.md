# UPBGE (0.36.1) - control game objects using OSC messages (SB Version)

This project is based on a great study by Jose Padovani.
Take a look at https://github.com/zepadovani/upbge_osc_gamemode

#### Author: Sandro Benigno
This version has few improvements and a new feature:

Improvement:

/move and /rotate commands are object agnostic, you can now send the obj_name in the OSC message

New feature:

/play executes an action of a given object, extracting its animation's start_frame and end_frame automatically.

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
