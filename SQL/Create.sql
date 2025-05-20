CREATE TABLE User (
	user_id VARCHAR(50) PRIMARY KEY,
    clinician_id VARCHAR(50),
    month_year_birth VARCHAR(10),
    gender VARCHAR(20),
    height BIGINT,
    weight BIGINT,
    amputation_type VARCHAR(40),
    socket_type VARCHAR(30),
    first_fitting DATE,
    hours_per_week BIGINT,
    distance_per_week DECIMAL
);

CREATE TABLE Activity (
	activity_id VARCHAR(50) PRIMARY KEY,
    user_id VARCHAR(50),
    end_time DATETIME,
    start_time DATETIME,
    activity_type VARCHAR(20),
    FOREIGN KEY (user_id) REFERENCES User (user_id)
);

CREATE TABLE Sensor (
	sensor_id VARCHAR(50) PRIMARY KEY,
    activity_id VARCHAR(50),
    location VARCHAR(60),
    sensor_type VARCHAR(20),
    pressure_tolerance DECIMAL,
    FOREIGN KEY (activity_id) REFERENCES Activity (activity_id)
);

CREATE TABLE Timestamp (
	sensor_id VARCHAR(50),
    time_stamp DECIMAL,
    FOREIGN KEY (sensor_id) REFERENCES SENSOR (sensor_id)
);

CREATE TABLE Sensor_signal (
	sensor_id VARCHAR(50),
    signal_output DECIMAL,
    FOREIGN KEY (sensor_id) REFERENCES SENSOR (sensor_id)
);

CREATE TABLE Point_of_interest (
	sensor_id VARCHAR(50),
    point_of_interest_time_stamp DECIMAL,
    FOREIGN KEY (sensor_id) REFERENCES SENSOR (sensor_id)
);