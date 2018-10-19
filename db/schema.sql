CREATE TABLE devices (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    device_type VARCHAR NOT NULL,
    description VARCHAR
);

ALTER TABLE devices ADD ip_addr INET;
ALTER TABLE devices ADD make VARCHAR;
ALTER TABLE devices ADD model VARCHAR;
ALTER TABLE devices ADD sw_version VARCHAR;
ALTER TABLE devices ADD serial_number VARCHAR;
ALTER TABLE devices ADD datacenter VARCHAR;
ALTER TABLE devices ADD location VARCHAR;
ALTER TABLE devices ADD console VARCHAR;
ALTER TABLE devices ADD notes VARCHAR;
