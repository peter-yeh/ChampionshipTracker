DROP TABLE IF EXISTS teamInfo;
DROP TABLE IF EXISTS matchResult;

CREATE TABLE teamInfo (
    teamName TEXT NOT NULL,
    registrationDate TEXT NOT NULL,
    groupNumber INTEGER NOT NULL,
    PRIMARY KEY (teamName, registrationDate)
);

CREATE TABLE matchResult (
    teamA TEXT NOT NULL,
    scoreA INTEGER NOT NULL,
    teamB TEXT NOT NULL,
    scoreB INTEGER NOT NULL,
    PRIMARY KEY (teamA, scoreA, teamB, scoreB)
);
