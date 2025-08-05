CREATE TABLE Clinician (
    clinician_id   VARCHAR(50)  PRIMARY KEY,
    name           VARCHAR(100) NOT NULL,
    email          VARCHAR(100) NOT NULL,
    password_hash  VARCHAR(255) NOT NULL
);

CREATE TABLE Patient (
    patient_id    VARCHAR(50)   PRIMARY KEY,
    clinician_id  VARCHAR(50),
    name           VARCHAR(100),
    month_year_birth VARCHAR(10),
    gender        VARCHAR(20),
    height        BIGINT,
    weight        BIGINT,
    amputation_type VARCHAR(40),
    socket_type   VARCHAR(30),
    first_fitting VARCHAR(10),
    hours_per_week VARCHAR(30),
    distance_per_week VARCHAR(30),
    FOREIGN KEY (clinician_id) REFERENCES Clinician(clinician_id)
);

CREATE TABLE Activity (
	activity_id VARCHAR(50) PRIMARY KEY,
    patient_id VARCHAR(50),
    end_time VARCHAR(30),
    start_time VARCHAR(30),
    activity_type VARCHAR(20),
    FOREIGN KEY (patient_id) REFERENCES Patient (patient_id)
);

CREATE TABLE Sensor (
	sensor_id VARCHAR(50) PRIMARY KEY,
    activity_id VARCHAR(50),
    location VARCHAR(60),
    sensor_type VARCHAR(20),
    pressure_tolerance VARCHAR(30),
    FOREIGN KEY (activity_id) REFERENCES Activity (activity_id)
);

CREATE TABLE Timestamp (
	sensor_id VARCHAR(50),
    sequence_number BIGINT,
    time_stamp VARCHAR(30),
    FOREIGN KEY (sensor_id) REFERENCES SENSOR (sensor_id)
);

CREATE TABLE Sensor_signal (
	sensor_id VARCHAR(50),
    sequence_number BIGINT,
    signal_output VARCHAR(30),
    FOREIGN KEY (sensor_id) REFERENCES SENSOR (sensor_id)
);

CREATE TABLE Point_of_interest (
	sensor_id VARCHAR(50),
    point_of_interest_time_stamp VARCHAR(30),
    FOREIGN KEY (sensor_id) REFERENCES SENSOR (sensor_id)
);