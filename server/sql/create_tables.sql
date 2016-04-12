-- Create a new instance of the database

DROP DATABASE IF EXISTS hoot;
CREATE SCHEMA IF NOT EXISTS hoot;
USE hoot;

CREATE TABLE multimedia (
    media_id int NOT NULL AUTO_INCREMENT,
    title varchar(100) NOT NULL,
    creator varchar(100) NOT NULL,
    description varchar (100),
    media_type varchar (100) NOT NULL,
    genre varchar (100) NOT NULL,
    asin varchar (20) NOT NULL UNIQUE,
    number_of_comments int NOT NULL DEFAULT 0,
    PRIMARY KEY (media_id)
);

CREATE TABLE multimedia_emotions (
    media_id int NOT NULL AUTO_INCREMENT,
    pleasantness double,
    attention double,
    sensitivity double,
    aptitude double,
    polarity double,
    PRIMARY KEY (media_id),
    FOREIGN KEY (media_id) REFERENCES multimedia(media_id)
);

CREATE TABLE comments (
    comment_id int NOT NULL AUTO_INCREMENT,
    item_id int NOT NULL,
    elevancy_score int NOT NULL,
    pleasantness double NOT NULL,
    attention double NOT NULL,
    sensitivity double NOT NULL,
    aptitude double NOT NULL,
    polarity double NOT NULL,
    PRIMARY KEY (comment_id),
    FOREIGN KEY (item_id) REFERENCES multimedia(media_id)
);

-- Triggers

delimiter |

-- update number of comments for a media whenever a comment is inserted
CREATE TRIGGER update_num_comments AFTER INSERT ON comments
    FOR EACH ROW
    BEGIN
        UPDATE multimedia SET number_of_comments = number_of_comments + 1 WHERE media_id = NEW.item_id;
    END;

|

-- new media entry -> new media_emotion entry
CREATE TRIGGER add_multimedia_emotions AFTER INSERT ON multimedia
    FOR EACH ROW
    BEGIN
        INSERT INTO multimedia_emotions () VALUES ();
    END;

|
            

delimiter ;
