-- Create a new instance of the database

DROP DATABASE IF EXISTS hoot;
CREATE SCHEMA IF NOT EXISTS hoot;
USE hoot;

CREATE TABLE multimedia (
    media_id int NOT NULL AUTO_INCREMENT,
    title varchar(100) NOT NULL,
    creator varchar(100) NOT NULL,
    description varchar (100),
    number_of_comments int NOT NULL,
    pleasantness double NOT NULL,
    attention double NOT NULL,
    sensitivity double NOT NULL,
    aptitude double NOT NULL,
    polarity double NOT NULL,
    PRIMARY KEY (media_id)
);

CREATE TABLE comments (
    comment_id int NOT NULL AUTO_INCREMENT,
    item_id int NOT NULL,
    relevancy_score int NOT NULL,
    pleasantness double NOT NULL,
    attention double NOT NULL,
    sensitivity double NOT NULL,
    apitude double NOT NULL,
    polarity double NOT NULL,
    PRIMARY KEY (comment_id),
    FOREIGN KEY (item_id) REFERENCES multimedia(media_id)
);
