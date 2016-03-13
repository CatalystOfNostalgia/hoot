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
    number_of_comments int NOT NULL,
    PRIMARY KEY (media_id)
);

CREATE TABLE multimediaemotions (
    media_id int NOT NULL,
    pleasantness double NOT NULL,
    attention double NOT NULL,
    sensitivity double NOT NULL,
    aptitude double NOT NULL,
    polarity double NOT NULL,
    PRIMARY KEY (media_id)
    FOREIGN KEY (media_id) REFERENCES multimedia(media_id)
);

CREATE TABLE comments (
    comment_id int NOT NULL AUTO_INCREMENT,
    item_id int NOT NULL,
    PRIMARY KEY (comment_id),
    FOREIGN KEY (item_id) REFERENCES multimedia(media_id)
);

CREATE TABLE commentemotions (
    comment_id int NOT NULL,
    relevancy_score int NOT NULL,
    pleasantness double NOT NULL,
    attention double NOT NULL,
    sensitivity double NOT NULL,
    aptitude double NOT NULL,
    polarity double NOT NULL,
    PRIMARY KEY (comment_id),
    FOREIGN KEY (comment_id) REFERENCES comments(comment_id)

);

-- Triggers

-- update number of comments for a media whenever a comment is inserted
delimiter |

CREATE TRIGGER update_num_comments AFTER INSERT ON comments
    FOR EACH ROW
    BEGIN
        UPDATE multimedia SET number_of_comments = number_of_comments + 1 WHERE media_id = NEW.item_id;
    END;

|
