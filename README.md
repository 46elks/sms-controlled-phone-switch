# [DEMO] SMS controlled telephony switch
This is a example of how you can build a telephony switch where you can configure who gets incoming calls via SMS


## Requirements

 - A [46elks account](https://46elks.com/register)
 - 2 virtual numbers from 46elks
   - One that your customers will call
   - One used for controlling the system (could technically be the same as the first one, but that would cause incoming messages from your customers to be parsed as commands)

## Setup

### Configure server

 - Copy config.toml.sample to config.toml
 - Edit the config to correspond with your system setup
   - The ```host``` value can be left as is
   - The ```port``` value needs to be unlocked for incoming traffic in your firewall and be accessable from the internet
   - ```base_url``` needs to be set to the URL where this server can be reached on. For example yourdomain.com.
   - The ```static_dir``` parameter should be set to a absolute path instead of a relative one


### Configure the numbers
The virtual numbers can be configure on the 46elks.com dashboard or directly via the API. See our documentation for more details [https://46elks.com/docs/configure-number](https://46elks.com/docs/configure-number)

#### Configure voice_start on the main virtual number
Should be set to f"{base_url}:{port}/incoming_calls"

Ex if your base_url is http://yourdomain.com and the port is 8080

voice_start -> http://yourdomain.com:8080/incoming_calls

#### Configure sms_url on the controll number
Should be set to f"{base_url}:{port}/incoming_sms"

Ex if your base_url is http://yourdomain.com and the port is 8080

sms_url -> http://yourdomain.com:8080/incoming_sms

### Installing pip packages

#### Using a virtual environment
It is a good idea to install python dependencies in a virtualenv. This isolates the packages from the rest of your system packages.

##### Installing virtualenv with pip

```
pip3 install virtualenv
```

##### Create a virtual environment:
```
virtualenv env
```
##### Enter the virtual environment
```
source env/bin/activate
```

#### Installing required packages:
```
pip intall -r requirements.txt
```

### Running the server
For production environments the server should be ran using a more stable web server than the built in dev server, for example waitress or gunicorn. But for demo and development purpses the dev server works fine.

The server can be started with:
```
python3 sms-switch.py
```

### Adding users
Copy ```users.json.sample``` to ```users.json``` and add the users that are allowed to controll the server

## Using the demo

Commands can be sent in text messages to the controll number

### Commands
 - set [name] - sets [name] as the active user that will receive calls
 - who - Replies with the name of the active user
 - disable - removes the active user, disabling call forwards
