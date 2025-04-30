# 🚦 Projet Traffic - Analyse de Données de Circulation
 
## 📦 Prérequis & Installation

### Dépendances nécessaires
```bash
# Installation des modules Python
pip install mysql-connector-python pandas matplotlib

# Pour Linux/Mac
pip3 install mysql-connector-python pandas matplotlib

# 🖥 Configuration de l'Environnement
# 1. Machine Virtuelle Vagrant
vagrant up       # Démarre la VM
vagrant ssh      # Se connecter à la VM
vagrant halt     # Arrêter la VM

# 2. Configuration MySQL
# 2.1.Créez la base de données :
CREATE DATABASE traffic_db;

# 2.2.Exécutez les scripts :
mysql -u username -p traffic_db < tables/structures.sql

# Lancement de l'Application
python app.py 

# 📊 Structure Principale - Table counts
Colonne	Type	Description	Unité
id (PK, AI)	INT	ID unique du comptage	-
count_point_id	INT	Référence point de comptage	-
count_date	DATE	Date du relevé	-
hour	INT	Heure (0-23)	h
link_length_km	FLOAT	Longueur de section	km
pedal_cycles	INT	Nombre de vélos	u
cars_and_taxis	FLOAT	Voitures et taxis	u
all_hgvs	FLOAT	Total poids lourds	u
all_motor_vehicles	FLOAT	Total véhicules motorisés	u
PK = Primary Key, AI = Auto-Increment

# Importation
Veuillez utiliser le fichier d'import 'traffic_2019_clean.csv'