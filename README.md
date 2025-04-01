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


## when vagrant/virtual box vm are configured (zscaler)

## Kubernetes installation

### Master & Worker

#### Disable Swap
sudo swapoff -a

To disable swap, sudo swapoff -a can be used to disable swapping temporarily. To make this change persistent across reboots, make sure swap is disabled in config files like /etc/fstab, systemd.swap, depending how it was configured on your system

#### Enable ipv4 packet forwarding

cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.ipv4.ip_forward = 1
EOF

sudo sysctl --system

#### Install container runtime : containerd

cd /usr/local
sudo wget https://github.com/containerd/containerd/releases/download/v2.0.0/containerd-2.0.0-linux-amd64.tar.gz

sudo tar Cxzvf /usr/local containerd-2.0.0-linux-amd64.tar.gz

continuer ici.

sudo wget https://github.com/opencontainers/runc/releases/download/v1.2.6/runc.amd64
sudo wget https://github.com/opencontainers/runc/releases/download/v1.2.6/runc.sha256sum
sha256sum -c runc.sha256sum

cd
