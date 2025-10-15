CREATE TABLE IF NOT EXISTS tbl_participant(
    uu_id UUID DEFAULT uuidv7() UNIQUE,
    name VARCHAR(100) NOT NULL,
    surname VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(15) UNIQUE NOT NULL,

    CONSTRAINT pk_participant PRIMARY KEY (uu_id)
);

INSERT INTO tbl_participant (name, surname, email, phone) VALUES
('John', 'Doe', 'john.doe@example.com', '123-456-7890'),
('Jane', 'Smith', 'jane.smith@example.com', '098-765-4321'),
('Alice', 'Johnson', 'alice.johnson@example.com', '555-123-4567'),
('Giulia', 'Gargiulo', 'giulia.gargiulo@example.com', '444-555-6666');
