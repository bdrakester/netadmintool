DROP TABLE IF EXISTS device_types CASCADE;
DROP TABLE IF EXISTS devices;
DROP TABLE IF EXISTS roles CASCADE;
DROP TABLE IF EXISTS users;

CREATE TABLE device_types (
  id SERIAL PRIMARY KEY,
  make VARCHAR NOT NULL,
  model VARCHAR NOT NULL,
  code VARCHAR NOT NULL UNIQUE
);

CREATE TABLE devices (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    ip_addr INET NOT NULL,
    device_type_id INTEGER REFERENCES device_types,
    sw_version VARCHAR NOT NULL,
    serial_number VARCHAR NOT NULL,
    datacenter VARCHAR NOT NULL,
    location VARCHAR NOT NULL,
    console VARCHAR,
    description VARCHAR,
    notes VARCHAR
);

CREATE TABLE roles (
  id SERIAL PRIMARY KEY,
  role_name VARCHAR NOT NULL UNIQUE
);

CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username VARCHAR NOT NULL UNIQUE,
  password VARCHAR NOT NULL,
  display_name VARCHAR NOT NULL,
  role_id INTEGER REFERENCES roles
);

INSERT INTO roles (role_name) VALUES ('admin');
INSERT INTO roles (role_name) VALUES ('readonly');

INSERT INTO device_types(make, model, code) VALUES ('Cisco', 'ASA 5555-X', 'cisco_asa');
INSERT INTO device_types(make, model, code) VALUES ('Cisco', '2951', 'cisco_ios');
INSERT INTO device_types(make, model, code) VALUES ('Cisco', 'SG300', 'cisco_s300');
