#!/bin/bash

echo "Atualizando a máquina.."
apt-get update
apt-get upgrade -y

echo "Instalando os módulos.."
sudo apt-get install apache2 -y
sudo apt-get install unzip -y

echo "Acessando e baixando projeto na pasta tmp.."
cd /tmp
wget https://github.com/denilsonbonatti/linux-site-dio/archive/refs/heads/main.zip

echo "Fazendo o unzip do arquivo.."
unzip main.zip

echo "Acessando pasta deszipada.."
cd linux-site-dio-main

echo "Copiando o arquivo para o destino.."
sudo cp -R * /var/www/html/

