INSERT INTO Clinician (clinician_id, name, email, password_hash)
VALUES ('CLIN402', 'Dr. Zhang', 'dr.zhang@example.com', 'fake_hash_for_test');

INSERT INTO Patient (patient_id, clinician_id, name, month_year_birth, gender, height, weight, 
                    amputation_type, socket_type, first_fitting, hours_per_week, distance_per_week)
VALUES ('PAT001', 'CLIN402', 'James Bond', '1990-05', 'M', 170, 65, 
        'Transfemoral', 'Ischial-support', '2023-01-15', 20, 30.5);

INSERT INTO Activity (activity_id, patient_id, start_time, end_time, activity_type)
VALUES ('ACT001', 'PAT001', '2025-08-05 10:00:00', '2025-08-05 10:05:00', 'walking');

INSERT INTO Sensor (sensor_id, activity_id, location, sensor_type, pressure_tolerance)
VALUES ('SEN001', 'ACT001', 'Socket', 'Pressure', 25.5);


INSERT INTO Timestamp (sensor_id, sequence_number, time_stamp)
VALUES 
  ('SEN001', 1, '0.0'),
  ('SEN001', 2, '0.2'),
  ('SEN001', 3, '0.4');

INSERT INTO Sensor_signal (sensor_id, sequence_number, signal_output)
VALUES 
  ('SEN001', 1, '12.3'),
  ('SEN001', 2, '15.7'),
  ('SEN001', 3, '18.2');

INSERT INTO Point_of_interest (sensor_id, point_of_interest_time_stamp)
VALUES 
  ('SEN001', '0.2'),
  ('SEN001', '0.4');