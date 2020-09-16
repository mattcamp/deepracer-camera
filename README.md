# deepracer-camera
Displays the camera feed from a physical deepracer car

Note that running this script will log any other sessions out of the web UI so start this feed BEFORE you open the web interface to control the camera (the camera should keep working).

## Installation

1. Create a python3 virtualenv:
    ```
    python3 -m venv ./venv
    source ./venv/bin/activate
    ```
   
2. Install the requirements
   ```
   pip install -r requirements.txt
   ```
   
3. Edit dr-cam.py and set the IP of the car and the password

4. run it!

```
python ./dr-cam.py
```

Hit Esc to exit.

