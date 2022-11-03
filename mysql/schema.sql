-- CREATE DATABASE
DROP DATABASE IF EXISTS secrets_db;
CREATE DATABASE secrets_db;
USE secrets_db;

-- CREATE TABLE
DROP TABLE IF EXISTS secrets;
CREATE TABLE secrets (
    id INT NOT NULL AUTO_INCREMENT,
    url VARCHAR(255) NOT NULL,
    user VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,

    PRIMARY KEY(id)
);

-- INSERT EXAMPLE
INSERT INTO secrets(url, user, password)
VALUES ("test.com", "my_test", "test123");
