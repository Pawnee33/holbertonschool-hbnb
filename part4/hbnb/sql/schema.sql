-- Script that creates the tables User
-- Create User if it does not already exist
CREATE TABLE IF NOT EXISTS User (
    id CHAR(36) PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE
);
-- Script that creates the tables Place
-- Create Place if it does not already exist
CREATE TABLE IF NOT EXISTS Place (
    id CHAR(36) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    owner_id CHAR(36) NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES User(id)
);
-- Script that creates the tables Review
-- Create Review if it does not already exist
CREATE TABLE IF NOT EXISTS Review (
    id CHAR(36) PRIMARY KEY,
    text TEXT NOT NULL,
    rating INT NOT NULL CHECK(rating >= 1 AND rating <= 5),
    user_id CHAR(36) NOT NULL,
    place_id CHAR(36) NOT NULL,
    UNIQUE(user_id, place_id),
    FOREIGN KEY (user_id) REFERENCES User(id),
    FOREIGN KEY (place_id) REFERENCES Place(id)
);
-- Script that creates the tables Amenity
-- Create Amenity if it does not already exist
CREATE TABLE IF NOT EXISTS Amenity (
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL
);
-- Script that creates the tables Place_Amenity
-- Create Place_Amenity if it does not already exist
CREATE TABLE IF NOT EXISTS Place_Amenity (
    place_id CHAR(36) NOT NULL,
    amenity_id CHAR(36) NOT NULL,
    PRIMARY KEY (place_id, amenity_id),
    FOREIGN KEY (place_id) REFERENCES Place(id),
    FOREIGN KEY (amenity_id) REFERENCES Amenity(id)
);
-- Script that insert a new rows in the table User
-- Insert administrator user
INSERT INTO User (id, first_name, last_name, email, password, is_admin) VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$/p5I36NWwepUBXlpeW.hPuTh67aNdtGXm.m10Bk0VEjCmg2sRaWWW',
    True
);
-- Script that insert a new rows in the table Amenity
-- Insert initial amenities into the Amenity table
INSERT INTO Amenity (id, name) VALUES
('3914cd05-b04e-4b7f-8c5f-c85b8af97ab8', 'WiFi'),
('478ede07-f435-40da-a18c-b633a3947f45', 'Swimming Pool'),
('8d959aaa-fa14-4276-b3a9-83a62d12c828', 'Air Conditioning');
