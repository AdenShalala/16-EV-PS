CREATE TABLE IF NOT EXISTS Clinician (
    clinician_id   VARCHAR(50)  PRIMARY KEY,
    first_name           VARCHAR(100) NOT NULL,
    last_name            VARCHAR(100) NOT NULL,
    email          VARCHAR(100) NOT NULL UNIQUE,
    password_hash  VARCHAR(255) NOT NULL
);