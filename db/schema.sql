CREATE TABLE devices (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    device_type VARCHAR NOT NULL,
    description VARCHAR
);

ALTER TABLE devices ADD ip_addr INET;
