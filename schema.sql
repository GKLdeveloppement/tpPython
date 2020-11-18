DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS game;
DROP TABLE IF EXISTS userGame;

CREATE TABLE user (
  idUser INTEGER PRIMARY KEY,
  username TEXT NOT NULL UNIQUE,
  password TEXT NOT NULL

);

CREATE TABLE game (
  idGame INTEGER PRIMARY KEY AUTOINCREMENT,
  gameName TEXT NOT NULL,
  plateform TEXT NOT NULL
);

CREATE TABLE userGame (
  idUserGame INTEGER PRIMARY KEY,
  fkUser INTEGER REFERENCES user(idUser),
  fkGame INTEGER REFERENCES game(idGame)
);

INSERT INTO game (gameName, plateform)
  VALUES 
  ('Rocket League', 'PC'),
  ('Rocket League', 'XBOX'),
  ('Rocket League', 'PlayStation'),
  ('Rocket League', 'Switch'),
  ('Fortnite', 'PC'),
  ('Fortnite', 'XBOX'),
  ('Fortnite', 'PlayStation'),
  ('Fortnite', 'Switch'),
  ('Diablo3', 'PC'),
  ('Diablo3', 'XBOX'),
  ('Diablo3', 'PlayStation'),
  ('Diablo3', 'Switch'),
  ('Civilization5', 'PC'),
  ('Civilization5', 'XBOX'),
  ('Civilization5', 'PlayStation'),
  ('Civilization5', 'Switch'),
  ('Rust', 'PC'),
  ('Rust', 'XBOX'),
  ('Rust', 'PlayStation'),
  ('FootballManager2020', 'PC'),
  ('FootballManager2020', 'XBOX'),
  ('FootballManager2020', 'PlayStation'),
  ('FootballManager2020', 'Switch');

INSERT INTO user (userName, password)
  VALUES 
  ('PepsiM', 'XBOX'),
  ('Maxime', 'Decorde');
