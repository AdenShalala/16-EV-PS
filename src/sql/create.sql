CREATE TABLE IF NOT EXISTS Session (
    session_id VARCHAR(50) PRIMARY KEY,
    id VARCHAR(50) NOT NULL,
    account_type VARCHAR(50) NOT NULL,
    secret_hash BLOB NOT NULL,
    created_at TIMESTAMP NOT NULL,
    last_verified_at TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS Admin (
    admin_id VARCHAR(50) PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS Clinician (
    clinician_id   VARCHAR(50)  PRIMARY KEY,
    first_name           VARCHAR(100) NOT NULL,
    last_name            VARCHAR(100) NOT NULL,
    email          VARCHAR(100) NOT NULL UNIQUE,
    password  VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS Patient (
    patient_id VARCHAR(50) PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    height VARCHAR(10),
    weight VARCHAR(10),
    amputation_type VARCHAR(50),
    prosthetic_type VARCHAR(50),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(255),
    user_id VARCHAR(50),
    clinician_id VARCHAR(50),
    FOREIGN KEY (clinician_id) REFERENCES Clinician(clinician_id)
);

CREATE TABLE IF NOT EXISTS Activity (
    activity_id VARCHAR(50) PRIMARY KEY,
    activity_type VARCHAR(20),
    start_time BIGINT,
    end_time BIGINT,
    is_uploaded BOOLEAN DEFAULT TRUE,
    patient_id VARCHAR(50),
    FOREIGN KEY (patient_id) REFERENCES Patient(patient_id)
);



CREATE TABLE IF NOT EXISTS Sensor (
    sensor_id VARCHAR(50) PRIMARY KEY,
    patient_id VARCHAR(50),

    sensor_type INT,
    location_name VARCHAR(50),
    location_id INT,
    sensor_location_id VARCHAR(50) UNIQUE,
    
    is_connected BOOLEAN DEFAULT TRUE,
    
    FOREIGN KEY (patient_id) REFERENCES Patient(patient_id)
);

CREATE TABLE IF NOT EXISTS PressureReading (
    pressure_reading_id VARCHAR(50) PRIMARY KEY,
    pressure_value DECIMAL(10, 2),
    time BIGINT,
    sensor_type INT,
    is_uploaded BOOLEAN DEFAULT TRUE,
    reading_series_id VARCHAR(50) UNIQUE,
    activity_id VARCHAR(50),
    sensor_id VARCHAR(50),
    FOREIGN KEY (activity_id) REFERENCES Activity(activity_id),
    FOREIGN KEY (sensor_id) REFERENCES Sensor(sensor_id)
);

CREATE TABLE IF NOT EXISTS ActivityReading (
    activity_id VARCHAR(50),
    reading_series_id VARCHAR(50),
    sensor_id VARCHAR(50),
    FOREIGN KEY (activity_id) REFERENCES Activity(activity_id),
    FOREIGN KEY (reading_series_id) REFERENCES PressureReading(reading_series_id),
    FOREIGN KEY (sensor_id) REFERENCES Sensor(sensor_id)
);