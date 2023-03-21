CREATE TABLE people (
  id INTEGER PRIMARY KEY,
  name TEXT,
  telegram TEXT,
);

CREATE TABLE social_media (
  id INTEGER PRIMARY KEY,
  person_id INTEGER,
  platform TEXT,
  link TEXT,
  FOREIGN KEY (person_id) REFERENCES people(id)
);