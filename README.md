# Cluster
Kubernetes cluster using virtualbox, vagrant, kubeadm

# Install
Installer virtualbox
Installer vagrant

Pour créer les vm avec vagrant sur virtualbox :
vagrant up

Pour se connecter aux vm :
vagrant ssh nomvm

Faire le script de paul pour le certificat ssl/tls

Copier le certificat zscaler.cer et le script zscaler_setup.sh sur les machines dans home/vagrant

chmod +x ./zscaler_setup.sh
./zscaler_setup.sh

### Debian 
sudo
apt update
apt install 
apt list
   
### Requirements 

To follow this guide, you need:
* One or more machines running a deb/rpm-compatible Linux OS; for example: Ubuntu or CentOS.
* 2 GiB or more of RAM per machine--any less leaves little room for your apps.
* At least 2 CPUs on the machine that you use as a control-plane node.
* Full network connectivity among all machines in the cluster. You can use either a public or a private network

Commands: 

Pour voir combien de cpu disponible
lscpu

Pour vérifier la ram disponible
free -h

Pour vérifier l'espace disque
df -h