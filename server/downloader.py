#!/usr/bin/env python2.7
from pytube import YouTube
import math
import cv2

#this function downloads a video by url
#and uses openCV to return its image array
def extract_files(url):
    videoFolder = './server/videos'
    # Set filename to id
    yt = YouTube(url)
    id = url.split("v=")[-1] if len(url.split("v=")) == 2 else url.rsplit('/', 1)[-1]
    yt.set_filename(id)
    #download video of certain quality
    video = yt.get('mp4', '360p')
    try:
    	video.download(videoFolder)
        print("done downloading video")
    except OSError:
        print("didn't need to download video")
        pass

    frames = []
    cap = cv2.VideoCapture(videoFolder + "/"+id+".mp4")
    frameRate = cap.get(5) #frame rate
    while(cap.isOpened()):
        frameId = cap.get(1) #current frame number
        ret, frame = cap.read()
        if (ret != True):
            break
        if (frameId % math.floor(frameRate) == 0):
            frames.append(frame)
    cap.release()

    return frames
