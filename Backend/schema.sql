DROP TABLE IF EXISTS teamInfo, matchResult;

CREATE TABLE teamInfo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    teamName TEXT NOT NULL,
    registrationDate DATE NOT NULL,
    groupNumber INTEGER NOT NULL,
);

CREATE TABLE atchResult (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    teamA TEXT NOT NULL,
    scoreA INTEGER NOT NULL,
    teamA TEXT NOT NULL,
    scoreB INTEGER NOT NULL,
);
