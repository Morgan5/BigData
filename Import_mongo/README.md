# Démarrage et Configuration du Projet Traffic

Ce projet utilise une machine virtuelle Vagrant pour héberger une base de données MongoDB et exécuter une application Python. Voici les étapes pour le démarrer correctement.


## 🚀 Lancer la machine virtuelle

```bash
vagrant up       # Démarrage de la VM
vagrant ssh      # Connexion à la VM
```

---

## ⚙️ Configuration de MongoDB

1. Ouvrir le fichier de configuration :
   ```bash
   sudo nano /etc/mongod.conf
   ```

2. Ajouter ou modifier les lignes suivantes :
   ```yaml
   net:
     port: 27017
     bindIp: 0.0.0.0
   ```

3. Redémarrer MongoDB pour appliquer les changements :
   ```bash
   sudo systemctl restart mongod
   ```

---

## 🗃️ Se connecter à MongoDB

```bash
mongo
```

---

## ▶️ Lancer l'application

Dans le dossier du projet, exécutez :

```bash
python app.py
```

---

## 📁 Données

Après l'importation du fichier :

- **Base de données** : `traffic_db`
- **Collection** : `traffic_data`
