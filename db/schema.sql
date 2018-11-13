CREATE TABLE devices (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    ip_addr INET NOT NULL,
    make VARCHAR NOT NULL,
    model VARCHAR NOT NULL,
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
