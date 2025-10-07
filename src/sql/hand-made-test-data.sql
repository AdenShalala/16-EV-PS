/*	So basically, to access the readings and the used sensor for each activity, you would simply get the sensor via;
		SELECT *
			FROM SENSOR
			WHERE sensor_id IN (
				SELECT sensor_id
				FROM ACTIVITYREADING
				WHERE activity_id = '62028bf5-4eb2-4e7a-bf28-c94a622564b4'
			)
		;
        
        And the pressure readings via:
        SELECT *
			FROM PRESSUREREADING
			WHERE reading_series_id IN (
				SELECT reading_series_id
				FROM ACTIVITYREADING
				WHERE reading_series_id = '6b68bb3b-52e2-42bc-89e1-9d9ae93a4103'
			) ORDER BY time
		;
	*/

INSERT INTO ADMIN values ('ef196bef-f691-41cd-a537-1b3152aa2c68', 'John', 'Chorizo', 'john@chorizo.com', 'hashedPassword');

INSERT INTO CLINICIAN (clinician_id, first_name, last_name, email, password, created_at) values
	('5854e7d9-a2c3-4af1-bb87-bbe393dd65b2', 'Amy', 'Adams', 'amy@adams.com', 'hashedAmyPassword', '2025-08-12 10:32:21'),
    ('90709f2c-d75e-447a-86e5-c7592ebf5d83', 'Craig', 'Jones', 'craig@jones.com', 'hashedCraigPassword', '2023-09-12 13:10:41');

INSERT INTO PATIENT (first_name, last_name, height, weight, amputation_type, prosthetic_type, email, password, patient_id, user_id, clinician_id) values
	('Eric', 'King', '181', '72', 'Anterior', 'Titanium', 'eric@king.com', 'hashedEricPassword', '84ec8239-b141-48d0-ae68-fe9439863286', 'USER01', '5854e7d9-a2c3-4af1-bb87-bbe393dd65b2'),
    ('Sasha', 'Burev', '168', '59', 'Posterior', 'Carbon-Fiber', 'sasha@burev.com', 'hashedSashaPassword', '5cc124e9-0db5-4d21-8bbc-3f073c015fa6', 'USER02', '5854e7d9-a2c3-4af1-bb87-bbe393dd65b2'),
    ('Chris', 'Redfield', '192', '91', 'Posterior', 'Fiber-Glass', 'chris@bsaa.com', 'hashedChrisPassword', '515c01a6-81cb-4855-ba5b-1aa466fa41e7', 'USER03', '90709f2c-d75e-447a-86e5-c7592ebf5d83'),
    ('Sheva', 'Alomar', '166', '61', 'Posterior', 'Carbon-Fiber', 'sheva@alomar.com', 'hashedShevaPassword', '240b6600-f21e-4667-9428-5732f11d1a25', 'USER04', '90709f2c-d75e-447a-86e5-c7592ebf5d83');

INSERT INTO ACTIVITY (activity_type, start_time, end_time, is_uploaded, patient_id, activity_id) values
	/*	Eric Kings Activities	                                                       ID: ---------------------------------------*/
	('Running', '1759769820', '1759770000', TRUE, '84ec8239-b141-48d0-ae68-fe9439863286', '62028bf5-4eb2-4e7a-bf28-c94a622564b4') /*4 Minute Activity*/,
    ('Walking', '1759597200', '1759597800', TRUE, '84ec8239-b141-48d0-ae68-fe9439863286', 'faffdcf8-06f3-47d4-90b4-ce286c51eca8') /*10 Minute Activity*/,
    /*	Sasha Burev's Activities	*/
    ('Running', '1751393400', '1751393640', TRUE, '5cc124e9-0db5-4d21-8bbc-3f073c015fa6', '29326be6-7cd0-4235-8ba3-587e662905c6') /*4 Minute Activity*/,
    ('Walking', '1749089400', '1749090000', TRUE, '5cc124e9-0db5-4d21-8bbc-3f073c015fa6', 'ef7787c9-0271-4ae0-91e4-9b81d4d893f0') /*10 Minute Activity*/,
    /*	Chris Redfields Activities	*/
    ('Jogging', '1751509200', '1751509440', TRUE, '515c01a6-81cb-4855-ba5b-1aa466fa41e7', '44fd9690-d770-4e52-90ea-d881c25f4955') /*4 Minute Activity*/,
    ('Strolling', '1725330240', '1725330840', TRUE, '515c01a6-81cb-4855-ba5b-1aa466fa41e7', '57d17292-f4ca-4cb6-abb3-ff390faac9d8') /*10 Minute Activity*/,
    /*	Sheva Alomars Activities	*/
    ('Swimming', '1731288840', '1731289080', TRUE, '240b6600-f21e-4667-9428-5732f11d1a25', '44330f42-8d27-41fe-9906-6433058c0c32') /*4 Minute Activity*/,
    ('Running', '1735090680', '1735091280', TRUE, '240b6600-f21e-4667-9428-5732f11d1a25', '76724920-6bec-46c8-9866-497ea534b9cf') /*10 Minute Activity*/
;

INSERT INTO SENSOR (sensor_id, patient_id, sensor_type, location_name, location_id, sensor_location_id, is_connected) values
	/*	Eric Kings Sensors	
  ID: -------------------------------------*/
	('7374299f-24a7-498c-8a53-dc5648050eee', '84ec8239-b141-48d0-ae68-fe9439863286', 0, 'upper', 0, '4211acbb-d69e-43f8-8c9e-8934ff071aea', TRUE),
    ('9078a409-5846-4f28-bb76-5fad493d3b56', '84ec8239-b141-48d0-ae68-fe9439863286', 1, 'lower', 1, '4be05ee6-d311-49a0-8ca6-9820a1a8c4ed', TRUE),
    /*	Sasha Burev's Sensors	*/
    ('e911f0cb-1bdf-4f21-ab90-a27c878072c4', '5cc124e9-0db5-4d21-8bbc-3f073c015fa6', 1, 'upper', 1, '645c7ccd-cf9f-4035-a7f5-96936de928a5', TRUE),
    ('c2684c2b-98f5-4a9a-a12c-5955f04a90f7', '5cc124e9-0db5-4d21-8bbc-3f073c015fa6', 1, 'upper', 1, 'af43c873-7a89-4691-9b14-ea1a27c12bfd', TRUE),
    /*	Chris Redfields Sensors	*/
    ('890f0931-ddfc-433e-8c2e-4375a6045086', '515c01a6-81cb-4855-ba5b-1aa466fa41e7', 1, 'lower', 1, '3651fb01-21af-4930-aec4-3a9bbc43720d', TRUE),
    ('c8f5f9bc-4f3f-4af8-9518-800cafd5a26c', '515c01a6-81cb-4855-ba5b-1aa466fa41e7', 0, 'lower', 0, '7c700b2c-c045-4cd4-a9b9-080ea7dc9ec1', TRUE),
    /*	Sheva Alomars Sensors	*/
    ('b47c7487-65b6-4498-b7a0-9bb22e150fc0', '240b6600-f21e-4667-9428-5732f11d1a25', 0, 'lower', 0, '98489080-50d4-4098-9c46-dc1f97cbec81', TRUE),
    ('ba14edd4-227e-49ca-9102-aa588b42e2da', '240b6600-f21e-4667-9428-5732f11d1a25', 0, 'upper', 0, '2de7849e-09f8-493f-8d9c-15971ab5f492', TRUE);


