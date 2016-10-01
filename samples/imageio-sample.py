import pylab
import imageio
import sys
import math
from PIL import Image

filename = 'vid.mp4'
vid = imageio.get_reader(filename,  'ffmpeg')
fps = int(math.floor(vid.get_meta_data()['fps']))
dur = int(math.floor(vid.get_meta_data()['duration']))

for i in range(dur):
    frame = vid.get_data(i * fps)
    img = Image.fromarray(frame, 'RGB')
    img.save('frame-%d.jpg' % (i))

sys.exit(0)
