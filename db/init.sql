CREATE TABLE Events(
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    location VARCHAR(255) NOT NULL,
    date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL
);

CREATE TABLE Participants(
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    surname VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(15) UNIQUE NOT NULL
);

CREATE TABLE EventsParticipants(
    event_id INTEGER,
    participant_id INTEGER,

    CONSTRAINT FK_Event FOREIGN KEY (event_id) 
        REFERENCES Events(id) ON DELETE CASCADE,
    CONSTRAINT FK_Participant FOREIGN KEY (participant_id) 
        REFERENCES Participants(id) ON DELETE CASCADE,
    PRIMARY KEY (event_id, participant_id)
);


INSERT INTO Events (name, location, date, start_time, end_time) VALUES
('Tech Conference', 'New York', '2024-09-15', '09:00', '17:00'),
('Art Workshop', 'San Francisco', '2024-10-20', '10:00', '15:00'),
('Music Festival', 'Los Angeles', '2024-11-05', '12:00', '22:00');

INSERT INTO Participants (name, surname, email, phone) VALUES
('John', 'Doe', 'john.doe@example.com', '123-456-7890'),
('Jane', 'Smith', 'jane.smith@example.com', '098-765-4321'),
('Alice', 'Johnson', 'alice.johnson@example.com', '555-123-4567'),
('Giulia', 'Gargiulo', 'giulia.gargiulo@example.com', '444-555-6666');

INSERT INTO EventsParticipants (event_id, participant_id) VALUES
(1, 1),
(1, 2),
(2, 1),
(2, 2),
(3, 1),
(3, 2),
(3, 3),
(3, 4);

