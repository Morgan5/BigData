const express = require('express');
const cassandra = require('cassandra-driver');
const csv = require('csv-parser');
const multer = require('multer');
const { v4: uuidv4 } = require('uuid');

const app = express();
const PORT = 3000;

const client = new cassandra.Client({
  contactPoints: ['127.0.0.1'],
  localDataCenter: 'datacenter1',
  keyspace: 'traffic'
});

// Configuration de multer pour gérer l'upload de fichiers
const storage = multer.memoryStorage(); // Stocker le fichier en mémoire
const upload = multer({ storage: storage });

app.use(express.static('public'));

app.post('/import', upload.single('file'), async (req, res) => {
  if (!req.file) {
    return res.status(400).send('Aucun fichier n\'a été envoyé.');
  }

  // Récupérer le fichier CSV envoyé dans le body
  const fileBuffer = req.file.buffer;
  const records = [];

  // Lire et traiter le fichier CSV depuis le buffer en mémoire
  const readableStream = require('stream').Readable.from(fileBuffer);
  readableStream
    .pipe(csv())
    .on('data', (row) => {
      // Convertir les valeurs du CSV pour correspondre aux types de la table
      const record = {
        count_point_id: row.count_point_id,
        direction_of_travel: row.direction_of_travel,
        year: parseInt(row.year),
        count_date: row.count_date, // Assurez-vous que le format de la date est correct
        hour: parseInt(row.hour),
        region_id: parseInt(row.region_id),
        region_name: row.region_name,
        local_authority_id: parseInt(row.local_authority_id),
        local_authority_name: row.local_authority_name,
        road_name: row.road_name,
        road_type: row.road_type,
        start_junction_road_name: row.start_junction_road_name,
        end_junction_road_name: row.end_junction_road_name,
        easting: parseFloat(row.easting),
        northing: parseFloat(row.northing),
        latitude: parseFloat(row.latitude),
        longitude: parseFloat(row.longitude),
        link_length_km: parseFloat(row.link_length_km),
        link_length_miles: parseFloat(row.link_length_miles),
        pedal_cycles: parseInt(row.pedal_cycles),
        two_wheeled_motor_vehicles: parseInt(row.two_wheeled_motor_vehicles),
        cars_and_taxis: parseInt(row.cars_and_taxis),
        buses_and_coaches: parseInt(row.buses_and_coaches),
        lgvs: parseInt(row.lgvs),
        hgvs_2_rigid_axle: parseInt(row.hgvs_2_rigid_axle),
        hgvs_3_rigid_axle: parseInt(row.hgvs_3_rigid_axle),
        hgvs_4_or_more_rigid_axle: parseInt(row.hgvs_4_or_more_rigid_axle),
        hgvs_3_or_4_articulated_axle: parseInt(row.hgvs_3_or_4_articulated_axle),
        hgvs_5_articulated_axle: parseInt(row.hgvs_5_articulated_axle),
        hgvs_6_articulated_axle: parseInt(row.hgvs_6_articulated_axle),
        all_hgvs: parseInt(row.all_hgvs),
        all_motor_vehicles: parseInt(row.all_motor_vehicles)
      };
      records.push(record);
    })
    .on('end', async () => {
      try {
        const insertQuery = `
            INSERT INTO traffic_data (
            count_point_id, direction_of_travel, year, count_date, hour, region_id, region_name,
            local_authority_id, local_authority_name, road_name, road_type, start_junction_road_name,
            end_junction_road_name, easting, northing, latitude, longitude, link_length_km, link_length_miles,
            pedal_cycles, two_wheeled_motor_vehicles, cars_and_taxis, buses_and_coaches, lgvs,
            hgvs_2_rigid_axle, hgvs_3_rigid_axle, hgvs_4_or_more_rigid_axle, hgvs_3_or_4_articulated_axle,
            hgvs_5_articulated_axle, hgvs_6_articulated_axle, all_hgvs, all_motor_vehicles
          ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?,?)
        `;

        // Insérer les enregistrements dans la base de données
        for (const record of records) {
          await client.execute(insertQuery, [
            record.count_point_id, record.direction_of_travel, record.year, record.count_date, record.hour,
            record.region_id, record.region_name, record.local_authority_id, record.local_authority_name,
            record.road_name, record.road_type, record.start_junction_road_name, record.end_junction_road_name,
            record.easting, record.northing, record.latitude, record.longitude, record.link_length_km,
            record.link_length_miles, record.pedal_cycles, record.two_wheeled_motor_vehicles, record.cars_and_taxis,
            record.buses_and_coaches, record.lgvs, record.hgvs_2_rigid_axle, record.hgvs_3_rigid_axle,
            record.hgvs_4_or_more_rigid_axle, record.hgvs_3_or_4_articulated_axle, record.hgvs_5_articulated_axle,
            record.hgvs_6_articulated_axle, record.all_hgvs, record.all_motor_vehicles
          ], { prepare: true });
        }

        res.send('Import terminé avec succès ✅');
      } catch (err) {
        console.error('Erreur lors de l\'importation :', err);
        res.status(500).send('Erreur serveur ❌');
      }
    });
});

// Tester la connexion Cassandra
client.connect()
  .then(() => {
    console.log('Connecté à Cassandra avec succès !');
})
  .catch(err => {
    console.error('Erreur de connexion Cassandra :', err);
  });

// Démarrer le serveur Express
app.listen(PORT, () => {
  console.log(`Serveur démarré sur http://localhost:${PORT}`);
});
