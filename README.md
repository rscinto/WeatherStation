# WeatherStation
This is a simple weather station that will detect wind speed, temperature and humidity using a Raspberry Pi. 

# 3D Printables

* Anemometer
I would like to give credit to this creator for making the the Anemometer. 
https://www.thingiverse.com/thing:2875873 
Thank you. 

![Anemometer](https://github.com/rscinto/WeatherStation/tree/main/pictures/PXL_20201119_045906194.jpg)

* Fan Mount
I would like to give credit the this creator for making a 30mm fan mount for the Raspberry Pi. 
https://www.thingiverse.com/thing:3768077
Thank you. 

![Fan Mount](https://github.com/rscinto/WeatherStation/tree/main/pictures/PXL_20201209_054719347.jpg)

* Case
Here is my box that houses the Raspbery Pi. It's a bit thin and should be kept out of the sun. My green house has killed many of my weather nodes. 
https://www.thingiverse.com/thing:4679757

![Case](https://github.com/rscinto/WeatherStation/pictures/PXL_20201208_230936668.jpg)


# Dependencies
sudo apt-get update

sudo apt-get upgrade

sudo apt-get install python3-pip

sudo pip3 install --upgrade setuptools

sudo apt-get install -y python3 git python3-pip

sudo update-alternatives --install /usr/bin/python python $(which python2) 1

sudo update-alternatives --install /usr/bin/python python $(which python3) 2

sudo update-alternatives --config python

pip3 install RPI.GPIO

Settings:
sudo raspi-config
    Enable SPI
    Enable I2C

sudo apt-get install python-rpi.gpio python3-rpi.gpio

sudo apt-get update
sudo apt-get install build-essential python-pip python-dev python-smbus git
git clone https://github.com/adafruit/Adafruit_Python_GPIO.git
cd Adafruit_Python_GPIO
sudo python setup.py install

sudo pip3 install adafruit-blinka
sudo pip3 install adafruit-circuitpython-ssd1306

sudo apt-get install git
git clone https://github.com/adafruit/Adafruit_Python_SSD1306.git
cd Adafruit_Python_SSD1306
sudo python setup.py install

sudo apt-get install pigpiod


