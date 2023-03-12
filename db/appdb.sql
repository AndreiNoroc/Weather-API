CREATE DATABASE app_db;
USE app_db;

CREATE TABLE Tari (
    id INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
    nume_tara VARCHAR(20) NOT NULL UNIQUE,
    latitudine FLOAT(8, 3) NOT NULL,
    longitudine FLOAT(8, 3) NOT NULL
);

CREATE TABLE Orase (
    id INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
    id_tara INTEGER NOT NULL,
    nume_oras VARCHAR(20) NOT NULL,
    latitudine FLOAT(8, 3) NOT NULL,
    longitudine FLOAT(8, 3) NOT NULL,
    CONSTRAINT uoras UNIQUE (id_tara, nume_oras),
    CONSTRAINT fktara FOREIGN KEY (id_tara)
        REFERENCES Tari (id) ON DELETE CASCADE
);

CREATE TABLE Temperaturi (
    id INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
    valoare FLOAT(8, 3) NOT NULL,
    timestamp DATETIME(6) DEFAULT CURRENT_TIMESTAMP(6),
    id_oras INTEGER NOT NULL,
    CONSTRAINT utemp UNIQUE (id_oras, timestamp),
    CONSTRAINT fkoras FOREIGN KEY (id_oras)
        REFERENCES Orase (id) ON DELETE CASCADE    
);
