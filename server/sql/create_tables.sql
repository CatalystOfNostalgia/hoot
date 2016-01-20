-- Create a new instance of the database

DROP DATABASE IF EXISTS hoot;
CREATE SCHEMA IF NOT EXISTS hoot;
USE hoot;

CREATE TABLE user(
    user_id int NOT NULL AUTO_INCREMENT, 
    name varchar(100) NOT NULL
);
