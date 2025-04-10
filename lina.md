Bienvenue sur lina

# Objectif 

Déploiement automatisé d'un cluster kubernetes avec une application test.

# Setup WSL

## config Zscaler cert

sudo apt-get update
sudo apt-get upgrade

## Requirements

wget :
sudo apt-get install wget

lsb-release : 
sudo apt-get -y install lsb-release

Vagrant : 
Objectif, configurer vagrant sur wsl
ATTENTION important, il faut que le vagrantfile soit situé sur : /mnt/c/Users/victor.marti
/mnt/c/Users/victor.marti/Documents/Code/Project/Cluster
donc pour lancer vagrant :
/mnt/c/Users/victor.marti/Documents/Code/Project/Cluster$ vagrant up

.vagrant.d/Vagrantfile
Vagrant.configure("2") do |config|
  # IP de votre machine Windows
  config.ssh.host = "  169.254.206.14"
end


.bashrc
export VAGRANT_WSL_ENABLE_WINDOWS_ACCESS="1"
export PATH="$PATH:/mnt/c/Program Files/Oracle/VirtualBox"
export VAGRANT_WSL_WINDOWS_ACCESS_USER_HOME_PATH="/mnt/c/Users/victor.marti"
export VAGRANT_HOME="$HOME/.vagrant.d"

Ansible : 
wget -O - https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install vagrant

Ansible : 
Virtualbox

## Vagrant

Déploie 1 node master et 2 node worker sur le même réseau

IP : 
master 192.168.56.2
worker1 192.168.56.3
worker2 192.168.56.4

## Ansible

Playbook permettant :

## Config certificat Zscaler
Opt. Vérification mémoire, cpu des vm

## Config Kubernetes 

###

