# tensortube

Volhacks 2016 Project by Douglas Aaser, Jeremy Anantharaj, Grant Bruer, Alex Klibisz

## Functionality

1. User pastes a Youtube URL.
2. Our server downloads the Youtube video and chops it up into 1-second frames.
3. Our server passes each frame through a TensorFlow neural network to label the frames.
4. The user receives the **highest**-confidence labels and can jump to those points in the video.

## How does it work?

TensorTube is a fairly simple combination of video processing and a single neural network implemented in python.

We take the youtube URL you give us, download a low-res copy of that video, and chop it up into 1-second frames. Then we feed each one of those frames through a [TensorFlow deep neural network](https://github.com/alexklibisz/tensortube) trained on the [ImageNet dataset](http://imagenet.stanford.edu/). The neural network labels each frame with several labels with varying confidence each. We pick the highest confidence labels and send them back to the web app so the user can jump to frames of the video based on the labels.

Our server isn't the beefiest, so if yourr video is slow to be labeled, you can follow the development instructions to run TensorTube on your own laptop.

## Development Instructions

We tried doing a neat virtual environment, but it wouldn't play nicely with monsters like opencv and tensorflow. It's unrefined, but you'll need to make sure you have pip installed and then run the script install-packages.sh:

> $ wget https://bootstrap.pypa.io/get-pip.py && sudo python2.7 get-pip.py
> $ ./install-packages.sh

After that you should be able to run the `server/main.py` script and open up the app on `localhost:5000`:

> $ ./server/main.py

## Deployment on AWS

1. Buy a domain name on namecheap.
2. Launch an ubuntu 14.04 ec2 on AWS and ssh into it.
3. Install Apache, the apache wsgi module, and git on the server.
> $ sudo apt-get install apache2 libapache2-mod-wsgi git

4. [Use this as a reference for getting the domain to point to the server.](http://techgenix.com/namecheap-aws-ec2-linux/)
5. Clone the app into the `/home/ubuntu` home directory.
> $ git clone https://github.com/alexklibisz/tensortube.git

6. Install the python libraries as user-level dependencies.
> $ ./install-packages.py

7. Copy the apache config to the config folder.
> $ sudo cp tensortube.conf /etc/apache2/sites-available

8. Disable the default site, enable the tensortube site, restart apache.
> $ sudo a2dissite 000-default.config
> $ sudo a2ensite tensortube.conf
> $ sudo service apache restart

9. View server logs at `/var/log/apache2/*.log`

## TODO

- Figure out a memory leak with the server (it crashes sporatically with a Memory Error).
- Limit the duration of video that can be submitted with clear error message.

***

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
