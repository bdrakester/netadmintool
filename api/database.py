#!/usr/local/bin/python3

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from configparser import ConfigParser


class NetAdminToolDB:
    """
    Database interface
    """

    def __init__(self, configFile):
        config = ConfigParser()
        config.read(configFile)

        dbuser = config['DATABASE']['dbusername']
        dbpass = config['DATABASE']['dbpassword']
        dbhost = config['DATABASE']['hostname']
        dbport = config['DATABASE']['port']
        dbname = config['DATABASE']['dbname']

        connString = f"postgresql://{dbuser}:{dbpass}@{dbhost}:{dbport}/{dbname}"
        self.dbname = dbname
        self.engine = create_engine(connString)
        self.db = scoped_session(sessionmaker(bind=self.engine))

    def add_device(self, name, ip_addr, make, model,
        sw_version, serial_number, datacenter, location, console="",
        description="", notes=""):
        """
        Add a Device, returns the new device's id.
        """
        result = self.db.execute("INSERT INTO devices \
                                (name, ip_addr, make, model, \
                                sw_version, serial_number, datacenter, \
                                location, console, description, notes) \
                                VALUES (:name, :ip_addr, :make, \
                                :model, :ver, :serial_num, :datacenter, \
                                :loc, :con, :descr, :notes)  RETURNING id",
                                {'name': name, 'ip_addr': ip_addr, 'make': make,
                                'model': model, 'ver': sw_version,
                                'serial_num': serial_number,
                                'datacenter': datacenter, 'loc': location,
                                'con': console, 'descr': description,
                                'notes': notes})

        self.db.commit()

        return result.fetchone().id


    def get_device(self, id=0):
        """
        Returns a dictionary of device with id. If id is not provided,
        returns a list of dictionaries of all devices in database
        """
        if id != 0:
            device = self.db.execute("SELECT * FROM devices WHERE id = :id",
                                    {'id': id}).fetchone()
        else:
            device = self.db.execute("SELECT * FROM devices").fetchall()

        # Added Commit to avoid crash with error.
        # "QueuePool limit of size 5 overflow 10 reached, connection timed out,
        # timeout 30"
        # Is there a better way?  Just need to free connection , not commit
        # changes?
        self.db.commit()
        return device

    def get_device_name(self, name):
        """
        Returns first device with name
        """
        device = self.db.execute("SELECT * FROM devices WHERE name = :name",
                            {'name': name }).fetchone()

        # Add commit to avoid crash - see get_device(self,id=0) comments
        self.db.commit()
        return device

    def update_device(self, id, **updates):
        """
        Update device with id with named arguments
        """

        for key, value in updates.items():
            if key == 'name':
                self.db.execute('UPDATE devices SET name = :value \
                                WHERE id = :id',
                                {'value': value, 'id':id})
            if key == 'ip_addr':
                self.db.execute('UPDATE devices SET ip_addr = :value \
                                WHERE id = :id',
                                {'value': value, 'id':id})
            if key == 'make':
                self.db.execute('UPDATE devices SET make = :value \
                                WHERE id = :id',
                                {'value': value, 'id':id})
            if key == 'model':
                self.db.execute('UPDATE devices SET model = :value \
                                WHERE id = :id',
                                {'value': value, 'id':id})
            if key == 'sw_version':
                self.db.execute('UPDATE devices SET sw_version = :value \
                                WHERE id = :id',
                                {'value': value, 'id':id})
            if key == 'serial_number':
                self.db.execute('UPDATE devices SET serial_number = :value \
                                WHERE id = :id',
                                {'value': value, 'id':id})
            if key == 'datacenter':
                self.db.execute('UPDATE devices SET datacenter = :value \
                                WHERE id = :id',
                                {'value': value, 'id':id})
            if key == 'location':
                self.db.execute('UPDATE devices SET location = :value \
                                WHERE id = :id',
                                {'value': value, 'id':id})
            if key == 'console':
                self.db.execute('UPDATE devices SET console = :value \
                                WHERE id = :id',
                                {'value': value, 'id':id})
            if key == 'description':
                self.db.execute('UPDATE devices SET description = :value \
                                WHERE id = :id',
                                {'value': value, 'id':id})
            if key == 'notes':
                self.db.execute('UPDATE devices SET notes = :value \
                                WHERE id = :id',
                                {'value': value, 'id':id})

        self.db.commit()


    def delete_device(self, id):
        """
        Delete device id from that database
        """
        self.db.execute("DELETE FROM devices WHERE id = :id", {'id': id})
        self.db.commit()


    def create_tables(self):
        """
        Recreate database tables
        """

        self.db.execute('DROP TABLE IF EXISTS devices')

        self.db.execute('CREATE TABLE devices ( \
            id SERIAL PRIMARY KEY, \
            name VARCHAR NOT NULL, \
            ip_addr INET NOT NULL, \
            make VARCHAR NOT NULL, \
            model VARCHAR NOT NULL, \
            sw_version VARCHAR NOT NULL, \
            serial_number VARCHAR NOT NULL, \
            datacenter VARCHAR NOT NULL, \
            location VARCHAR NOT NULL, \
            console VARCHAR, \
            description VARCHAR, \
            notes VARCHAR)')

        self.db.commit()
