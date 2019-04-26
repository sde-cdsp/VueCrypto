FROM node:lts-alpine

# make the 'cryptovue' folder the current working directory
RUN mkdir /cryptovue
WORKDIR /cryptovue

# copy both 'package.json' and 'package-lock.json' in 'cryptovue' folder (if available)
COPY package*.json /cryptovue/

# install project dependencies
RUN npm install

# copy project files and folders to the current working directory (i.e. 'cryptovue' folder)
COPY . .

# build app for production with minification
#RUN npm run build