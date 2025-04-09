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

cd

sudo wget https://github.com/opencontainers/runc/releases/download/v1.2.6/runc.amd64
sudo wget https://github.com/opencontainers/runc/releases/download/v1.2.6/runc.sha256sum
sha256sum -c runc.sha256sum

sudo install -m 755 runc.amd64 /usr/local/sbin/runc

sudo wget https://github.com/containernetworking/plugins/releases/download/v1.6.2/cni-plugins-linux-amd64-v1.6.2.tgz
sudo wget https://github.com/containernetworking/plugins/releases/download/v1.6.2/cni-plugins-linux-amd64-v1.6.2.tgz.sha256
sha256sum -c cni-plugins-linux-amd64-v1.6.2.tgz.sha256

sudo mkdir -p /opt/cni/bin
sudo tar Cxzvf /opt/cni/bin cni-plugins-linux-amd64-v1.6.2.tgz

sudo mkdir -p /etc/containerd/
sudo sh -c 'containerd config default > /etc/containerd/config.toml'

sudo mkdir -p /usr/local/lib/systemd/system/
sudo wget -O /usr/local/lib/systemd/system/containerd.service https://raw.githubusercontent.com/containerd/containerd/main/containerd.service


sudo systemctl daemon-reload
sudo systemctl enable --now containerd

sudo systemctl status

#### Install Kubeadm kubelet kubectl
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl gpg
sudo curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.32/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg

sudo echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.32/deb/ /' | sudo tee /etc/apt/sources.list.d/kubernetes.list

sudo apt-get update
sudo apt-get install -y kubelet kubeadm kubectl
sudo apt-mark hold kubelet kubeadm kubectl

sudo systemctl enable --now kubelet

#### Network setup
Rien compris

#### Control plane

sudo kubeadm init --apiserver-advertise-address=192.168.56.2 --pod-network-cidr=10.244.0.0/16

mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config

kubectl apply -f https://docs.projectcalico.org/manifests/calico.yaml
Bien attendre que ce soit running
watch kubectl get pods --all-namespaces   

(au fait j'ai mis 4 go de ram dans le doute)

#### Data plane

kubeadm join 192.168.56.2:6443 --token pp8qs7.25m51ud7orb8kv1u \
        --discovery-token-ca-cert-hash sha256:449bb2fc16eceb34df778806f8e06363ad5dcb5d3a32f73d8124c03d8d5c2713 

attendre que ca marche
kubectl get pods -n kube-system
kubectl get nodes

sudo journalctl -u containerd
sudo journalctl -u kubelet

Cette config fonctionne

Tester avec nginx
kubectl create deployment nginx --image=nginx

kubectl expose deployment nginx --type=NodePort --port=80

kubectl get services


#### pour arreter le cluster

kubectl get all --all-namespaces -o yaml > all-resources.yaml
kubectl delete all --all --namespace=<namespace>  # Supprimer tous les objets dans un namespace particulier
kubectl cluster-info


#### Pour utiliser kubectl depuis l'hôte windows

scp master:/etc/kubernetes/admin.conf C:\Users\victor.marti\.kube\config

On peut mtn utiliser kubeclt sur windows

# prompt
J'ai déployé un cluster kubernetes avec kubeadm.
Il est construit avec une node master et une node worker.

Je souhaite déployer une image que j'ai construite dessus.
L'image que je souhaite déployer est une image nginx qui affiche son adresse, son nom sur le web.

Quel docker file dois je faire pour créer cette image


PS C:\> Expand-Archive C:\Users\victor.marti\Downloads\docker-28.0.4.zip -DestinationPath $Env:ProgramFiles


#### Docker wsl
Finalement j'utilse debian avec wsl pour utiliser docker plus facilement
sudo apt update
sudo apt install -y kubectl


wsl --install
wsl --list --online        # Liste les distributions disponibles
wsl --install -d Debian    # Installe une distribution spécifique


Configuration wsl c'est partit.

on ajouter zscaler.crt

technique secrete :

Sauron a permis a ma machine de se connecter a internet (zscaler était désactivé)
J'ai donc installer openssl et update-ca-certificate, je vais mtn tenter de régler le certificat
ca marche ;)
nvm j'avais pas connecté zscaler

j'installe docker



lancement du cluster avec nginx : 

vagrant up
kubectl get nodes
kubectl get pods --all-namespaces
kubectl create deployment my-dep --image=victormarti/cluster:v1.0
kubectl get deployments
kubectl expose deployment my-dep --type=NodePort --port=80
kubectl get services

on a bien le container affiché avec le bon nom et la bonne ip
kubectl get pods -o wide


A faire  : 
ajouter une bdd postgress sql 
et un loadbalancer (ingress postgress jsp)
bidouiller


pour stopper les vm
vagrant halt


Nouveau déploiement :
192.168.56.2:31331
http://192.168.56.2:80
10.0.2.15:31331

Je fais un déploiement avec un ingress controller.

kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.12.1/deploy/static/provider/cloud/deploy.yaml


kubectl get pods --all-namespaces


kubectl apply -f nginx-deployment.yaml

kubectl get deployments
kubectl get pods

kubectl apply -f nginx-ingress.yaml

kubectl get svc
kubectl describe svc nginx-service

kubectl apply -f nginx-service.yaml

kubectl get ingress

Pour tester
Rester appuyé sur ctrl r pour spam sur edge
C'est con mais ca marche

OBjectif afficher une bdd commune entre les containre
qui affiche le nombre de requetes a chaque container par ex.


pour le python
https://claude.site/artifacts/fb62b4a1-e4b9-4fe8-9d51-af778a771e4d

http://192.168.56.2:30161


kubectl apply -f postgres.yaml
kubectl apply -f webapp.yaml



kubectl delete -f webapp.yaml  
kubectl delete -f postgres.yaml


kubectl get pv,pvc,pods,statefulset

probleme je dois préciser un path sur le node worker qui est lié au pod postgres.

sur le node worker :

mkdir postgres-data
chmod -R 777 /data/postgres-data
