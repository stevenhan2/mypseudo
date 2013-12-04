#! /bin/sh

# MySQL setup
sudo echo "create database mypseudo" | mysql -p
sudo mysql -p mypseudo < ./install/mypseudo.sql

# Remove previous install (preserve config)
sudo cp /usr/local/bin/mypseudo/config.json ../mypseudo/config.json
sudo rm -rf /etc/init.d/mypseudo /usr/local/bin/mypseudo

# Program files
sudo cp ./install/mypseudo /etc/init.d/mypseudo
sudo chmod 755 /etc/init.d/mypseudo

# Daemon setup
sudo cp -r ../mypseudo /usr/local/bin/mypseudo
sudo chmod -R 755 /usr/local/bin/mypseudo
sudo update-rc.d mypseudo defaults