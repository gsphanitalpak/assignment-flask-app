CREATE DATABASE gov_data;

USE gov_data;

CREATE TABLE pib_releases (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title TEXT,
    summary TEXT,
    publication_date DATETIME,
    url TEXT
);
