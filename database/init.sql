CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    oauth_ID VARCHAR(255) NOT NULL
);

CREATE TABLE ratings (
    id SERIAL PRIMARY KEY,
    movie_ID VARCHAR(255) NOT NULL,
    oauth_ID VARCHAR(255) NOT NULL,
    rating INTEGER NOT NULL,
    rdate TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO users (username, oauth_ID) VALUES
  ('Mkyong', 40),
  ('Ali', 28),
  ('Teoh', 18);


