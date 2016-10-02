# tensortube

Volhacks 2016 Project

## Functionality

1. User pastes a Youtube URL.
2. Our server downloads the Youtube video and chops it up into 1-second frames.
3. Our server passes each frame through a TensorFlow neural network to label the frames.
4. The user receives the **highest**-confidence labels and can jump to those points in the video.

## Development

We tried doing a neat virtual environment, but it wouldn't play nicely with monsters like opencv and tensorflow. So you'll need to run the script install-packages.sh.

> $ wget https://bootstrap.pypa.io/get-pip.py && sudo python2.7 get-pip.py
> $ ./install-packages.sh

## Deployment

1. Buy a domain name on namecheap.
2. Launch an ubuntu 14.04 ec2 on AWS and ssh into it.
3. Install Apache, the apache wsgi module, and git on the server.
> $ sudo apt-get install apache2 libapache2-mod-wsgi git

4. [Use this as a reference for getting the domain to point to the server.](http://techgenix.com/namecheap-aws-ec2-linux/)
5. Clone the app into the `/home/ubuntu` home directory.
> $ git clone https://github.com/alexklibisz/tensortube.git

6. Copy the apache config to the config folder.
> $ sudo cp tensortube.conf /etc/apache2/sites-available

7. Disable the default site, enable the tensortube site, restart apache.
> $ sudo a2dissite 000-default.config
> $ sudo a2ensite tensortube.conf
> $ sudo service apache restart

8. View server logs at `/var/log/apache2/*.log`

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
