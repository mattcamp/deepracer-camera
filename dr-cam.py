import requests
from bs4 import BeautifulSoup
import cv2
import numpy as np
import os
import pprint
import json
import urllib3
urllib3.disable_warnings()

CAR_IP="192.168.0.119"
PASSWORD = "password"
FULL_SCREEN = False


if __name__ == "__main__":

    with requests.Session() as s:
        URL = "https://%s/" % CAR_IP
        post_login_url = URL+"login"
        video_url = URL+"route?topic=/display_mjpeg&width=640&height=480"
        home_url = URL+"home"

        # Get the CSRF Token
        # response = s.get(URL, verify=False)
        # 
        # soup = BeautifulSoup(response.text, 'lxml')
        # csrf_token = soup.select_one('meta[name="csrf-token"]')['content']
        # headers = {'X-CSRFToken': csrf_token}
        # # print("CSRF token found: " + str(csrf_token))
        # 
        # # Login to the DeepRacer web interface with Post
        # payload = {'password': PASSWORD}
        # post = s.post(post_login_url, data=payload, headers=headers, verify=False)

        # Get the video stream
        reset = False
        bytes = bytes()
        while True:
            print("Starting")
            reset = False

            video_stream = s.get(video_url, stream=True, verify=False)
            if video_stream.status_code == 200:
                print("Video Connected!")

                if FULL_SCREEN:
                    cv2.namedWindow("Deepracer camera stream", cv2.WND_PROP_FULLSCREEN)
                    cv2.setWindowProperty("Deepracer camera stream", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)


                for chunk in video_stream.iter_content(chunk_size=1024):
                    bytes += chunk
                    a = bytes.find(b'\xff\xd8')  # Marker byte pair
                    b = bytes.find(b'\xff\xd9')  # Trailing byte pair
                    #  If both byte pairs on in the stream then build the jpeg
                    if a != -1 and b != -1:
                        jpg = bytes[a:b + 2]
                        bytes = bytes[b + 2:]
                        i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                        window_title = "Deepracer %s camera" % CAR_IP
                        cv2.imshow('Deepracer camera stream', i)

                        if cv2.waitKey(1) == 27:
                            # exit(0)
                            reset = True
                            break

        else:
            print("Received unexpected status code {}".format(video_stream.status_code))