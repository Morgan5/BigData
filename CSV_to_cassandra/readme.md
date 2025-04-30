<!-- 1 ouvrir le fichier - Vagrantfile et ajouter la ligne en bas des autres config.vm.network-->
config.vm.network "forwarded_port", guest: 9042, host: 9042
<!-- 2 Recharger vagrant -->
vagrant reload
<!-- 3 Se connecter -->
vagrant ssh
<!-- 4- ouvrir le fichier cassandra.yaml-->
sudo nano /opt/cassandra/conf/cassandra.yaml
<!-- 5- Modifier les lignes suivant -->
    listen_address: 127.0.0.1
    rpc_address: 0.0.0.0
    broadcast_rpc_address: 127.0.0.1
<!-- 6- Redemarrer cassandra -->
/opt/cassandra/bin/cassandra -R
<!-- 7- Verifier son status -->
/opt/cassandra/bin/nodetool status
<!-- Acces a cqlsh (cassandra cli) -->
/opt/cassandra/bin/cqlsh
