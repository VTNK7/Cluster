# Objectif

Créer un déploiement automatisé avec CICD

# Tools

Gitlab
Virtualbox
ansible
vagrant
kubeadm
containerd
flask/python
postgres

# Repo

nginx : déploiement nginx basique
webapp : déploiemment flask + postgress
lina : déploiement automatique flask ansible






##### autre

Tuto pour connnecter wsl au cluster kuberneters 
Le faire depuis root n'est pas pareil que depuis home/victor



root@FR-F6YYV93:/home/victor# cp /mnt/c/Users/victor.marti/.kube/config ~/.kube/
root@FR-F6YYV93:/home/victor# chmod 600 ~/.kube/config
root@FR-F6YYV93:/home/victor# kubectl get nodes
NAME      STATUS   ROLES           AGE    VERSION
master    Ready    control-plane   7d1h   v1.32.3
worker1   Ready    <none>          7d1h   v1.32.3
root@FR-F6YYV93:/home/victor# 



scp -i C:/Users/victor.marti/Documents/Code/Project/Cluster/.vagrant/machines/master/virtualbox/private_key -P 2222 vagrant@127.0.0.1:/home/vagrant/.kube/config C:\Users\victor.marti\Documents\Code\Project\Cluster\config


scp -i C:/Users/victor.marti/Documents/Code/Project/Cluster/.vagrant/machines/master/virtualbox/private_key -P 2222 vagrant@127.0.0.1:/home/vagrant/.kube/config C:\Users\victor.marti\Documents\Code\Project\Cluster\config