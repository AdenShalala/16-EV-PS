INSERT INTO Admin (admin_id, first_name, last_name, email, password) VALUES
('ef196bef-f691-41cd-a537-1b3152aa2c68', 'John', 'Chorizo', 'john.chorizo@admin.com', '$argon2id$v=19$m=65536,t=3,p=4$MfvUCUCyfMNyQBZqAdwGFQ$e8vdyLPm+rRPlKMoupSe0sCxoCLImAXC2n0Q0zOPPdE');

INSERT INTO Clinician (clinician_id, first_name, last_name, email, password, created_at) VALUES
('5854e7d9-a2c3-4af1-bb87-bbe393dd65b2', 'Amy', 'Adams', 'amy.adams@clinician.com', '$argon2id$v=19$m=65536,t=3,p=4$MfvUCUCyfMNyQBZqAdwGFQ$e8vdyLPm+rRPlKMoupSe0sCxoCLImAXC2n0Q0zOPPdE', '2025-08-12 10:32:21'),
('90709f2c-d75e-447a-86e5-c7592ebf5d83', 'Craig', 'Jones', 'craig.jones@clinician.com', '$argon2id$v=19$m=65536,t=3,p=4$MfvUCUCyfMNyQBZqAdwGFQ$e8vdyLPm+rRPlKMoupSe0sCxoCLImAXC2n0Q0zOPPdE', '2023-09-12 13:10:41');

INSERT INTO Patient (patient_id, first_name, last_name, height, weight, amputation_type, prosthetic_type, email, password, user_id, clinician_id) VALUES
('84ec8239-b141-48d0-ae68-fe9439863286', 'Eric', 'King', '181', '72', 'Anterior', 'Titanium', 'eric.king@patient.com', '$argon2id$v=19$m=65536,t=3,p=4$MfvUCUCyfMNyQBZqAdwGFQ$e8vdyLPm+rRPlKMoupSe0sCxoCLImAXC2n0Q0zOPPdE', 'USER01', '5854e7d9-a2c3-4af1-bb87-bbe393dd65b2'),
('5cc124e9-0db5-4d21-8bbc-3f073c015fa6', 'Sasha', 'Burev', '168', '59', 'Posterior', 'Carbon-Fiber', 'sasha.burev@patient.com', '$argon2id$v=19$m=65536,t=3,p=4$MfvUCUCyfMNyQBZqAdwGFQ$e8vdyLPm+rRPlKMoupSe0sCxoCLImAXC2n0Q0zOPPdE',  'USER02', '5854e7d9-a2c3-4af1-bb87-bbe393dd65b2'),
('515c01a6-81cb-4855-ba5b-1aa466fa41e7', 'Chris', 'Redfield', '192', '91', 'Posterior', 'Fiber-Glass', 'chris.redfield@patient.com', '$argon2id$v=19$m=65536,t=3,p=4$MfvUCUCyfMNyQBZqAdwGFQ$e8vdyLPm+rRPlKMoupSe0sCxoCLImAXC2n0Q0zOPPdE', 'USER03', '90709f2c-d75e-447a-86e5-c7592ebf5d83'),
('240b6600-f21e-4667-9428-5732f11d1a25', 'Sheva', 'Alomar', '166', '61', 'Posterior', 'Carbon-Fiber', 'sheva.alomar@patient.com', '$argon2id$v=19$m=65536,t=3,p=4$MfvUCUCyfMNyQBZqAdwGFQ$e8vdyLPm+rRPlKMoupSe0sCxoCLImAXC2n0Q0zOPPdE', 'USER04', '90709f2c-d75e-447a-86e5-c7592ebf5d83');

INSERT INTO Activity (activity_id, activity_type, start_time, end_time, is_uploaded, patient_id) VALUES
('62028bf5-4eb2-4e7a-bf28-c94a622564b4', 'Running', '1759769820', '1759770000', TRUE, '84ec8239-b141-48d0-ae68-fe9439863286'),
('faffdcf8-06f3-47d4-90b4-ce286c51eca8', 'Walking', '1759597200', '1759597800', TRUE, '84ec8239-b141-48d0-ae68-fe9439863286'),
('29326be6-7cd0-4235-8ba3-587e662905c6', 'Running', '1751393400', '1751393640', TRUE, '5cc124e9-0db5-4d21-8bbc-3f073c015fa6'),
('ef7787c9-0271-4ae0-91e4-9b81d4d893f0', 'Walking', '1749089400', '1749090000', TRUE, '5cc124e9-0db5-4d21-8bbc-3f073c015fa6'),
('44fd9690-d770-4e52-90ea-d881c25f4955', 'Jogging', '1751509200', '1751509440', TRUE, '515c01a6-81cb-4855-ba5b-1aa466fa41e7'), 
('57d17292-f4ca-4cb6-abb3-ff390faac9d8', 'Strolling', '1725330240', '1725330840', TRUE, '515c01a6-81cb-4855-ba5b-1aa466fa41e7'),
('44330f42-8d27-41fe-9906-6433058c0c32', 'Swimming', '1731288840', '1731289080', TRUE, '240b6600-f21e-4667-9428-5732f11d1a25'),
('76724920-6bec-46c8-9866-497ea534b9cf', 'Running', '1735090680', '1735091280', TRUE, '240b6600-f21e-4667-9428-5732f11d1a25');

INSERT INTO Sensor (sensor_id, patient_id, sensor_type, location_name, location_id, sensor_location_id, is_connected) VALUES
('7374299f-24a7-498c-8a53-dc5648050eee', '84ec8239-b141-48d0-ae68-fe9439863286', 0, 'upper', 0, '4211acbb-d69e-43f8-8c9e-8934ff071aea', TRUE),
('9078a409-5846-4f28-bb76-5fad493d3b56', '84ec8239-b141-48d0-ae68-fe9439863286', 1, 'lower', 1, '4be05ee6-d311-49a0-8ca6-9820a1a8c4ed', TRUE),
('e911f0cb-1bdf-4f21-ab90-a27c878072c4', '5cc124e9-0db5-4d21-8bbc-3f073c015fa6', 1, 'upper', 1, '645c7ccd-cf9f-4035-a7f5-96936de928a5', TRUE),
('c2684c2b-98f5-4a9a-a12c-5955f04a90f7', '5cc124e9-0db5-4d21-8bbc-3f073c015fa6', 1, 'upper', 1, 'af43c873-7a89-4691-9b14-ea1a27c12bfd', TRUE),
('890f0931-ddfc-433e-8c2e-4375a6045086', '515c01a6-81cb-4855-ba5b-1aa466fa41e7', 1, 'lower', 1, '3651fb01-21af-4930-aec4-3a9bbc43720d', TRUE),
('c8f5f9bc-4f3f-4af8-9518-800cafd5a26c', '515c01a6-81cb-4855-ba5b-1aa466fa41e7', 0, 'lower', 0, '7c700b2c-c045-4cd4-a9b9-080ea7dc9ec1', TRUE),
('b47c7487-65b6-4498-b7a0-9bb22e150fc0', '240b6600-f21e-4667-9428-5732f11d1a25', 0, 'lower', 0, '98489080-50d4-4098-9c46-dc1f97cbec81', TRUE),
('ba14edd4-227e-49ca-9102-aa588b42e2da', '240b6600-f21e-4667-9428-5732f11d1a25', 0, 'upper', 0, '2de7849e-09f8-493f-8d9c-15971ab5f492', TRUE);