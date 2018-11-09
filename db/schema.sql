CREATE TABLE devices (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    ip_addr INET NOT NULL,
    device_type VARCHAR NOT NULL,
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

ALTER TABLE devices DROP COLUMN device_type;
