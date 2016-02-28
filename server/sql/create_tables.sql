-- Create a new instance of the database

DROP DATABASE IF EXISTS hoot;
CREATE SCHEMA IF NOT EXISTS hoot;
USE hoot;

CREATE TABLE item(
    category varchar(100) NOT NULL,
    id varchar(100) NOT NULL,
    name varchar(500),
    token varchar(100),
    urls varchar(2500), 
    PRIMARY KEY(category,id)
);

CREATE TABLE review(
    id int NOT NULL, 
    item_category varchar(100) NOT NULL,
    item_id varchar(100) NOT NULL, 
    is_positive boolean,
    comment_token varchar(100),
    PRIMARY KEY(id)
);

CREATE TABLE item_tag(
    id int NOT NULL, 
    tag varchar(50),
    item_category varchar(100) NOT NULL,
    item_id varchar(100) NOT NULL, 
    PRIMARY KEY(id)
);

CREATE TABLE comment_tag(
    id int NOT NULL, 
    tag varchar(50), 
    comment_id int NOT NULL, 
    PRIMARY KEY(id)
);

