# tensortube

Volhacks 2016 Project

## Functionality

1. User pastes a Youtube URL.
2. Our server downloads the Youtube video and chops it up into 1-second frames.
3. Our server passes each frame through a TensorFlow neural network to label the frames.
4. The user receives the **highest**-confidence labels and can jump to those points in the video.

## Development

We tried doing a neat virtual environment, but it wouldn't play nicely with monsters like opencv and tensorflow. So you'll need to run the script install-packages.sh.

> $ sudo apt-get install pip # Install pip if you don't have it.
> $ ./install-packages.sh

## Hosting

- [This was a nice reference for setting up the AWS/Namecheap domain name.](http://techgenix.com/namecheap-aws-ec2-linux/)


## Virtual Environment (Non-working)

1. Install python virtualenv.
> $ sudo pip2.7 install virtualenv

2. Set up the virtualenv.
> $ virtualenv venv

3. Enter the virtualenv.
> $ source venv/bin/activate

4. Install the required packages.
> $ pip install --requirement requirements.txt

5. It might fail on the Tensorflow package, in which case:
> $ export TF_BINARY_URL=https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-0.11.0rc0-cp27-none-linux_x86_64.whl
> $ pip install $TF_BINARY_URL

6. After installing new packages, freeze them to the requirements.txt file.
> $ pip freeze > requirements.txt
