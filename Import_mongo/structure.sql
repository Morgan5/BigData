-- This SQL script is used to create a database for road traffic data in the UK.
-- The database contains information about traffic counts, locations, and measures.
--traffic_data (db: traffic_db)
{
  "count_point_id": 52,
  "direction_of_travel": "E",
  "region_name": "South West",
  "local_authority_name": "Isles of Scilly",
  "location": {
    "latitude": 49.9142,
    "longitude": -6.2918
  },
  "road": {
    "name": "A3112",
    "type": "A Road",
    "start_junction_road_name": "X Street",
    "end_junction_road_name": "Y Avenue"
  },
  "measures": [
    {"count_date": "2019-09-06", "hour": 17, "cars_and_taxis": 20, "buses_and_coaches": 0, "lgvs": 8, "pedal_cycles": 6},
    {"count_date": "2019-09-06", "hour": 18, "cars_and_taxis": 25, "buses_and_coaches": 1, "lgvs": 10, "pedal_cycles": 9}
    ...
  ]
}