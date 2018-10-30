/* Testing postgresql database setup.
 * Creates a test database, and test user as the owner.
*/
CREATE ROLE testuser WITH ENCRYPTED PASSWORD '<password>';
CREATE DATABASE test_netadmin OWNER = testuser;
ALTER ROLE "testuser" WITH LOGIN;
