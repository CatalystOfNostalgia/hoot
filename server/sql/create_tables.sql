-- Create a new instance of the database

DROP DATABASE IF EXISTS hoot;
CREATE SCHEMA IF NOT EXISTS hoot;
USE hoot;

CREATE TABLE multimedia (
    media_id int NOT NULL AUTO_INCREMENT,
    title varchar(100) NOT NULL,
    creator varchar(100) NOT NULL,
    description varchar (1000),
    media_type varchar (100) NOT NULL,
    asin varchar (20) NOT NULL UNIQUE,
    number_of_comments int NOT NULL DEFAULT 0,
    last_updated int NOT NULL,
    PRIMARY KEY (media_id)
);

CREATE TABLE multimedia_emotions (
    media_id int NOT NULL,
    emotion varchar(50) NOT NULL,
    PRIMARY KEY (media_id, emotion),
    FOREIGN KEY (media_id) REFERENCES multimedia(media_id)
);

CREATE TABLE comments (
    comment_id int NOT NULL AUTO_INCREMENT,
    comment_date int NOT NULL,
    item_id int NOT NULL,
    relevancy double NOT NULL,
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

CREATE TRIGGER decrement_num_comments AFTER DELETE ON comments
    FOR EACH ROW
    BEGIN
        UPDATE multimedia SET number_of_comments = number_of_comments - 1 WHERE media_id = OLD.item_id;
    END;

|

delimiter ;
