CREATE TABLE regions (
    id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE local_authorities (
    id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    region_id INT,
    FOREIGN KEY (region_id) REFERENCES regions(id)
);

CREATE TABLE roads (
    id VARCHAR(10) PRIMARY KEY,
    name VARCHAR(20) NOT NULL,
    type VARCHAR(50)
);

CREATE TABLE count_points (
    id INT PRIMARY KEY,
    road_id VARCHAR(10),
    direction_of_travel VARCHAR(10),
    start_junction_road_name VARCHAR(50),
    end_junction_road_name VARCHAR(50),
    easting INT,
    northing INT,
    latitude DECIMAL(10,6),
    longitude DECIMAL(10,6),
    FOREIGN KEY (road_id) REFERENCES roads(id)
);

CREATE TABLE traffic_counts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    count_point_id INT,
    count_date DATE,
    hour INT,
    link_length_km FLOAT,
    link_length_miles FLOAT,
    pedal_cycles INT,
    two_wheeled_motor_vehicles INT,
    cars_and_taxis FLOAT,
    buses_and_coaches FLOAT,
    lgvs INT,
    hgvs_2_rigid_axle FLOAT,
    hgvs_3_rigid_axle FLOAT,
    hgvs_4_or_more_rigid_axle FLOAT,
    hgvs_3_or_4_articulated_axle FLOAT,
    hgvs_5_articulated_axle FLOAT,
    hgvs_6_articulated_axle FLOAT,
    all_hgvs FLOAT,
    all_motor_vehicles FLOAT,
    FOREIGN KEY (count_point_id) REFERENCES count_points(id)
);
