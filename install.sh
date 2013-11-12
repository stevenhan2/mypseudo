sudo mysql -uroot -e "create database 'mypseudo'"
sudo mysql mypseudo < ./install/mypseudo.sql
sudo cp ./install/mypseudo /etc/init.d/mypseudo
sudo chmod 755 /etc/init.d/mypseudo
sudo cp -r ../mypseudo /usr/local/bin/mypseudo
sudo chmod -R 755 /etc/init.d/mypseudo
sudo update-rc.d mypseudo defaults