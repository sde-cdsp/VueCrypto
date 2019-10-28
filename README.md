# My crypto list
Experimental project with Django as a backend and VueJS as a frontend.
## Prerequisites
### Docker installation
This project is made to work with [Docker](https://docs.docker.com/install/linux/docker-ce/ubuntu/).

### Project configuration
#### Database setup
A *variables.samples.env* file is provided. 
You can set the database variables as you wish and put them in a *variables.env* file, which will be used by the dockrun script.

#### Other configs

A *configs.sample.py* file is provided. You must set the provided variables for several features to work (such as getting a coinmarketcap API key).
When this is done, copy them in a *configs.py* file.


## Create the docker images
Generate the django and vue images
```
./dockbuild.sh && cd mycryptolist && ./dockbuild.sh
```

## Run the app
The app will run after the containers are loaded. It might take a little while at first launch to install all required packages and retrieve the postgres database image.
```
./dockrun.sh
```
You can then visit **localhost:8000**
