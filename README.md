# Raspberry PI Temperature with Azure IoT - Basic MQTT 

The goal of this project is to provide a very simple method of getting started with Azure IoT and an MQTT client using a real sensor.  I have selected a DHT11 Temperature and Humidity sensor given the simplicity of how to wire the solution.  

**This is not meant to be an all-inclusive tutorial to Azure IoT connectivity, but a simple "getting started".  To learn aout the platform and other options for connectivity, please refer to the Azure IoT documentation**
https://docs.microsoft.com/en-us/azure/iot-hub

**Special thanks for the code already included in this repository that helps read the sensor values from the DHT11**
https://github.com/szazo/DHT11_Python.git

## Raspberry PI Setup and Prerequisits

1. Verify you have "python version 3"

```console
python3 --version
```

2. You may need to install some Python packages as pre-requisites.  Here are some:

```console
sudo pip3 install paho-mqtt
```



## Step 1:  Wire the DHT 11 Sensor to your PI

Follow the instructions here:
https://www.instructables.com/id/DHT11-Raspberry-Pi/

Some hints:
1.  You can do this with simply the DHT11 and 3 Female to Female jumper wires
2.  If you hold the raspberry pi such that the USB inputs are on the right and the Pins are on the top:
    * Wire the first pin on the bottom row to the VCC of the DHT11 - This is 3.3V power
    * Wire the second pin on the top row to the ground (GND) of the DHT11 - this is the ground 
    * Wire the third pin on the 6th pin on the bottom row to the DATA of the DHT11 - this is GPIO Pin 17

## Step 2:  Verify the DHT 11 is working properly

Run the following command to verify that you are receiving values:

```console
python dht11_example.py
```

Verify that the temperature and humidity readings are displayed.


```console
Last valid input: 2019-12-17 10:33:59.947765
Temperature: 18.3 C
Temperature: 64.9 F
Humidity: 39.0 %
```

## Step 3:  Sign up for Azure Cloud and Create an IoT Service

1. Sign up for the Azure cloud from this link: 
https://azure.microsoft.com/Account/Free

2. After you go through the registration process, login with your Microsoft Azure ID
https://portal.azure.com/#home

3. Create an instance of the IoT service by clicking "Create a Resource" and searching for IoT

4.  Select "IoT Hub" and "Create".  
    * For Subscription, it should default to your Azure Subscription
    * for Resource Group, if one does not exist, create one - call it "default"
    * For region, select the region closest to you
    * For the IoT Hub Name, pick a relatively short unique name easy to remember

5.  Next, select the "Size and Scale" to review - Select F1: Free Tier for the pricing and scaling tier.

6.  When finished, select "Review and Create", and then "Create" if everything looks OK.

7.  The deployment will begin.  Monitor the deployment page until it says "Deployment is complete" (or similar).  Click "Go to resource" to go to the new IoT Hub that you just created.

## Step 4:  Create a new Device called "pi1"

1.  Navigate to "IoT Devices" from the left hand panel.  This is located under "Explorers" sub-group.

2.  Select "New"
    * For the Device ID, select "pi1"
    * Leave all other fields as default 
    * Hit Save when complete 
**You can name it whatever you want, but the program here uses the device id  called "pi1"**

3. Your new "pi1" device should show up in the list.  Click on the new device.  Click on the "Primary Connection String" to reveal the details:
   * Take note of the hostname.  For example, if you named your IoT Hub "foo", it will be something like "foo.azure-devices.net"
   * Device ID should be "pi1" - same as what you created
   * The Primary Key will be a long token.  Copy that into an area where you can embed it into the python program

## Step 5:  Customize your Configuration Values in the Python Script

1.  Edit the program and put it in your specific credentials.  
    * Change the absolute path location of where you are running this on your PI to the certificate "baltimorebase64.cer"
    * Change the iothubname to the name of your Azure IoT hub as above
    * deviceid should be the name of the device - in this case 'pi1'
    * The username field should take the form {iothubhostname}/{deviceid}
    * The primarykey field should he the Shared Token that you copied into a text folder

```python
# device credentials
ca_absolute_path = '/home/pi/dev/iot-temp/pitemp-azureiot-basic/baltimorebase64.cer'
iothubname = 'mjrothera200'
deviceid = 'pi1'  # Azure IoT Device ID
username = 'mjrothera200.azure-devices.net/pi1'
primarykey = 'F1ewFxFWM/PytVHeGCrE2AV/6j7vlhv1QZuK8qplo5Q='

```

## Step 7:  Run the Program
 

```console
python3 iot-temp.py
```

## Step 8:  Monitor Results From the Azure IoT Command Line

1.  Install the Azure Command Line interface on another computer

2.  Login with the Command Line Tool

```console
az login
```

There is an IoT extension you need to add to the Azure CLI

```console
az extension add --name azure-cli-iot-ext
```

3.  Monitor the events

```console
az iot hub monitor-events --hub0name mjrothera200 --device-id pi1
``` 

Substitute your iot hub name and device id where appropriate.

Enjoy!

Matt Rothera


## License

This project is licensed under the terms of the MIT license.
