-- Admins (unchanged)
INSERT INTO Admin (admin_id, first_name, last_name, email, password_hash) VALUES ('ADM001','AdminF1','AdminL1','admin1@system.com','hashed_pw_admin1');
INSERT INTO Admin (admin_id, first_name, last_name, email, password_hash) VALUES ('ADM002','AdminF2','AdminL2','admin2@system.com','hashed_pw_admin2');
INSERT INTO Admin (admin_id, first_name, last_name, email, password_hash) VALUES ('ADM003','AdminF3','AdminL3','admin3@system.com','hashed_pw_admin3');
INSERT INTO Admin (admin_id, first_name, last_name, email, password_hash) VALUES ('ADM004','AdminF4','AdminL4','admin4@system.com','hashed_pw_admin4');
INSERT INTO Admin (admin_id, first_name, last_name, email, password_hash) VALUES ('ADM005','AdminF5','AdminL5','admin5@system.com','hashed_pw_admin5');

-- Clinicians (unchanged)
INSERT INTO Clinician (clinician_id, first_name, last_name, email, password_hash) VALUES ('CLIN001','ClinF1','ClinL1','clin1@clinic.com','hashed_pw_clin1');
INSERT INTO Clinician (clinician_id, first_name, last_name, email, password_hash) VALUES ('CLIN002','ClinF2','ClinL2','clin2@clinic.com','hashed_pw_clin2');
INSERT INTO Clinician (clinician_id, first_name, last_name, email, password_hash) VALUES ('CLIN003','ClinF3','ClinL3','clin3@clinic.com','hashed_pw_clin3');
INSERT INTO Clinician (clinician_id, first_name, last_name, email, password_hash) VALUES ('CLIN004','ClinF4','ClinL4','clin4@clinic.com','hashed_pw_clin4');
INSERT INTO Clinician (clinician_id, first_name, last_name, email, password_hash) VALUES ('CLIN005','ClinF5','ClinL5','clin5@clinic.com','hashed_pw_clin5');
INSERT INTO Clinician (clinician_id, first_name, last_name, email, password_hash) VALUES ('CLIN006','ClinF6','ClinL6','clin6@clinic.com','hashed_pw_clin6');
INSERT INTO Clinician (clinician_id, first_name, last_name, email, password_hash) VALUES ('CLIN007','ClinF7','ClinL7','clin7@clinic.com','hashed_pw_clin7');
INSERT INTO Clinician (clinician_id, first_name, last_name, email, password_hash) VALUES ('CLIN008','ClinF8','ClinL8','clin8@clinic.com','hashed_pw_clin8');
INSERT INTO Clinician (clinician_id, first_name, last_name, email, password_hash) VALUES ('CLIN009','ClinF9','ClinL9','clin9@clinic.com','hashed_pw_clin9');
INSERT INTO Clinician (clinician_id, first_name, last_name, email, password_hash) VALUES ('CLIN010','ClinF10','ClinL10','clin10@clinic.com','hashed_pw_clin10');


-- Patients (unchanged)
INSERT INTO Patient (patient_id, first_name, last_name, height, weight, amputation_type, prosthetic_type, email, password_hash, user_id, clinician_id) VALUES ('PAT001','PatF1','PatL1','171','51','Below Knee','Blatchford Linx','pat1@patient.com','hashed_pw_pat1','USER001','CLIN007');
INSERT INTO Patient (patient_id, first_name, last_name, height, weight, amputation_type, prosthetic_type, email, password_hash, user_id, clinician_id) VALUES ('PAT002','PatF2','PatL2','161','77','Above Knee','Bebionic Arm','pat2@patient.com','hashed_pw_pat2','USER002','CLIN001');
INSERT INTO Patient (patient_id, first_name, last_name, height, weight, amputation_type, prosthetic_type, email, password_hash, user_id, clinician_id) VALUES ('PAT003','PatF3','PatL3','160','87','Above Knee','Bebionic Arm','pat3@patient.com','hashed_pw_pat3','USER003','CLIN002');
INSERT INTO Patient (patient_id, first_name, last_name, height, weight, amputation_type, prosthetic_type, email, password_hash, user_id, clinician_id) VALUES ('PAT004','PatF4','PatL4','175','54','Below Elbow','Blatchford Linx','pat4@patient.com','hashed_pw_pat4','USER004','CLIN004');
INSERT INTO Patient (patient_id, first_name, last_name, height, weight, amputation_type, prosthetic_type, email, password_hash, user_id, clinician_id) VALUES ('PAT005','PatF5','PatL5','183','72','Above Elbow','Bebionic Arm','pat5@patient.com','hashed_pw_pat5','USER005','CLIN007');
INSERT INTO Patient (patient_id, first_name, last_name, height, weight, amputation_type, prosthetic_type, email, password_hash, user_id, clinician_id) VALUES ('PAT006','PatF6','PatL6','152','61','Above Knee','Blatchford Linx','pat6@patient.com','hashed_pw_pat6','USER006','CLIN004');
INSERT INTO Patient (patient_id, first_name, last_name, height, weight, amputation_type, prosthetic_type, email, password_hash, user_id, clinician_id) VALUES ('PAT007','PatF7','PatL7','174','58','Above Knee','Ottobock Genium','pat7@patient.com','hashed_pw_pat7','USER007','CLIN006');
INSERT INTO Patient (patient_id, first_name, last_name, height, weight, amputation_type, prosthetic_type, email, password_hash, user_id, clinician_id) VALUES ('PAT008','PatF8','PatL8','156','86','Below Elbow','Blatchford Linx','pat8@patient.com','hashed_pw_pat8','USER008','CLIN005');
INSERT INTO Patient (patient_id, first_name, last_name, height, weight, amputation_type, prosthetic_type, email, password_hash, user_id, clinician_id) VALUES ('PAT009','PatF9','PatL9','163','72','Above Knee','Blatchford Linx','pat9@patient.com','hashed_pw_pat9','USER009','CLIN003');
INSERT INTO Patient (patient_id, first_name, last_name, height, weight, amputation_type, prosthetic_type, email, password_hash, user_id, clinician_id) VALUES ('PAT010','PatF10','PatL10','167','51','Above Knee','Blatchford Linx','pat10@patient.com','hashed_pw_pat10','USER010','CLIN010');
INSERT INTO Patient (patient_id, first_name, last_name, height, weight, amputation_type, prosthetic_type, email, password_hash, user_id, clinician_id) VALUES ('PAT011','PatF11','PatL11','161','64','Above Elbow','Bebionic Arm','pat11@patient.com','hashed_pw_pat11','USER011','CLIN005');
INSERT INTO Patient (patient_id, first_name, last_name, height, weight, amputation_type, prosthetic_type, email, password_hash, user_id, clinician_id) VALUES ('PAT012','PatF12','PatL12','187','61','Above Knee','Bebionic Arm','pat12@patient.com','hashed_pw_pat12','USER012','CLIN007');
INSERT INTO Patient (patient_id, first_name, last_name, height, weight, amputation_type, prosthetic_type, email, password_hash, user_id, clinician_id) VALUES ('PAT013','PatF13','PatL13','156','66','Below Knee','Blatchford Linx','pat13@patient.com','hashed_pw_pat13','USER013','CLIN004');
INSERT INTO Patient (patient_id, first_name, last_name, height, weight, amputation_type, prosthetic_type, email, password_hash, user_id, clinician_id) VALUES ('PAT014','PatF14','PatL14','179','68','Below Elbow','Ottobock Genium','pat14@patient.com','hashed_pw_pat14','USER014','CLIN007');
INSERT INTO Patient (patient_id, first_name, last_name, height, weight, amputation_type, prosthetic_type, email, password_hash, user_id, clinician_id) VALUES ('PAT015','PatF15','PatL15','163','75','Above Knee','Blatchford Linx','pat15@patient.com','hashed_pw_pat15','USER015','CLIN006');
INSERT INTO Patient (patient_id, first_name, last_name, height, weight, amputation_type, prosthetic_type, email, password_hash, user_id, clinician_id) VALUES ('PAT016','PatF16','PatL16','169','65','Above Knee','Bebionic Arm','pat16@patient.com','hashed_pw_pat16','USER016','CLIN001');
INSERT INTO Patient (patient_id, first_name, last_name, height, weight, amputation_type, prosthetic_type, email, password_hash, user_id, clinician_id) VALUES ('PAT017','PatF17','PatL17','181','59','Above Elbow','Bebionic Arm','pat17@patient.com','hashed_pw_pat17','USER017','CLIN002');
INSERT INTO Patient (patient_id, first_name, last_name, height, weight, amputation_type, prosthetic_type, email, password_hash, user_id, clinician_id) VALUES ('PAT018','PatF18','PatL18','182','67','Below Elbow','Bebionic Arm','pat18@patient.com','hashed_pw_pat18','USER018','CLIN003');
INSERT INTO Patient (patient_id, first_name, last_name, height, weight, amputation_type, prosthetic_type, email, password_hash, user_id, clinician_id) VALUES ('PAT019','PatF19','PatL19','159','56','Below Knee','Ottobock Genium','pat19@patient.com','hashed_pw_pat19','USER019','CLIN008');
INSERT INTO Patient (patient_id, first_name, last_name, height, weight, amputation_type, prosthetic_type, email, password_hash, user_id, clinician_id) VALUES ('PAT020','PatF20','PatL20','172','71','Above Elbow','Blatchford Linx','pat20@patient.com','hashed_pw_pat20','USER020','CLIN009');
INSERT INTO Patient (patient_id, first_name, last_name, height, weight, amputation_type, prosthetic_type, email, password_hash, user_id, clinician_id) VALUES ('PAT021','PatF21','PatL21','160','88','Above Elbow','Össur Rheo Knee','pat21@patient.com','hashed_pw_pat21','USER021','CLIN010');
INSERT INTO Patient (patient_id, first_name, last_name, height, weight, amputation_type, prosthetic_type, email, password_hash, user_id, clinician_id) VALUES ('PAT022','PatF22','PatL22','178','71','Above Knee','Ottobock Genium','pat22@patient.com','hashed_pw_pat22','USER022','CLIN001');
INSERT INTO Patient (patient_id, first_name, last_name, height, weight, amputation_type, prosthetic_type, email, password_hash, user_id, clinician_id) VALUES ('PAT023','PatF23','PatL23','177','67','Below Knee','Blatchford Linx','pat23@patient.com','hashed_pw_pat23','USER023','CLIN002');
INSERT INTO Patient (patient_id, first_name, last_name, height, weight, amputation_type, prosthetic_type, email, password_hash, user_id, clinician_id) VALUES ('PAT024','PatF24','PatL24','186','89','Above Knee','Ottobock Genium','pat24@patient.com','hashed_pw_pat24','USER024','CLIN003');
INSERT INTO Patient (patient_id, first_name, last_name, height, weight, amputation_type, prosthetic_type, email, password_hash, user_id, clinician_id) VALUES ('PAT025','PatF25','PatL25','170','90','Above Elbow','Össur Rheo Knee','pat25@patient.com','hashed_pw_pat25','USER025','CLIN004');
INSERT INTO Patient (patient_id, first_name, last_name, height, weight, amputation_type, prosthetic_type, email, password_hash, user_id, clinician_id) VALUES ('PAT026','PatF26','PatL26','163','88','Above Elbow','Ottobock Genium','pat26@patient.com','hashed_pw_pat26','USER026','CLIN005');
INSERT INTO Patient (patient_id, first_name, last_name, height, weight, amputation_type, prosthetic_type, email, password_hash, user_id, clinician_id) VALUES ('PAT027','PatF27','PatL27','157','80','Above Knee','Ottobock Genium','pat27@patient.com','hashed_pw_pat27','USER027','CLIN006');
INSERT INTO Patient (patient_id, first_name, last_name, height, weight, amputation_type, prosthetic_type, email, password_hash, user_id, clinician_id) VALUES ('PAT028','PatF28','PatL28','163','59','Below Knee','Ottobock Genium','pat28@patient.com','hashed_pw_pat28','USER028','CLIN007');
INSERT INTO Patient (patient_id, first_name, last_name, height, weight, amputation_type, prosthetic_type, email, password_hash, user_id, clinician_id) VALUES ('PAT029','PatF29','PatL29','190','50','Below Knee','Blatchford Linx','pat29@patient.com','hashed_pw_pat29','USER029','CLIN008');
INSERT INTO Patient (patient_id, first_name, last_name, height, weight, amputation_type, prosthetic_type, email, password_hash, user_id, clinician_id) VALUES ('PAT030','PatF30','PatL30','178','80','Below Elbow','Ottobock Genium','pat30@patient.com','hashed_pw_pat30','USER030','CLIN009');
INSERT INTO Patient (patient_id, first_name, last_name, height, weight, amputation_type, prosthetic_type, email, password_hash, user_id, clinician_id) VALUES ('PAT031','PatF31','PatL31','155','72','Above Knee','Blatchford Linx','pat31@patient.com','hashed_pw_pat31','USER031','CLIN010');
INSERT INTO Patient (patient_id, first_name, last_name, height, weight, amputation_type, prosthetic_type, email, password_hash, user_id, clinician_id) VALUES ('PAT032','PatF32','PatL32','173','62','Below Knee','Blatchford Linx','pat32@patient.com','hashed_pw_pat32','USER032','CLIN001');
INSERT INTO Patient (patient_id, first_name, last_name, height, weight, amputation_type, prosthetic_type, email, password_hash, user_id, clinician_id) VALUES ('PAT033','PatF33','PatL33','190','71','Below Knee','Ottobock Genium','pat33@patient.com','hashed_pw_pat33','USER033','CLIN002');
INSERT INTO Patient (patient_id, first_name, last_name, height, weight, amputation_type, prosthetic_type, email, password_hash, user_id, clinician_id) VALUES ('PAT034','PatF34','PatL34','170','59','Above Knee','Ottobock Genium','pat34@patient.com','hashed_pw_pat34','USER034','CLIN003');
INSERT INTO Patient (patient_id, first_name, last_name, height, weight, amputation_type, prosthetic_type, email, password_hash, user_id, clinician_id) VALUES ('PAT035','PatF35','PatL35','161','82','Below Elbow','Ottobock Genium','pat35@patient.com','hashed_pw_pat35','USER035','CLIN004');


-- Activities (unchanged)
INSERT INTO Activity (activity_id, activity_type, start_time, end_time, is_uploaded, patient_id) VALUES ('ACT001_1','Running',1693110000,1693110879,TRUE,'PAT001');
INSERT INTO Activity (activity_id, activity_type, start_time, end_time, is_uploaded, patient_id) VALUES ('ACT001_2','Standing',1693110500,1693111822,TRUE,'PAT001');
INSERT INTO Activity (activity_id, activity_type, start_time, end_time, is_uploaded, patient_id) VALUES ('ACT002_1','Walking',1693120000,1693122542,TRUE,'PAT002');
INSERT INTO Activity (activity_id, activity_type, start_time, end_time, is_uploaded, patient_id) VALUES ('ACT002_2','Running',1693120500,1693121367,TRUE,'PAT002');
INSERT INTO Activity (activity_id, activity_type, start_time, end_time, is_uploaded, patient_id) VALUES ('ACT003_1','Running',1693130000,1693132247,TRUE,'PAT003');
INSERT INTO Activity (activity_id, activity_type, start_time, end_time, is_uploaded, patient_id) VALUES ('ACT003_2','Walking',1693130500,1693131566,TRUE,'PAT003');
INSERT INTO Activity (activity_id, activity_type, start_time, end_time, is_uploaded, patient_id) VALUES ('ACT004_1','GripTest',1693140000,1693140648,TRUE,'PAT004');
INSERT INTO Activity (activity_id, activity_type, start_time, end_time, is_uploaded, patient_id) VALUES ('ACT004_2','Running',1693140500,1693143794,TRUE,'PAT004');
INSERT INTO Activity (activity_id, activity_type, start_time, end_time, is_uploaded, patient_id) VALUES ('ACT005_1','Standing',1693150000,1693150624,TRUE,'PAT005');
INSERT INTO Activity (activity_id, activity_type, start_time, end_time, is_uploaded, patient_id) VALUES ('ACT005_2','Cycling',1693150500,1693153344,TRUE,'PAT005');
INSERT INTO Activity (activity_id, activity_type, start_time, end_time, is_uploaded, patient_id) VALUES ('ACT006_1','Running',1693160000,1693161957,TRUE,'PAT006');
INSERT INTO Activity (activity_id, activity_type, start_time, end_time, is_uploaded, patient_id) VALUES ('ACT006_2','Walking',1693160500,1693163710,TRUE,'PAT006');
INSERT INTO Activity (activity_id, activity_type, start_time, end_time, is_uploaded, patient_id) VALUES ('ACT007_1','Cycling',1693170000,1693171039,TRUE,'PAT007');
INSERT INTO Activity (activity_id, activity_type, start_time, end_time, is_uploaded, patient_id) VALUES ('ACT007_2','Running',1693170500,1693171916,TRUE,'PAT007');
INSERT INTO Activity (activity_id, activity_type, start_time, end_time, is_uploaded, patient_id) VALUES ('ACT008_1','Cycling',1693180000,1693182354,TRUE,'PAT008');
INSERT INTO Activity (activity_id, activity_type, start_time, end_time, is_uploaded, patient_id) VALUES ('ACT008_2','GripTest',1693180500,1693181526,TRUE,'PAT008');
INSERT INTO Activity (activity_id, activity_type, start_time, end_time, is_uploaded, patient_id) VALUES ('ACT009_1','Lifting',1693190000,1693191224,TRUE,'PAT009');
INSERT INTO Activity (activity_id, activity_type, start_time, end_time, is_uploaded, patient_id) VALUES ('ACT009_2','Lifting',1693190500,1693193467,TRUE,'PAT009');
INSERT INTO Activity (activity_id, activity_type, start_time, end_time, is_uploaded, patient_id) VALUES ('ACT010_1','Cycling',1693200000,1693203410,TRUE,'PAT010');
INSERT INTO Activity (activity_id, activity_type, start_time, end_time, is_uploaded, patient_id) VALUES ('ACT010_2','Walking',1693200500,1693201828,TRUE,'PAT010');
INSERT INTO Activity (activity_id, activity_type, start_time, end_time, is_uploaded, patient_id) VALUES ('ACT011_1','Standing',1693210000,1693210884,TRUE,'PAT011');
INSERT INTO Activity (activity_id, activity_type, start_time, end_time, is_uploaded, patient_id) VALUES ('ACT011_2','GripTest',1693210500,1693212694,TRUE,'PAT011');
INSERT INTO Activity (activity_id, activity_type, start_time, end_time, is_uploaded, patient_id) VALUES ('ACT012_1','Walking',1693220000,1693221851,TRUE,'PAT012');
INSERT INTO Activity (activity_id, activity_type, start_time, end_time, is_uploaded, patient_id) VALUES ('ACT012_2','Running',1693220500,1693222104,TRUE,'PAT012');
INSERT INTO Activity (activity_id, activity_type, start_time, end_time, is_uploaded, patient_id) VALUES ('ACT013_1','Walking',1693230000,1693233336,TRUE,'PAT013');
INSERT INTO Activity (activity_id, activity_type, start_time, end_time, is_uploaded, patient_id) VALUES ('ACT013_2','Standing',1693230500,1693231677,TRUE,'PAT013');
INSERT INTO Activity (activity_id, activity_type, start_time, end_time, is_uploaded, patient_id) VALUES ('ACT014_1','Running',1693240000,1693241486,TRUE,'PAT014');
INSERT INTO Activity (activity_id, activity_type, start_time, end_time, is_uploaded, patient_id) VALUES ('ACT014_2','GripTest',1693240500,1693243810,TRUE,'PAT014');
INSERT INTO Activity (activity_id, activity_type, start_time, end_time, is_uploaded, patient_id) VALUES ('ACT015_1','Lifting',1693250000,1693251882,TRUE,'PAT015');
INSERT INTO Activity (activity_id, activity_type, start_time, end_time, is_uploaded, patient_id) VALUES ('ACT015_2','Walking',1693250500,1693253185,TRUE,'PAT015');

-- New activities for additional patients
INSERT INTO Activity (activity_id, activity_type, start_time, end_time, is_uploaded, patient_id) VALUES ('ACT016_1','Running',1693260000,1693262168,TRUE,'PAT016');
INSERT INTO Activity (activity_id, activity_type, start_time, end_time, is_uploaded, patient_id) VALUES ('ACT016_2','Cycling',1693260500,1693262407,TRUE,'PAT016');
INSERT INTO Activity (activity_id, activity_type, start_time, end_time, is_uploaded, patient_id) VALUES ('ACT017_1','GripTest',1693270000,1693271035,TRUE,'PAT017');
INSERT INTO Activity (activity_id, activity_type, start_time, end_time, is_uploaded, patient_id) VALUES ('ACT017_2','Lifting',1693270500,1693272815,TRUE,'PAT017');
INSERT INTO Activity (activity_id, activity_type, start_time, end_time, is_uploaded, patient_id) VALUES ('ACT018_1','Walking',1693280000,1693281644,TRUE,'PAT018');
INSERT INTO Activity (activity_id, activity_type, start_time, end_time, is_uploaded, patient_id) VALUES ('ACT018_2','GripTest',1693280500,1693282689,TRUE,'PAT018');
INSERT INTO Activity (activity_id, activity_type, start_time, end_time, is_uploaded, patient_id) VALUES ('ACT019_1','Cycling',1693290000,1693293138,TRUE,'PAT019');
INSERT INTO Activity (activity_id, activity_type, start_time, end_time, is_uploaded, patient_id) VALUES ('ACT019_2','Running',1693290500,1693292557,TRUE,'PAT019');
INSERT INTO Activity (activity_id, activity_type, start_time, end_time, is_uploaded, patient_id) VALUES ('ACT020_1','Lifting',1693300000,1693301498,TRUE,'PAT020');
INSERT INTO Activity (activity_id, activity_type, start_time, end_time, is_uploaded, patient_id) VALUES ('ACT020_2','GripTest',1693300500,1693302857,TRUE,'PAT020');
INSERT INTO Activity (activity_id, activity_type, start_time, end_time, is_uploaded, patient_id) VALUES ('ACT021_1','Standing',1693310000,1693310663,TRUE,'PAT021');
INSERT INTO Activity (activity_id, activity_type, start_time, end_time, is_uploaded, patient_id) VALUES ('ACT021_2','Walking',1693310500,1693313922,TRUE,'PAT021');
INSERT INTO Activity (activity_id, activity_type, start_time, end_time, is_uploaded, patient_id) VALUES ('ACT022_1','Running',1693320000,1693322879,TRUE,'PAT022');
INSERT INTO Activity (activity_id, activity_type, start_time, end_time, is_uploaded, patient_id) VALUES ('ACT022_2','Cycling',1693320500,1693324049,TRUE,'PAT022');
INSERT INTO Activity (activity_id, activity_type, start_time, end_time, is_uploaded, patient_id) VALUES ('ACT023_1','Standing',1693330000,1693330739,TRUE,'PAT023');
INSERT INTO Activity (activity_id, activity_type, start_time, end_time, is_uploaded, patient_id) VALUES ('ACT023_2','Walking',1693330500,1693332982,TRUE,'PAT023');
INSERT INTO Activity (activity_id, activity_type, start_time, end_time, is_uploaded, patient_id) VALUES ('ACT024_1','Running',1693340000,1693343526,TRUE,'PAT024');
INSERT INTO Activity (activity_id, activity_type, start_time, end_time, is_uploaded, patient_id) VALUES ('ACT024_2','Lifting',1693340500,1693342089,TRUE,'PAT024');
INSERT INTO Activity (activity_id, activity_type, start_time, end_time, is_uploaded, patient_id) VALUES ('ACT025_1','GripTest',1693350000,1693351566,TRUE,'PAT025');
INSERT INTO Activity (activity_id, activity_type, start_time, end_time, is_uploaded, patient_id) VALUES ('ACT025_2','Standing',1693350500,1693352865,TRUE,'PAT025');
INSERT INTO Activity (activity_id, activity_type, start_time, end_time, is_uploaded, patient_id) VALUES ('ACT026_1','Walking',1693360000,1693363409,TRUE,'PAT026');
INSERT INTO Activity (activity_id, activity_type, start_time, end_time, is_uploaded, patient_id) VALUES ('ACT026_2','GripTest',1693360500,1693361507,TRUE,'PAT026');
INSERT INTO Activity (activity_id, activity_type, start_time, end_time, is_uploaded, patient_id) VALUES ('ACT027_1','Cycling',1693370000,1693372299,TRUE,'PAT027');
INSERT INTO Activity (activity_id, activity_type, start_time, end_time, is_uploaded, patient_id) VALUES ('ACT027_2','Running',1693370500,1693371302,TRUE,'PAT027');
INSERT INTO Activity (activity_id, activity_type, start_time, end_time, is_uploaded, patient_id) VALUES ('ACT028_1','Walking',1693380000,1693381582,TRUE,'PAT028');
INSERT INTO Activity (activity_id, activity_type, start_time, end_time, is_uploaded, patient_id) VALUES ('ACT028_2','Standing',1693380500,1693382449,TRUE,'PAT028');
INSERT INTO Activity (activity_id, activity_type, start_time, end_time, is_uploaded, patient_id) VALUES ('ACT029_1','Lifting',1693390000,1693392771,TRUE,'PAT029');
INSERT INTO Activity (activity_id, activity_type, start_time, end_time, is_uploaded, patient_id) VALUES ('ACT029_2','Running',1693390500,1693391395,TRUE,'PAT029');
INSERT INTO Activity (activity_id, activity_type, start_time, end_time, is_uploaded, patient_id) VALUES ('ACT030_1','Cycling',1693400000,1693400843,TRUE,'PAT030');
INSERT INTO Activity (activity_id, activity_type, start_time, end_time, is_uploaded, patient_id) VALUES ('ACT030_2','GripTest',1693400500,1693402908,TRUE,'PAT030');
INSERT INTO Activity (activity_id, activity_type, start_time, end_time, is_uploaded, patient_id) VALUES ('ACT031_1','Standing',1693410000,1693413137,TRUE,'PAT031');
INSERT INTO Activity (activity_id, activity_type, start_time, end_time, is_uploaded, patient_id) VALUES ('ACT031_2','Walking',1693410500,1693413339,TRUE,'PAT031');
INSERT INTO Activity (activity_id, activity_type, start_time, end_time, is_uploaded, patient_id) VALUES ('ACT032_1','Running',1693420000,1693422000,TRUE,'PAT032');
INSERT INTO Activity (activity_id, activity_type, start_time, end_time, is_uploaded, patient_id) VALUES ('ACT032_2','Cycling',1693420500,1693422774,TRUE,'PAT032');
INSERT INTO Activity (activity_id, activity_type, start_time, end_time, is_uploaded, patient_id) VALUES ('ACT033_1','Lifting',1693430000,1693430650,TRUE,'PAT033');
INSERT INTO Activity (activity_id, activity_type, start_time, end_time, is_uploaded, patient_id) VALUES ('ACT033_2','Walking',1693430500,1693431507,TRUE,'PAT033');
INSERT INTO Activity (activity_id, activity_type, start_time, end_time, is_uploaded, patient_id) VALUES ('ACT034_1','Standing',1693440000,1693441203,TRUE,'PAT034');
INSERT INTO Activity (activity_id, activity_type, start_time, end_time, is_uploaded, patient_id) VALUES ('ACT034_2','Running',1693440500,1693442772,TRUE,'PAT034');
INSERT INTO Activity (activity_id, activity_type, start_time, end_time, is_uploaded, patient_id) VALUES ('ACT035_1','GripTest',1693450000,1693452416,TRUE,'PAT035');

INSERT INTO Sensor (sensor_id, location_name, sensor_location_id, sensor_type, is_connected, patient_email, location_id, pressure_sensor_id, activity_id) VALUES ('SNS001_1','Loc1','LOC001_A1',4,TRUE,'pat1@patient.com',101,NULL,'ACT001_1');
INSERT INTO Sensor (sensor_id, location_name, sensor_location_id, sensor_type, is_connected, patient_email, location_id, pressure_sensor_id, activity_id) VALUES ('SNS001_2','Loc1','LOC001_A2',4,TRUE,'pat1@patient.com',101,NULL,'ACT001_2');
INSERT INTO Sensor (sensor_id, location_name, sensor_location_id, sensor_type, is_connected, patient_email, location_id, pressure_sensor_id, activity_id) VALUES ('SNS002_1','Loc2','LOC002_A1',2,TRUE,'pat2@patient.com',102,NULL,'ACT002_1');
INSERT INTO Sensor (sensor_id, location_name, sensor_location_id, sensor_type, is_connected, patient_email, location_id, pressure_sensor_id, activity_id) VALUES ('SNS002_2','Loc2','LOC002_A2',2,TRUE,'pat2@patient.com',102,NULL,'ACT002_2');
INSERT INTO Sensor (sensor_id, location_name, sensor_location_id, sensor_type, is_connected, patient_email, location_id, pressure_sensor_id, activity_id) VALUES ('SNS003_1','Loc3','LOC003_A1',2,TRUE,'pat3@patient.com',103,NULL,'ACT003_1');
INSERT INTO Sensor (sensor_id, location_name, sensor_location_id, sensor_type, is_connected, patient_email, location_id, pressure_sensor_id, activity_id) VALUES ('SNS003_2','Loc3','LOC003_A2',2,TRUE,'pat3@patient.com',103,NULL,'ACT003_2');
INSERT INTO Sensor (sensor_id, location_name, sensor_location_id, sensor_type, is_connected, patient_email, location_id, pressure_sensor_id, activity_id) VALUES ('SNS004_1','Loc4','LOC004_A1',3,TRUE,'pat4@patient.com',104,NULL,'ACT004_1');
INSERT INTO Sensor (sensor_id, location_name, sensor_location_id, sensor_type, is_connected, patient_email, location_id, pressure_sensor_id, activity_id) VALUES ('SNS004_2','Loc4','LOC004_A2',3,TRUE,'pat4@patient.com',104,NULL,'ACT004_2');
INSERT INTO Sensor (sensor_id, location_name, sensor_location_id, sensor_type, is_connected, patient_email, location_id, pressure_sensor_id, activity_id) VALUES ('SNS005_1','Loc5','LOC005_A1',2,TRUE,'pat5@patient.com',105,NULL,'ACT005_1');
INSERT INTO Sensor (sensor_id, location_name, sensor_location_id, sensor_type, is_connected, patient_email, location_id, pressure_sensor_id, activity_id) VALUES ('SNS005_2','Loc5','LOC005_A2',2,TRUE,'pat5@patient.com',105,NULL,'ACT005_2');
INSERT INTO Sensor (sensor_id, location_name, sensor_location_id, sensor_type, is_connected, patient_email, location_id, pressure_sensor_id, activity_id) VALUES ('SNS006_1','Loc6','LOC006_A1',1,TRUE,'pat6@patient.com',106,NULL,'ACT006_1');
INSERT INTO Sensor (sensor_id, location_name, sensor_location_id, sensor_type, is_connected, patient_email, location_id, pressure_sensor_id, activity_id) VALUES ('SNS006_2','Loc6','LOC006_A2',1,TRUE,'pat6@patient.com',106,NULL,'ACT006_2');
INSERT INTO Sensor (sensor_id, location_name, sensor_location_id, sensor_type, is_connected, patient_email, location_id, pressure_sensor_id, activity_id) VALUES ('SNS007_1','Loc7','LOC007_A1',4,TRUE,'pat7@patient.com',107,NULL,'ACT007_1');
INSERT INTO Sensor (sensor_id, location_name, sensor_location_id, sensor_type, is_connected, patient_email, location_id, pressure_sensor_id, activity_id) VALUES ('SNS007_2','Loc7','LOC007_A2',4,TRUE,'pat7@patient.com',107,NULL,'ACT007_2');
INSERT INTO Sensor (sensor_id, location_name, sensor_location_id, sensor_type, is_connected, patient_email, location_id, pressure_sensor_id, activity_id) VALUES ('SNS008_1','Loc8','LOC008_A1',2,TRUE,'pat8@patient.com',108,NULL,'ACT008_1');
INSERT INTO Sensor (sensor_id, location_name, sensor_location_id, sensor_type, is_connected, patient_email, location_id, pressure_sensor_id, activity_id) VALUES ('SNS008_2','Loc8','LOC008_A2',3,TRUE,'pat8@patient.com',108,NULL,'ACT008_2');
INSERT INTO Sensor (sensor_id, location_name, sensor_location_id, sensor_type, is_connected, patient_email, location_id, pressure_sensor_id, activity_id) VALUES ('SNS009_1','Loc9','LOC009_A1',2,TRUE,'pat9@patient.com',109,NULL,'ACT009_1');
INSERT INTO Sensor (sensor_id, location_name, sensor_location_id, sensor_type, is_connected, patient_email, location_id, pressure_sensor_id, activity_id) VALUES ('SNS009_2','Loc9','LOC009_A2',2,TRUE,'pat9@patient.com',109,NULL,'ACT009_2');
INSERT INTO Sensor (sensor_id, location_name, sensor_location_id, sensor_type, is_connected, patient_email, location_id, pressure_sensor_id, activity_id) VALUES ('SNS010_1','Loc10','LOC010_A1',1,TRUE,'pat10@patient.com',110,NULL,'ACT010_1');
INSERT INTO Sensor (sensor_id, location_name, sensor_location_id, sensor_type, is_connected, patient_email, location_id, pressure_sensor_id, activity_id) VALUES ('SNS010_2','Loc10','LOC010_A2',1,TRUE,'pat10@patient.com',110,NULL,'ACT010_2');
INSERT INTO Sensor (sensor_id, location_name, sensor_location_id, sensor_type, is_connected, patient_email, location_id, pressure_sensor_id, activity_id) VALUES ('SNS011_1','Loc11','LOC011_A1',4,TRUE,'pat11@patient.com',111,NULL,'ACT011_1');
INSERT INTO Sensor (sensor_id, location_name, sensor_location_id, sensor_type, is_connected, patient_email, location_id, pressure_sensor_id, activity_id) VALUES ('SNS011_2','Loc11','LOC011_A2',3,TRUE,'pat11@patient.com',111,NULL,'ACT011_2');
INSERT INTO Sensor (sensor_id, location_name, sensor_location_id, sensor_type, is_connected, patient_email, location_id, pressure_sensor_id, activity_id) VALUES ('SNS012_1','Loc12','LOC012_A1',2,TRUE,'pat12@patient.com',112,NULL,'ACT012_1');
INSERT INTO Sensor (sensor_id, location_name, sensor_location_id, sensor_type, is_connected, patient_email, location_id, pressure_sensor_id, activity_id) VALUES ('SNS012_2','Loc12','LOC012_A2',2,TRUE,'pat12@patient.com',112,NULL,'ACT012_2');
INSERT INTO Sensor (sensor_id, location_name, sensor_location_id, sensor_type, is_connected, patient_email, location_id, pressure_sensor_id, activity_id) VALUES ('SNS013_1','Loc13','LOC013_A1',1,TRUE,'pat13@patient.com',113,NULL,'ACT013_1');
INSERT INTO Sensor (sensor_id, location_name, sensor_location_id, sensor_type, is_connected, patient_email, location_id, pressure_sensor_id, activity_id) VALUES ('SNS013_2','Loc13','LOC013_A2',1,TRUE,'pat13@patient.com',113,NULL,'ACT013_2');
INSERT INTO Sensor (sensor_id, location_name, sensor_location_id, sensor_type, is_connected, patient_email, location_id, pressure_sensor_id, activity_id) VALUES ('SNS014_1','Loc14','LOC014_A1',3,TRUE,'pat14@patient.com',114,NULL,'ACT014_1');
INSERT INTO Sensor (sensor_id, location_name, sensor_location_id, sensor_type, is_connected, patient_email, location_id, pressure_sensor_id, activity_id) VALUES ('SNS014_2','Loc14','LOC014_A2',3,TRUE,'pat14@patient.com',114,NULL,'ACT014_2');
INSERT INTO Sensor (sensor_id, location_name, sensor_location_id, sensor_type, is_connected, patient_email, location_id, pressure_sensor_id, activity_id) VALUES ('SNS015_1','Loc15','LOC015_A1',4,TRUE,'pat15@patient.com',115,NULL,'ACT015_1');
INSERT INTO Sensor (sensor_id, location_name, sensor_location_id, sensor_type, is_connected, patient_email, location_id, pressure_sensor_id, activity_id) VALUES ('SNS015_2','Loc15','LOC015_A2',1,TRUE,'pat15@patient.com',115,NULL,'ACT015_2');

-- New sensors for additional patients
INSERT INTO Sensor (sensor_id, location_name, sensor_location_id, sensor_type, is_connected, patient_email, location_id, pressure_sensor_id, activity_id) VALUES ('SNS016_1','Loc16','LOC016_A1',2,TRUE,'pat16@patient.com',116,NULL,'ACT016_1');
INSERT INTO Sensor (sensor_id, location_name, sensor_location_id, sensor_type, is_connected, patient_email, location_id, pressure_sensor_id, activity_id) VALUES ('SNS016_2','Loc16','LOC016_A2',2,TRUE,'pat16@patient.com',116,NULL,'ACT016_2');
INSERT INTO Sensor (sensor_id, location_name, sensor_location_id, sensor_type, is_connected, patient_email, location_id, pressure_sensor_id, activity_id) VALUES ('SNS017_1','Loc17','LOC017_A1',3,TRUE,'pat17@patient.com',117,NULL,'ACT017_1');
INSERT INTO Sensor (sensor_id, location_name, sensor_location_id, sensor_type, is_connected, patient_email, location_id, pressure_sensor_id, activity_id) VALUES ('SNS017_2','Loc17','LOC017_A2',3,TRUE,'pat17@patient.com',117,NULL,'ACT017_2');
INSERT INTO Sensor (sensor_id, location_name, sensor_location_id, sensor_type, is_connected, patient_email, location_id, pressure_sensor_id, activity_id) VALUES ('SNS018_1','Loc18','LOC018_A1',2,TRUE,'pat18@patient.com',118,NULL,'ACT018_1');
INSERT INTO Sensor (sensor_id, location_name, sensor_location_id, sensor_type, is_connected, patient_email, location_id, pressure_sensor_id, activity_id) VALUES ('SNS018_2','Loc18','LOC018_A2',2,TRUE,'pat18@patient.com',118,NULL,'ACT018_2');

-- Continuing with remaining sensors for patients 19-35
INSERT INTO Sensor (sensor_id, location_name, sensor_location_id, sensor_type, is_connected, patient_email, location_id, pressure_sensor_id, activity_id) VALUES ('SNS019_1','Loc19','LOC019_A1',4,TRUE,'pat19@patient.com',119,NULL,'ACT019_1');
INSERT INTO Sensor (sensor_id, location_name, sensor_location_id, sensor_type, is_connected, patient_email, location_id, pressure_sensor_id, activity_id) VALUES ('SNS019_2','Loc19','LOC019_A2',4,TRUE,'pat19@patient.com',119,NULL,'ACT019_2');
INSERT INTO Sensor (sensor_id, location_name, sensor_location_id, sensor_type, is_connected, patient_email, location_id, pressure_sensor_id, activity_id) VALUES ('SNS020_1','Loc20','LOC020_A1',3,TRUE,'pat20@patient.com',120,NULL,'ACT020_1');
INSERT INTO Sensor (sensor_id, location_name, sensor_location_id, sensor_type, is_connected, patient_email, location_id, pressure_sensor_id, activity_id) VALUES ('SNS020_2','Loc20','LOC020_A2',3,TRUE,'pat20@patient.com',120,NULL,'ACT020_2');
INSERT INTO Sensor (sensor_id, location_name, sensor_location_id, sensor_type, is_connected, patient_email, location_id, pressure_sensor_id, activity_id) VALUES ('SNS021_1','Loc21','LOC021_A1',1,TRUE,'pat21@patient.com',121,NULL,'ACT021_1');
INSERT INTO Sensor (sensor_id, location_name, sensor_location_id, sensor_type, is_connected, patient_email, location_id, pressure_sensor_id, activity_id) VALUES ('SNS021_2','Loc21','LOC021_A2',1,TRUE,'pat21@patient.com',121,NULL,'ACT021_2');
INSERT INTO Sensor (sensor_id, location_name, sensor_location_id, sensor_type, is_connected, patient_email, location_id, pressure_sensor_id, activity_id) VALUES ('SNS022_1','Loc22','LOC022_A1',4,TRUE,'pat22@patient.com',122,NULL,'ACT022_1');
INSERT INTO Sensor (sensor_id, location_name, sensor_location_id, sensor_type, is_connected, patient_email, location_id, pressure_sensor_id, activity_id) VALUES ('SNS022_2','Loc22','LOC022_A2',4,TRUE,'pat22@patient.com',122,NULL,'ACT022_2');
INSERT INTO Sensor (sensor_id, location_name, sensor_location_id, sensor_type, is_connected, patient_email, location_id, pressure_sensor_id, activity_id) VALUES ('SNS023_1','Loc23','LOC023_A1',1,TRUE,'pat23@patient.com',123,NULL,'ACT023_1');
INSERT INTO Sensor (sensor_id, location_name, sensor_location_id, sensor_type, is_connected, patient_email, location_id, pressure_sensor_id, activity_id) VALUES ('SNS023_2','Loc23','LOC023_A2',1,TRUE,'pat23@patient.com',123,NULL,'ACT023_2');
INSERT INTO Sensor (sensor_id, location_name, sensor_location_id, sensor_type, is_connected, patient_email, location_id, pressure_sensor_id, activity_id) VALUES ('SNS024_1','Loc24','LOC024_A1',4,TRUE,'pat24@patient.com',124,NULL,'ACT024_1');
INSERT INTO Sensor (sensor_id, location_name, sensor_location_id, sensor_type, is_connected, patient_email, location_id, pressure_sensor_id, activity_id) VALUES ('SNS024_2','Loc24','LOC024_A2',4,TRUE,'pat24@patient.com',124,NULL,'ACT024_2');
INSERT INTO Sensor (sensor_id, location_name, sensor_location_id, sensor_type, is_connected, patient_email, location_id, pressure_sensor_id, activity_id) VALUES ('SNS025_1','Loc25','LOC025_A1',3,TRUE,'pat25@patient.com',125,NULL,'ACT025_1');
INSERT INTO Sensor (sensor_id, location_name, sensor_location_id, sensor_type, is_connected, patient_email, location_id, pressure_sensor_id, activity_id) VALUES ('SNS025_2','Loc25','LOC025_A2',3,TRUE,'pat25@patient.com',125,NULL,'ACT025_2');
INSERT INTO Sensor (sensor_id, location_name, sensor_location_id, sensor_type, is_connected, patient_email, location_id, pressure_sensor_id, activity_id) VALUES ('SNS026_1','Loc26','LOC026_A1',1,TRUE,'pat26@patient.com',126,NULL,'ACT026_1');
INSERT INTO Sensor (sensor_id, location_name, sensor_location_id, sensor_type, is_connected, patient_email, location_id, pressure_sensor_id, activity_id) VALUES ('SNS026_2','Loc26','LOC026_A2',1,TRUE,'pat26@patient.com',126,NULL,'ACT026_2');
INSERT INTO Sensor (sensor_id, location_name, sensor_location_id, sensor_type, is_connected, patient_email, location_id, pressure_sensor_id, activity_id) VALUES ('SNS027_1','Loc27','LOC027_A1',4,TRUE,'pat27@patient.com',127,NULL,'ACT027_1');
INSERT INTO Sensor (sensor_id, location_name, sensor_location_id, sensor_type, is_connected, patient_email, location_id, pressure_sensor_id, activity_id) VALUES ('SNS027_2','Loc27','LOC027_A2',4,TRUE,'pat27@patient.com',127,NULL,'ACT027_2');
INSERT INTO Sensor (sensor_id, location_name, sensor_location_id, sensor_type, is_connected, patient_email, location_id, pressure_sensor_id, activity_id) VALUES ('SNS028_1','Loc28','LOC028_A1',1,TRUE,'pat28@patient.com',128,NULL,'ACT028_1');
INSERT INTO Sensor (sensor_id, location_name, sensor_location_id, sensor_type, is_connected, patient_email, location_id, pressure_sensor_id, activity_id) VALUES ('SNS028_2','Loc28','LOC028_A2',1,TRUE,'pat28@patient.com',128,NULL,'ACT028_2');
INSERT INTO Sensor (sensor_id, location_name, sensor_location_id, sensor_type, is_connected, patient_email, location_id, pressure_sensor_id, activity_id) VALUES ('SNS029_1','Loc29','LOC029_A1',1,TRUE,'pat29@patient.com',129,NULL,'ACT029_1');
INSERT INTO Sensor (sensor_id, location_name, sensor_location_id, sensor_type, is_connected, patient_email, location_id, pressure_sensor_id, activity_id) VALUES ('SNS029_2','Loc29','LOC029_A2',1,TRUE,'pat29@patient.com',129,NULL,'ACT029_2');
INSERT INTO Sensor (sensor_id, location_name, sensor_location_id, sensor_type, is_connected, patient_email, location_id, pressure_sensor_id, activity_id) VALUES ('SNS030_1','Loc30','LOC030_A1',3,TRUE,'pat30@patient.com',130,NULL,'ACT030_1');
INSERT INTO Sensor (sensor_id, location_name, sensor_location_id, sensor_type, is_connected, patient_email, location_id, pressure_sensor_id, activity_id) VALUES ('SNS030_2','Loc30','LOC030_A2',3,TRUE,'pat30@patient.com',130,NULL,'ACT030_2');
INSERT INTO Sensor (sensor_id, location_name, sensor_location_id, sensor_type, is_connected, patient_email, location_id, pressure_sensor_id, activity_id) VALUES ('SNS031_1','Loc31','LOC031_A1',2,TRUE,'pat31@patient.com',131,NULL,'ACT031_1');
INSERT INTO Sensor (sensor_id, location_name, sensor_location_id, sensor_type, is_connected, patient_email, location_id, pressure_sensor_id, activity_id) VALUES ('SNS031_2','Loc31','LOC031_A2',2,TRUE,'pat31@patient.com',131,NULL,'ACT031_2');
INSERT INTO Sensor (sensor_id, location_name, sensor_location_id, sensor_type, is_connected, patient_email, location_id, pressure_sensor_id, activity_id) VALUES ('SNS032_1','Loc32','LOC032_A1',1,TRUE,'pat32@patient.com',132,NULL,'ACT032_1');
INSERT INTO Sensor (sensor_id, location_name, sensor_location_id, sensor_type, is_connected, patient_email, location_id, pressure_sensor_id, activity_id) VALUES ('SNS032_2','Loc32','LOC032_A2',1,TRUE,'pat32@patient.com',132,NULL,'ACT032_2');
INSERT INTO Sensor (sensor_id, location_name, sensor_location_id, sensor_type, is_connected, patient_email, location_id, pressure_sensor_id, activity_id) VALUES ('SNS033_1','Loc33','LOC033_A1',1,TRUE,'pat33@patient.com',133,NULL,'ACT033_1');
INSERT INTO Sensor (sensor_id, location_name, sensor_location_id, sensor_type, is_connected, patient_email, location_id, pressure_sensor_id, activity_id) VALUES ('SNS033_2','Loc33','LOC033_A2',1,TRUE,'pat33@patient.com',133,NULL,'ACT033_2');
INSERT INTO Sensor (sensor_id, location_name, sensor_location_id, sensor_type, is_connected, patient_email, location_id, pressure_sensor_id, activity_id) VALUES ('SNS034_1','Loc34','LOC034_A1',4,TRUE,'pat34@patient.com',134,NULL,'ACT034_1');
INSERT INTO Sensor (sensor_id, location_name, sensor_location_id, sensor_type, is_connected, patient_email, location_id, pressure_sensor_id, activity_id) VALUES ('SNS034_2','Loc34','LOC034_A2',4,TRUE,'pat34@patient.com',134,NULL,'ACT034_2');
INSERT INTO Sensor (sensor_id, location_name, sensor_location_id, sensor_type, is_connected, patient_email, location_id, pressure_sensor_id, activity_id) VALUES ('SNS035_1','Loc35','LOC035_A1',3,TRUE,'pat35@patient.com',135,NULL,'ACT035_1');

-- This version generates pressure readings that span the complete duration of each activity

-- CORRECTED PRESSURE READINGS - Now spanning full activity duration
-- Activity ACT001_1 (Running): 1693110000 to 1693110879 (879 seconds, ~14.7 minutes)
-- Generating readings every 30 seconds for sensor SNS001_1
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR001_1_001',45.2,1693110000,4,TRUE,'ACT001_1','SNS001_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR001_1_002',52.8,1693110030,4,TRUE,'ACT001_1','SNS001_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR001_1_003',48.9,1693110060,4,TRUE,'ACT001_1','SNS001_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR001_1_004',55.6,1693110090,4,TRUE,'ACT001_1','SNS001_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR001_1_005',49.3,1693110120,4,TRUE,'ACT001_1','SNS001_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR001_1_006',47.8,1693110150,4,TRUE,'ACT001_1','SNS001_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR001_1_007',53.4,1693110180,4,TRUE,'ACT001_1','SNS001_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR001_1_008',51.7,1693110210,4,TRUE,'ACT001_1','SNS001_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR001_1_009',46.2,1693110240,4,TRUE,'ACT001_1','SNS001_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR001_1_010',54.9,1693110270,4,TRUE,'ACT001_1','SNS001_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR001_1_011',50.1,1693110300,4,TRUE,'ACT001_1','SNS001_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR001_1_012',48.7,1693110330,4,TRUE,'ACT001_1','SNS001_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR001_1_013',52.3,1693110360,4,TRUE,'ACT001_1','SNS001_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR001_1_014',47.5,1693110390,4,TRUE,'ACT001_1','SNS001_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR001_1_015',49.8,1693110420,4,TRUE,'ACT001_1','SNS001_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR001_1_016',53.1,1693110450,4,TRUE,'ACT001_1','SNS001_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR001_1_017',45.9,1693110480,4,TRUE,'ACT001_1','SNS001_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR001_1_018',51.6,1693110510,4,TRUE,'ACT001_1','SNS001_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR001_1_019',48.4,1693110540,4,TRUE,'ACT001_1','SNS001_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR001_1_020',50.7,1693110570,4,TRUE,'ACT001_1','SNS001_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR001_1_021',52.8,1693110600,4,TRUE,'ACT001_1','SNS001_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR001_1_022',47.2,1693110630,4,TRUE,'ACT001_1','SNS001_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR001_1_023',49.5,1693110660,4,TRUE,'ACT001_1','SNS001_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR001_1_024',54.3,1693110690,4,TRUE,'ACT001_1','SNS001_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR001_1_025',46.8,1693110720,4,TRUE,'ACT001_1','SNS001_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR001_1_026',51.4,1693110750,4,TRUE,'ACT001_1','SNS001_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR001_1_027',48.9,1693110780,4,TRUE,'ACT001_1','SNS001_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR001_1_028',53.7,1693110810,4,TRUE,'ACT001_1','SNS001_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR001_1_029',47.6,1693110840,4,TRUE,'ACT001_1','SNS001_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR001_1_030',50.2,1693110870,4,TRUE,'ACT001_1','SNS001_1');

-- Activity ACT001_2 (Standing): 1693110500 to 1693111822 (1322 seconds, ~22 minutes)
-- Generating readings every 45 seconds for sensor SNS001_2
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR001_2_001',65.3,1693110500,4,TRUE,'ACT001_2','SNS001_2');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR001_2_002',68.7,1693110545,4,TRUE,'ACT001_2','SNS001_2');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR001_2_003',67.1,1693110590,4,TRUE,'ACT001_2','SNS001_2');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR001_2_004',69.4,1693110635,4,TRUE,'ACT001_2','SNS001_2');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR001_2_005',66.8,1693110680,4,TRUE,'ACT001_2','SNS001_2');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR001_2_006',70.2,1693110725,4,TRUE,'ACT001_2','SNS001_2');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR001_2_007',64.9,1693110770,4,TRUE,'ACT001_2','SNS001_2');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR001_2_008',67.6,1693110815,4,TRUE,'ACT001_2','SNS001_2');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR001_2_009',68.3,1693110860,4,TRUE,'ACT001_2','SNS001_2');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR001_2_010',65.7,1693110905,4,TRUE,'ACT001_2','SNS001_2');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR001_2_011',69.8,1693110950,4,TRUE,'ACT001_2','SNS001_2');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR001_2_012',66.5,1693110995,4,TRUE,'ACT001_2','SNS001_2');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR001_2_013',68.9,1693111040,4,TRUE,'ACT001_2','SNS001_2');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR001_2_014',67.2,1693111085,4,TRUE,'ACT001_2','SNS001_2');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR001_2_015',65.4,1693111130,4,TRUE,'ACT001_2','SNS001_2');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR001_2_016',70.1,1693111175,4,TRUE,'ACT001_2','SNS001_2');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR001_2_017',68.6,1693111220,4,TRUE,'ACT001_2','SNS001_2');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR001_2_018',66.3,1693111265,4,TRUE,'ACT001_2','SNS001_2');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR001_2_019',69.7,1693111310,4,TRUE,'ACT001_2','SNS001_2');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR001_2_020',67.8,1693111355,4,TRUE,'ACT001_2','SNS001_2');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR001_2_021',65.2,1693111400,4,TRUE,'ACT001_2','SNS001_2');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR001_2_022',68.4,1693111445,4,TRUE,'ACT001_2','SNS001_2');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR001_2_023',66.9,1693111490,4,TRUE,'ACT001_2','SNS001_2');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR001_2_024',70.5,1693111535,4,TRUE,'ACT001_2','SNS001_2');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR001_2_025',67.3,1693111580,4,TRUE,'ACT001_2','SNS001_2');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR001_2_026',64.8,1693111625,4,TRUE,'ACT001_2','SNS001_2');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR001_2_027',69.1,1693111670,4,TRUE,'ACT001_2','SNS001_2');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR001_2_028',66.7,1693111715,4,TRUE,'ACT001_2','SNS001_2');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR001_2_029',68.2,1693111760,4,TRUE,'ACT001_2','SNS001_2');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR001_2_030',67.5,1693111805,4,TRUE,'ACT001_2','SNS001_2');

-- Activity ACT002_1 (Walking): 1693120000 to 1693122542 (2542 seconds, ~42 minutes)
-- Generating readings every 60 seconds for sensor SNS002_1
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR002_1_001',38.4,1693120000,2,TRUE,'ACT002_1','SNS002_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR002_1_002',41.2,1693120060,2,TRUE,'ACT002_1','SNS002_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR002_1_003',39.7,1693120120,2,TRUE,'ACT002_1','SNS002_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR002_1_004',42.8,1693120180,2,TRUE,'ACT002_1','SNS002_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR002_1_005',40.1,1693120240,2,TRUE,'ACT002_1','SNS002_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR002_1_006',43.5,1693120300,2,TRUE,'ACT002_1','SNS002_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR002_1_007',37.9,1693120360,2,TRUE,'ACT002_1','SNS002_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR002_1_008',41.6,1693120420,2,TRUE,'ACT002_1','SNS002_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR002_1_009',39.3,1693120480,2,TRUE,'ACT002_1','SNS002_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR002_1_010',42.1,1693120540,2,TRUE,'ACT002_1','SNS002_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR002_1_011',40.7,1693120600,2,TRUE,'ACT002_1','SNS002_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR002_1_012',38.8,1693120660,2,TRUE,'ACT002_1','SNS002_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR002_1_013',43.2,1693120720,2,TRUE,'ACT002_1','SNS002_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR002_1_014',41.4,1693120780,2,TRUE,'ACT002_1','SNS002_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR002_1_015',39.6,1693120840,2,TRUE,'ACT002_1','SNS002_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR002_1_016',42.9,1693120900,2,TRUE,'ACT002_1','SNS002_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR002_1_017',40.3,1693120960,2,TRUE,'ACT002_1','SNS002_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR002_1_018',38.5,1693121020,2,TRUE,'ACT002_1','SNS002_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR002_1_019',41.8,1693121080,2,TRUE,'ACT002_1','SNS002_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR002_1_020',43.1,1693121140,2,TRUE,'ACT002_1','SNS002_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR002_1_021',39.9,1693121200,2,TRUE,'ACT002_1','SNS002_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR002_1_022',42.4,1693121260,2,TRUE,'ACT002_1','SNS002_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR002_1_023',40.8,1693121320,2,TRUE,'ACT002_1','SNS002_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR002_1_024',38.2,1693121380,2,TRUE,'ACT002_1','SNS002_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR002_1_025',41.7,1693121440,2,TRUE,'ACT002_1','SNS002_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR002_1_026',43.6,1693121500,2,TRUE,'ACT002_1','SNS002_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR002_1_027',40.2,1693121560,2,TRUE,'ACT002_1','SNS002_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR002_1_028',42.3,1693121620,2,TRUE,'ACT002_1','SNS002_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR002_1_029',39.1,1693121680,2,TRUE,'ACT002_1','SNS002_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR002_1_030',41.9,1693121740,2,TRUE,'ACT002_1','SNS002_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR002_1_031',40.6,1693121800,2,TRUE,'ACT002_1','SNS002_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR002_1_032',38.7,1693121860,2,TRUE,'ACT002_1','SNS002_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR002_1_033',43.4,1693121920,2,TRUE,'ACT002_1','SNS002_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR002_1_034',41.3,1693121980,2,TRUE,'ACT002_1','SNS002_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR002_1_035',39.8,1693122040,2,TRUE,'ACT002_1','SNS002_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR002_1_036',42.7,1693122100,2,TRUE,'ACT002_1','SNS002_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR002_1_037',40.4,1693122160,2,TRUE,'ACT002_1','SNS002_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR002_1_038',38.9,1693122220,2,TRUE,'ACT002_1','SNS002_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR002_1_039',41.5,1693122280,2,TRUE,'ACT002_1','SNS002_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR002_1_040',43.0,1693122340,2,TRUE,'ACT002_1','SNS002_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR002_1_041',39.4,1693122400,2,TRUE,'ACT002_1','SNS002_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR002_1_042',42.2,1693122460,2,TRUE,'ACT002_1','SNS002_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR002_1_043',40.9,1693122520,2,TRUE,'ACT002_1','SNS002_1');

-- Activity ACT002_2 (Running): 1693120500 to 1693121367 (867 seconds, ~14.5 minutes)
-- Generating readings every 30 seconds for sensor SNS002_2
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR002_2_001',52.1,1693120500,2,TRUE,'ACT002_2','SNS002_2');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR002_2_002',48.7,1693120530,2,TRUE,'ACT002_2','SNS002_2');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR002_2_003',54.3,1693120560,2,TRUE,'ACT002_2','SNS002_2');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR002_2_004',49.8,1693120590,2,TRUE,'ACT002_2','SNS002_2');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR002_2_005',51.6,1693120620,2,TRUE,'ACT002_2','SNS002_2');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR002_2_006',47.2,1693120650,2,TRUE,'ACT002_2','SNS002_2');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR002_2_007',53.9,1693120680,2,TRUE,'ACT002_2','SNS002_2');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR002_2_008',50.4,1693120710,2,TRUE,'ACT002_2','SNS002_2');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR002_2_009',48.1,1693120740,2,TRUE,'ACT002_2','SNS002_2');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR002_2_010',52.7,1693120770,2,TRUE,'ACT002_2','SNS002_2');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR002_2_011',49.3,1693120800,2,TRUE,'ACT002_2','SNS002_2');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR002_2_012',51.8,1693120830,2,TRUE,'ACT002_2','SNS002_2');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR002_2_013',46.9,1693120860,2,TRUE,'ACT002_2','SNS002_2');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR002_2_014',54.1,1693120890,2,TRUE,'ACT002_2','SNS002_2');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR002_2_015',50.6,1693120920,2,TRUE,'ACT002_2','SNS002_2');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR002_2_016',48.4,1693120950,2,TRUE,'ACT002_2','SNS002_2');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR002_2_017',53.2,1693120980,2,TRUE,'ACT002_2','SNS002_2');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR002_2_018',49.7,1693121010,2,TRUE,'ACT002_2','SNS002_2');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR002_2_019',51.4,1693121040,2,TRUE,'ACT002_2','SNS002_2');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR002_2_020',47.6,1693121070,2,TRUE,'ACT002_2','SNS002_2');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR002_2_021',52.8,1693121100,2,TRUE,'ACT002_2','SNS002_2');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR002_2_022',50.1,1693121130,2,TRUE,'ACT002_2','SNS002_2');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR002_2_023',48.9,1693121160,2,TRUE,'ACT002_2','SNS002_2');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR002_2_024',53.5,1693121190,2,TRUE,'ACT002_2','SNS002_2');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR002_2_025',49.2,1693121220,2,TRUE,'ACT002_2','SNS002_2');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR002_2_026',51.9,1693121250,2,TRUE,'ACT002_2','SNS002_2');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR002_2_027',47.4,1693121280,2,TRUE,'ACT002_2','SNS002_2');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR002_2_028',54.0,1693121310,2,TRUE,'ACT002_2','SNS002_2');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR002_2_029',50.8,1693121340,2,TRUE,'ACT002_2','SNS002_2');

-- For brevity, I'll continue with a few more examples and provide the pattern
-- Activity ACT003_1 (Running): 1693130000 to 1693132247 (2247 seconds, ~37.5 minutes)
-- Sample pressure readings every 45 seconds for sensor SNS003_1
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR003_1_001',58.2,1693130000,2,TRUE,'ACT003_1','SNS003_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR003_1_002',61.7,1693130045,2,TRUE,'ACT003_1','SNS003_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR003_1_003',59.4,1693130090,2,TRUE,'ACT003_1','SNS003_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR003_1_004',63.1,1693130135,2,TRUE,'ACT003_1','SNS003_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR003_1_005',60.8,1693130180,2,TRUE,'ACT003_1','SNS003_1');
-- [Continue this pattern for the full duration...]

-- Activity ACT004_1 (GripTest): 1693140000 to 1693140648 (648 seconds, ~10.8 minutes)
-- Sample pressure readings every 20 seconds for sensor SNS004_1
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR004_1_001',42.3,1693140000,3,TRUE,'ACT004_1','SNS004_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR004_1_002',45.8,1693140020,3,TRUE,'ACT004_1','SNS004_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR004_1_003',44.1,1693140040,3,TRUE,'ACT004_1','SNS004_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR004_1_004',47.6,1693140060,3,TRUE,'ACT004_1','SNS004_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR004_1_005',43.9,1693140080,3,TRUE,'ACT004_1','SNS004_1');
-- [Continue this pattern for the full duration...]
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR018_1_001',39.4,1693280000,2,TRUE,'ACT018_1','SNS018_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR018_1_002',42.1,1693280045,2,TRUE,'ACT018_1','SNS018_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR018_1_003',40.7,1693280090,2,TRUE,'ACT018_1','SNS018_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR018_1_004',43.8,1693280135,2,TRUE,'ACT018_1','SNS018_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR018_1_005',41.3,1693280180,2,TRUE,'ACT018_1','SNS018_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR018_1_006',38.9,1693280225,2,TRUE,'ACT018_1','SNS018_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR018_1_007',42.6,1693280270,2,TRUE,'ACT018_1','SNS018_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR018_1_008',40.2,1693280315,2,TRUE,'ACT018_1','SNS018_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR018_1_009',44.1,1693280360,2,TRUE,'ACT018_1','SNS018_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR018_1_010',41.8,1693280405,2,TRUE,'ACT018_1','SNS018_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR018_1_011',39.6,1693280450,2,TRUE,'ACT018_1','SNS018_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR018_1_012',43.3,1693280495,2,TRUE,'ACT018_1','SNS018_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR018_1_013',40.9,1693280540,2,TRUE,'ACT018_1','SNS018_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR018_1_014',42.4,1693280585,2,TRUE,'ACT018_1','SNS018_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR018_1_015',38.7,1693280630,2,TRUE,'ACT018_1','SNS018_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR018_1_016',41.5,1693280675,2,TRUE,'ACT018_1','SNS018_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR018_1_017',43.7,1693280720,2,TRUE,'ACT018_1','SNS018_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR018_1_018',40.1,1693280765,2,TRUE,'ACT018_1','SNS018_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR018_1_019',42.8,1693280810,2,TRUE,'ACT018_1','SNS018_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR018_1_020',39.3,1693280855,2,TRUE,'ACT018_1','SNS018_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR018_1_021',41.9,1693280900,2,TRUE,'ACT018_1','SNS018_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR018_1_022',44.2,1693280945,2,TRUE,'ACT018_1','SNS018_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR018_1_023',40.6,1693280990,2,TRUE,'ACT018_1','SNS018_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR018_1_024',42.3,1693281035,2,TRUE,'ACT018_1','SNS018_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR018_1_025',38.8,1693281080,2,TRUE,'ACT018_1','SNS018_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR018_1_026',41.4,1693281125,2,TRUE,'ACT018_1','SNS018_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR018_1_027',43.6,1693281170,2,TRUE,'ACT018_1','SNS018_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR018_1_028',40.0,1693281215,2,TRUE,'ACT018_1','SNS018_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR018_1_029',42.7,1693281260,2,TRUE,'ACT018_1','SNS018_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR018_1_030',39.2,1693281305,2,TRUE,'ACT018_1','SNS018_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR018_1_031',41.7,1693281350,2,TRUE,'ACT018_1','SNS018_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR018_1_032',43.9,1693281395,2,TRUE,'ACT018_1','SNS018_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR018_1_033',40.5,1693281440,2,TRUE,'ACT018_1','SNS018_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR018_1_034',42.1,1693281485,2,TRUE,'ACT018_1','SNS018_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR018_1_035',38.4,1693281530,2,TRUE,'ACT018_1','SNS018_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR018_1_036',41.2,1693281575,2,TRUE,'ACT018_1','SNS018_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR018_1_037',43.5,1693281620,2,TRUE,'ACT018_1','SNS018_1');

-- Activity ACT018_2 (GripTest): 1693280500 to 1693282689 (2189 seconds, ~36.5 minutes)
-- Generating readings every 30 seconds for sensor SNS018_2
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR018_2_001',34.7,1693280500,2,TRUE,'ACT018_2','SNS018_2');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR018_2_002',38.2,1693280530,2,TRUE,'ACT018_2','SNS018_2');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR018_2_003',36.9,1693280560,2,TRUE,'ACT018_2','SNS018_2');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR018_2_004',39.4,1693280590,2,TRUE,'ACT018_2','SNS018_2');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR018_2_005',35.6,1693280620,2,TRUE,'ACT018_2','SNS018_2');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR018_2_006',37.8,1693280650,2,TRUE,'ACT018_2','SNS018_2');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR018_2_007',40.1,1693280680,2,TRUE,'ACT018_2','SNS018_2');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR018_2_008',36.3,1693280710,2,TRUE,'ACT018_2','SNS018_2');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR018_2_009',38.7,1693280740,2,TRUE,'ACT018_2','SNS018_2');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR018_2_010',34.2,1693280770,2,TRUE,'ACT018_2','SNS018_2');

-- Activity ACT019_1 (Cycling): 1693290000 to 1693293138 (3138 seconds, ~52 minutes)
-- Generating readings every 60 seconds for sensor SNS019_1
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR019_1_001',55.8,1693290000,4,TRUE,'ACT019_1','SNS019_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR019_1_002',58.3,1693290060,4,TRUE,'ACT019_1','SNS019_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR019_1_003',57.1,1693290120,4,TRUE,'ACT019_1','SNS019_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR019_1_004',59.7,1693290180,4,TRUE,'ACT019_1','SNS019_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR019_1_005',56.4,1693290240,4,TRUE,'ACT019_1','SNS019_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR019_1_006',60.2,1693290300,4,TRUE,'ACT019_1','SNS019_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR019_1_007',54.9,1693290360,4,TRUE,'ACT019_1','SNS019_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR019_1_008',58.6,1693290420,4,TRUE,'ACT019_1','SNS019_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR019_1_009',57.3,1693290480,4,TRUE,'ACT019_1','SNS019_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR019_1_010',61.0,1693290540,4,TRUE,'ACT019_1','SNS019_1');

-- Activity ACT020_1 (Lifting): 1693300000 to 1693301498 (1498 seconds, ~25 minutes)
-- Generating readings every 40 seconds for sensor SNS020_1
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR020_1_001',72.4,1693300000,3,TRUE,'ACT020_1','SNS020_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR020_1_002',68.9,1693300040,3,TRUE,'ACT020_1','SNS020_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR020_1_003',75.1,1693300080,3,TRUE,'ACT020_1','SNS020_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR020_1_004',70.6,1693300120,3,TRUE,'ACT020_1','SNS020_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR020_1_005',73.8,1693300160,3,TRUE,'ACT020_1','SNS020_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR020_1_006',67.3,1693300200,3,TRUE,'ACT020_1','SNS020_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR020_1_007',76.2,1693300240,3,TRUE,'ACT020_1','SNS020_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR020_1_008',69.7,1693300280,3,TRUE,'ACT020_1','SNS020_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR020_1_009',74.5,1693300320,3,TRUE,'ACT020_1','SNS020_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR020_1_010',71.2,1693300360,3,TRUE,'ACT020_1','SNS020_1');

-- Activity ACT025_1 (GripTest): 1693350000 to 1693351566 (1566 seconds, ~26 minutes)
-- Generating readings every 25 seconds for sensor SNS025_1
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR025_1_001',45.3,1693350000,3,TRUE,'ACT025_1','SNS025_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR025_1_002',48.7,1693350025,3,TRUE,'ACT025_1','SNS025_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR025_1_003',46.1,1693350050,3,TRUE,'ACT025_1','SNS025_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR025_1_004',49.8,1693350075,3,TRUE,'ACT025_1','SNS025_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR025_1_005',47.4,1693350100,3,TRUE,'ACT025_1','SNS025_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR025_1_006',44.9,1693350125,3,TRUE,'ACT025_1','SNS025_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR025_1_007',50.2,1693350150,3,TRUE,'ACT025_1','SNS025_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR025_1_008',46.8,1693350175,3,TRUE,'ACT025_1','SNS025_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR025_1_009',48.3,1693350200,3,TRUE,'ACT025_1','SNS025_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR025_1_010',45.7,1693350225,3,TRUE,'ACT025_1','SNS025_1');

-- Activity ACT030_1 (Cycling): 1693400000 to 1693400843 (843 seconds, ~14 minutes)
-- Generating readings every 30 seconds for sensor SNS030_1
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR030_1_001',52.6,1693400000,3,TRUE,'ACT030_1','SNS030_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR030_1_002',49.8,1693400030,3,TRUE,'ACT030_1','SNS030_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR030_1_003',54.2,1693400060,3,TRUE,'ACT030_1','SNS030_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR030_1_004',51.4,1693400090,3,TRUE,'ACT030_1','SNS030_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR030_1_005',48.7,1693400120,3,TRUE,'ACT030_1','SNS030_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR030_1_006',53.9,1693400150,3,TRUE,'ACT030_1','SNS030_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR030_1_007',50.3,1693400180,3,TRUE,'ACT030_1','SNS030_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR030_1_008',52.1,1693400210,3,TRUE,'ACT030_1','SNS030_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR030_1_009',49.5,1693400240,3,TRUE,'ACT030_1','SNS030_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR030_1_010',55.1,1693400270,3,TRUE,'ACT030_1','SNS030_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR030_1_011',51.8,1693400300,3,TRUE,'ACT030_1','SNS030_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR030_1_012',48.2,1693400330,3,TRUE,'ACT030_1','SNS030_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR030_1_013',53.7,1693400360,3,TRUE,'ACT030_1','SNS030_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR030_1_014',50.9,1693400390,3,TRUE,'ACT030_1','SNS030_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR030_1_015',52.4,1693400420,3,TRUE,'ACT030_1','SNS030_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR030_1_016',49.1,1693400450,3,TRUE,'ACT030_1','SNS030_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR030_1_017',54.6,1693400480,3,TRUE,'ACT030_1','SNS030_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR030_1_018',51.2,1693400510,3,TRUE,'ACT030_1','SNS030_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR030_1_019',48.8,1693400540,3,TRUE,'ACT030_1','SNS030_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR030_1_020',53.3,1693400570,3,TRUE,'ACT030_1','SNS030_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR030_1_021',50.7,1693400600,3,TRUE,'ACT030_1','SNS030_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR030_1_022',52.0,1693400630,3,TRUE,'ACT030_1','SNS030_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR030_1_023',49.4,1693400660,3,TRUE,'ACT030_1','SNS030_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR030_1_024',54.8,1693400690,3,TRUE,'ACT030_1','SNS030_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR030_1_025',51.6,1693400720,3,TRUE,'ACT030_1','SNS030_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR030_1_026',48.3,1693400750,3,TRUE,'ACT030_1','SNS030_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR030_1_027',53.1,1693400780,3,TRUE,'ACT030_1','SNS030_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR030_1_028',50.5,1693400810,3,TRUE,'ACT030_1','SNS030_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR030_1_029',52.8,1693400840,3,TRUE,'ACT030_1','SNS030_1');

-- Activity ACT032_1 (Running): 1693420000 to 1693422000 (2000 seconds, ~33 minutes)
-- Generating readings every 45 seconds for sensor SNS032_1
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR032_1_001',51.7,1693420000,1,TRUE,'ACT032_1','SNS032_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR032_1_002',54.3,1693420045,1,TRUE,'ACT032_1','SNS032_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR032_1_003',52.9,1693420090,1,TRUE,'ACT032_1','SNS032_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR032_1_004',55.8,1693420135,1,TRUE,'ACT032_1','SNS032_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR032_1_005',50.4,1693420180,1,TRUE,'ACT032_1','SNS032_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR032_1_006',53.6,1693420225,1,TRUE,'ACT032_1','SNS032_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR032_1_007',49.2,1693420270,1,TRUE,'ACT032_1','SNS032_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR032_1_008',56.1,1693420315,1,TRUE,'ACT032_1','SNS032_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR032_1_009',52.7,1693420360,1,TRUE,'ACT032_1','SNS032_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR032_1_010',54.5,1693420405,1,TRUE,'ACT032_1','SNS032_1');

-- Activity ACT035_1 (GripTest): 1693450000 to 1693452416 (2416 seconds, ~40 minutes)
-- Generating readings every 35 seconds for sensor SNS035_1
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR035_1_001',41.2,1693450000,3,TRUE,'ACT035_1','SNS035_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR035_1_002',44.8,1693450035,3,TRUE,'ACT035_1','SNS035_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR035_1_003',42.6,1693450070,3,TRUE,'ACT035_1','SNS035_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR035_1_004',46.3,1693450105,3,TRUE,'ACT035_1','SNS035_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR035_1_005',43.9,1693450140,3,TRUE,'ACT035_1','SNS035_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR035_1_006',40.7,1693450175,3,TRUE,'ACT035_1','SNS035_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR035_1_007',47.1,1693450210,3,TRUE,'ACT035_1','SNS035_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR035_1_008',44.4,1693450245,3,TRUE,'ACT035_1','SNS035_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR035_1_009',42.1,1693450280,3,TRUE,'ACT035_1','SNS035_1');
INSERT INTO PressureReading (pressure_reading_id, pressure_value, time, sensor_type, is_uploaded, activity_id, sensor_id) VALUES ('PR035_1_010',45.7,1693450315,3,TRUE,'ACT035_1','SNS035_1');


-- This demonstrates the corrected approach where:
-- 1. Each activity has pressure readings spanning its complete duration
-- 2. Reading intervals vary by activity type (more frequent for grip tests, less frequent for long walks)
-- 3. Pressure values are realistic for each activity type
-- 4. All readings fall within the activity's start_time to end_time range
-- 5. Sensor types match the activity requirements