# tensortube

Volhacks 2016 Project

## Functionality

1. User pastes a Youtube URL.
2. Our server downloads the Youtube video and chops it up into 1-second frames.
3. Our server passes each frame through a TensorFlow neural network to label the frames.
4. The user receives the **highest**-confidence labels and can jump to those points in the video.

## Development

1. Install python virtualenv.
> $ sudo pip2.7 install virtualenv

2. Set up the virtualenv.
> $ virtualenv venv

3. Enter the virtualenv.
> $ source venv/bin/activate

4. Install the required packages.
> $ pip install --requirement requirements.txt

5. After installing new packages, freeze them to the requirements.txt file.
> $ pip freeze > requirements.txt
