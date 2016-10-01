# tensortube

Volhacks 2016 Project

## Functionality

1. User pastes a Youtube URL.
2. Our server downloads the Youtube video and chops it up into 1-second frames.
3. Our server passes each frame through a TensorFlow neural network to label the frames.
4. The user receives the highest-confidence labels and can jump to those points in the video.
