# mycryptolist

## Prerequisites: Docker installation
This project is made to work with [Docker](https://docs.docker.com/install/linux/docker-ce/ubuntu/).  


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

### Run the app
The app will run after the containers are loaded. It might take a little while at first launch to install all required packages and retrieve the postgres database image.
```
./dockrun.sh
```
You can then visit **localhost:8000**
