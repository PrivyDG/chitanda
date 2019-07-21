CREATE TABLE irc_channels (
    name TEXT,
    server TEXT,
    active INT NOT NULL DEFAULT 1,
    PRIMARY KEY (name, server)
);
