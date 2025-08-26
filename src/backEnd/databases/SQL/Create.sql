CREATE TABLE IF NOT EXISTS 'Admin' (
    admin_id VARCHAR(50) PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS Clinician (
    clinician_id   VARCHAR(50)  PRIMARY KEY,
    first_name           VARCHAR(100) NOT NULL,
    last_name            VARCHAR(100) NOT NULL,
    email          VARCHAR(100) NOT NULL,
    password_hash  VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS Patient (
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    height VARCHAR(10),
    weight VARCHAR(10),
    amputation_type VARCHAR(50),
    prosthetic_type VARCHAR(50),
    email VARCHAR(100),
    password_hash VARCHAR(255),
    patient_id VARCHAR(50) PRIMARY KEY,
    user_id VARCHAR(50),
    clinician_id VARCHAR(50),
    FOREIGN KEY (clinician_id) REFERENCES Clinician(clinician_id)
);

-- CREATE TABLE Activity (
-- 	activity_id VARCHAR(50) PRIMARY KEY,
--     patient_id VARCHAR(50),
--     end_time VARCHAR(30),
--     start_time VARCHAR(30),
--     activity_type VARCHAR(20),
--     FOREIGN KEY (patient_id) REFERENCES Patient (patient_id)
-- );

CREATE TABLE IF NOT EXISTS Activity (
	activity_type VARCHAR(20) PRIMARY KEY,
    start_time BIGINT,
    end_time BIGINT,
    is_uploaded BOOLEAN DEFAULT TRUE,
    patient_id VARCHAR(50),
    activity_id VARCHAR(50) PRIMARY KEY,
    FOREIGN KEY (patient_id) REFERENCES Patient (patient_id)
);

-- CREATE TABLE Sensor (
-- 	sensor_id VARCHAR(50) PRIMARY KEY,
--     activity_id VARCHAR(50),
--     location VARCHAR(60),
--     sensor_type VARCHAR(20),
--     pressure_tolerance VARCHAR(30),
--     FOREIGN KEY (activity_id) REFERENCES Activity (activity_id)
-- );

CREATE TABLE IF NOT EXISTS Sensor (
    location_name VARCHAR(50),
    sensor_location_id VARCHAR(50) PRIMARY KEY,
    type INT,
    is_connected BOOLEAN DEFAULT TRUE,
    patient_email VARCHAR(100),
    location_id INT,
    pressure_sensor_id VARCHAR(50),
    FOREIGN KEY (pressure_sensor_id) REFERENCES Sensor(sensor_id),
    FOREIGN KEY (patient_email) REFERENCES Patient(email)
);

CREATE TABLE IF NOT EXISTS PressureReading (
    pressure_value DECIMAL(10, 2),
    time BIGINT,
    sensor_type INT,
    is_uploaded BOOLEAN DEFAULT TRUE,
    activity_id VARCHAR(50),
    sensor_location_id VARCHAR(50),
    pressure_sensor_id VARCHAR(50),
    pressure_reading_id VARCHAR(50) PRIMARY KEY,
    FOREIGN KEY (activity_id) REFERENCES Activity(activity_id),
    FOREIGN KEY (sensor_location_id) REFERENCES Sensor(sensor_location_id),
    FOREIGN KEY (pressure_sensor_id) REFERENCES Sensor(sensor_id)
);

-- CREATE TABLE Timestamp (
-- 	sensor_id VARCHAR(50),
--     sequence_number BIGINT,
--     time_stamp VARCHAR(30),
--     FOREIGN KEY (sensor_id) REFERENCES SENSOR (sensor_id)
-- );

-- CREATE TABLE Sensor_signal (
-- 	sensor_id VARCHAR(50),
--     sequence_number BIGINT,
--     signal_output VARCHAR(30),
--     FOREIGN KEY (sensor_id) REFERENCES SENSOR (sensor_id)
-- );

-- CREATE TABLE Point_of_interest (
-- 	sensor_id VARCHAR(50),
--     point_of_interest_time_stamp VARCHAR(30),
--     FOREIGN KEY (sensor_id) REFERENCES SENSOR (sensor_id)
-- );