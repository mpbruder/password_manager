-- CREATE DATABASE
DROP DATABASE IF EXISTS secrets_db;
CREATE DATABASE secrets_db;
USE secrets_db;

-- CREATE TABLE secrets
DROP TABLE IF EXISTS secrets;
CREATE TABLE secrets (
    id INT NOT NULL AUTO_INCREMENT,
    url VARCHAR(255) NOT NULL,
    user VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,

    PRIMARY KEY(id)
);

-- CREATE TABLE auth
DROP TABLE IF EXISTS auth;
CREATE TABLE auth (
    id INT NOT NULL AUTO_INCREMENT,
    status int NOT NULL,
    master_password VARCHAR(255) NULL,

    PRIMARY KEY(id)
);

-- INSERT secrets EXAMPLE
INSERT INTO secrets(url, user, password)
VALUES ("test.com", "my_test", "test123");

-- INSERT secrets EXAMPLE
INSERT INTO auth(status, master_password)
VALUES (0, "");
