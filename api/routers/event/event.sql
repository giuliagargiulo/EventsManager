CREATE TABLE IF NOT EXISTS tbl_event(
    uu_id UUID DEFAULT uuidv7() UNIQUE,
    name VARCHAR(255) NOT NULL,
    location VARCHAR(255) NOT NULL,
    event_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,

    CONSTRAINT pk_event PRIMARY KEY (uu_id)
);

CREATE TABLE tbl_event_participant(
    event_uu_id UUID NOT NULL,
    participant_uu_id UUID NOT NULL,

    CONSTRAINT fk_Event FOREIGN KEY (event_uu_id) 
        REFERENCES tbl_event(uu_id) ON DELETE CASCADE,
    CONSTRAINT fk_Participant FOREIGN KEY (participant_uu_id) 
        REFERENCES tbl_participant(uu_id) ON DELETE CASCADE,
    CONSTRAINT pk_Event_Participant PRIMARY KEY (event_uu_id, participant_uu_id)
);


INSERT INTO tbl_event (name, location, event_date, start_time, end_time) VALUES
('Tech Conference', 'New York', '2024-09-15', '09:00', '17:00'),
('Art Workshop', 'San Francisco', '2024-10-20', '10:00', '15:00'),
('Music Festival', 'Los Angeles', '2024-11-05', '12:00', '22:00');

INSERT INTO tbl_event_participant (event_uu_id, participant_uu_id) VALUES
(1, 1),
(1, 2),
(2, 1),
(2, 2),
(3, 1),
(3, 2),
(3, 3),
(3, 4);