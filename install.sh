# MySQL setup
sudo echo "create database mypseudo" | mysql
sudo mysql mypseudo < ./install/mypseudo.sql

# Program files
sudo cp ./install/mypseudo /etc/init.d/mypseudo
sudo chmod 755 /etc/init.d/mypseudo

# Daemon setup
sudo cp -r ../mypseudo /usr/local/bin/mypseudo
sudo chmod -R 755 /etc/init.d/mypseudo
sudo update-rc.d mypseudo defaults