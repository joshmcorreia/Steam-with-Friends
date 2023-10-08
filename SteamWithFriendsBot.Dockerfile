# To build this Dockerfile, run the following command:
# docker build -t steam_with_friends_bot -f SteamWithFriendsBot.Dockerfile .

# To run this docker container run the following command:
# docker run -i --name steam_with_friends_bot -v $(pwd):/home/root/steam-with-friends -t steam_with_friends_bot

FROM ubuntu:jammy

ENV DEBIAN_FRONTEND=noninteractive

# Dependency breakdown:
# git - to pull code updates from my git repo
# python3 - to run the application
# python3-pip - to install python3 libraries

RUN apt-get -y update && apt-get install -y git python3 python3-pip

RUN mkdir /home/root
WORKDIR /home/root

# RUN pip3 install -r pip_dependencies.txt

# TODO: Change this dockerfile to use a Python image so it's more lightweight
