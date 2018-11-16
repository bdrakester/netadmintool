/* Testing postgresql database setup.
 * Creates a test database, and test user as the owner.
*/
CREATE ROLE testuser WITH ENCRYPTED PASSWORD '<password>';
CREATE DATABASE test_netadmin OWNER = testuser;
ALTER ROLE "testuser" WITH LOGIN;

/* I ran schema.sql on the test database, and it ended up recreating tables
 * with a different own.  Ran this command to change owner of tables back
 * to testuser
 */
  ALTER TABLE devices OWNER TO testuser;
  ALTER TABLE roles OWNER TO testuser;
  ALTER TABLE users OWNER TO testuser;
