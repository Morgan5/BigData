from flask import Flask, request, redirect, render_template, flash
import mysql.connector
import csv
import io

app = Flask(__name__)
app.secret_key = 'votre_cle_secrete'  # Pour les messages flash

# Configuration base de données
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'magento',
    'database': 'traffic_db'
}


#@app.route('/')
#def index():
#    rows = fetch_recent_rows()
#    return render_template('index.html', rows=rows)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Aucun fichier envoyé.')
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            flash('Fichier non sélectionné.')
            return redirect(request.url)

        if file:
            try:
                stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
                csv_input = csv.DictReader(stream)
                process_csv(csv_input)
                flash("Données insérées avec succès.")
            except Exception as e:
                flash(f"Erreur lors de l'insertion : {e}")
            return redirect('/')
    
    rows = fetch_recent_rows()
    return render_template('index.html', traffic_data=rows)

def process_csv(csv_input):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    for row in csv_input:
        # Regions
        cursor.execute("""
            INSERT IGNORE INTO regions (id, name) VALUES (%s, %s)
        """, (int(row['region_id']), row['region_name']))

        # Local Authorities
        cursor.execute("""
            INSERT IGNORE INTO local_authorities (id, name, region_id) VALUES (%s, %s, %s)
        """, (int(row['local_authority_id']), row['local_authority_name'], int(row['region_id'])))

        # Roads
        cursor.execute("""
            INSERT IGNORE INTO roads (id, name, type) VALUES (%s, %s, %s)
        """, (row['road_name'], row['road_name'], row['road_type']))

        # Count Points
        cursor.execute("""
            INSERT IGNORE INTO count_points (
                id, road_id, direction_of_travel, start_junction_road_name, end_junction_road_name,
                easting, northing, latitude, longitude
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            int(row['count_point_id']), row['road_name'], row['direction_of_travel'],
            row['start_junction_road_name'], row['end_junction_road_name'],
            int(row['easting']), int(row['northing']),
            float(row['latitude']), float(row['longitude'])
        ))

        # Traffic Counts
        cursor.execute("""
            INSERT INTO traffic_counts (
                count_point_id, count_date, hour, link_length_km, link_length_miles,
                pedal_cycles, two_wheeled_motor_vehicles, cars_and_taxis, buses_and_coaches,
                lgvs, hgvs_2_rigid_axle, hgvs_3_rigid_axle, hgvs_4_or_more_rigid_axle,
                hgvs_3_or_4_articulated_axle, hgvs_5_articulated_axle, hgvs_6_articulated_axle,
                all_hgvs, all_motor_vehicles
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            int(row['count_point_id']),
            row['count_date'],
            int(row['hour']),
            float(row['link_length_km']),
            float(row['link_length_miles']),
            int(row['pedal_cycles']),
            int(row['two_wheeled_motor_vehicles']),
            float(row['cars_and_taxis']),
            float(row['buses_and_coaches']),
            int(row['lgvs']),
            float(row['hgvs_2_rigid_axle']),
            float(row['hgvs_3_rigid_axle']),
            float(row['hgvs_4_or_more_rigid_axle']),
            float(row['hgvs_3_or_4_articulated_axle']),
            float(row['hgvs_5_articulated_axle']),
            float(row['hgvs_6_articulated_axle']),
            float(row['all_hgvs']),
            float(row['all_motor_vehicles'])
        ))

    conn.commit()
    cursor.close()
    conn.close()


def fetch_recent_rows_old(limit=10):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT tc.id, tc.count_point_id, tc.count_date, tc.hour, r.name AS region, la.name AS authority, 
               cp.road_id, cp.latitude, cp.longitude, tc.all_motor_vehicles
        FROM traffic_counts tc
        JOIN count_points cp ON tc.count_point_id = cp.id
        JOIN roads rd ON cp.road_id = rd.id
        JOIN local_authorities la ON la.id = (
            SELECT local_authority_id 
            FROM local_authorities 
            WHERE region_id = (
                SELECT region_id 
                FROM local_authorities 
                WHERE id = la.id
            ) LIMIT 1
        )
        JOIN regions r ON la.region_id = r.id
        ORDER BY tc.id DESC
        LIMIT %s
    """, (limit,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def fetch_recent_rows(limit=10):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT t.id, t.count_date, t.hour, t.cars_and_taxis, t.buses_and_coaches,
               t.pedal_cycles, cp.direction_of_travel, r.name as road_name,
               la.name as authority_name, rg.name as region_name
        FROM traffic_counts t
        JOIN count_points cp ON t.count_point_id = cp.id
        JOIN roads r ON cp.road_id = r.id
        JOIN local_authorities la ON la.id = cp.id
        JOIN regions rg ON la.region_id = rg.id
        ORDER BY t.count_date DESC
        LIMIT %s
    """, (limit,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


if __name__ == '__main__':
    app.run(port=5001)
    app.run(debug=True)
