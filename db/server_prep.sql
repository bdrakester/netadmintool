# Created database netadmintool
# Created user natooldbuser

GRANT ALL PRIVILEGES ON DATABASE netadmintool to natooldbuser;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO natooldbuser;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO natooldbuser;

# Or Just make it the owner
ALTER DATABASE netadmintool OWNER TO natooldbuser;
