# My crypto list
Experimental project with Django as a backend and VueJS as a frontend.
## Prerequisites
### Docker installation
This project is made to work with [Docker](https://docs.docker.com/install/linux/docker-ce/ubuntu/).

### Project configuration
#### Database setup
You can set the database variables as you wish in the *variables.env* file.

#### Other configs

A *configs.sample.py* file is provided. You must set the provided variables for several features to work.  
When this is done, rename this file as *configs.py*


## Create the docker images
Generate the vue app image:
```
cd mycryptolist
./dockbuild.sh
```
Generate the django app image:
```
cd ..
./dockbuild.sh
```

## Run the app
The app will run after the containers are loaded. It might take a little while at first launch to install all required packages and retrieve the postgres database image.
```
./dockrun.sh
```
You can then visit **localhost:8000**
