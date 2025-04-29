from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = 'votre_cle_secrete'

# Configuration MongoDB
client = MongoClient('mongodb://127.0.0.1:27017/')
db = client['traffic_db']
collection = db['traffic_data']

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Aucun fichier sélectionné', 'error')
            return redirect(request.url)
        
        file = request.files['file']
        
        if file.filename == '':
            flash('Aucun fichier sélectionné', 'error')
            return redirect(request.url)
        
        if file and file.filename.endswith('.xlsx'):
            try:
                filepath = os.path.join('uploads', file.filename)
                file.save(filepath)
                process_excel(filepath)
                flash('Fichier importé avec succès!', 'success')
            except Exception as e:
                flash(f'Erreur lors de l\'import: {str(e)}', 'error')
    
    # Récupérer les données pour affichage
    data = list(collection.find().limit(50))  # Limite à 50 documents pour l'affichage
    return render_template('index.html', traffic_data=data)

def process_excel(filepath):
    df = pd.read_excel(filepath)
    df = df.where(pd.notnull(df), None)
    
    grouped = df.groupby(['count_point_id', 'direction_of_travel'])
    
    documents = []
    for (count_point_id, direction), group in grouped:
        doc = {
            'count_point_id': int(count_point_id),
            'direction_of_travel': direction,
            'region_name': group['region_name'].iloc[0],
            'local_authority_name': group['local_authority_name'].iloc[0],
            'location': {
                'latitude': float(group['latitude'].iloc[0]),
                'longitude': float(group['longitude'].iloc[0])
            },
            'road': {
                'name': group['road_name'].iloc[0],
                'type': group['road_type'].iloc[0],
                'start_junction_road_name': group['start_junction_road_name'].iloc[0],
                'end_junction_road_name': group['end_junction_road_name'].iloc[0]
            },
            'measures': []
        }
        
        for _, row in group.iterrows():
            measure = {
                'count_date': str(row['count_date'].date()) if pd.notnull(row['count_date']) else None,
                'hour': int(row['hour']) if pd.notnull(row['hour']) else None,
                'cars_and_taxis': float(row['cars_and_taxis']) if pd.notnull(row['cars_and_taxis']) else 0,
                'buses_and_coaches': float(row['buses_and_coaches']) if pd.notnull(row['buses_and_coaches']) else 0,
                'lgvs': float(row['lgvs']) if pd.notnull(row['lgvs']) else 0,
                'pedal_cycles': float(row['pedal_cycles']) if pd.notnull(row['pedal_cycles']) else 0
            }
            doc['measures'].append(measure)
        
        documents.append(doc)
    
    if documents:
        collection.insert_many(documents)

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True, port=5000)