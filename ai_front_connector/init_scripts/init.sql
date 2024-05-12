CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    oauth_ID VARCHAR(255) NOT NULL
);

INSERT INTO users (username, oauth_ID) VALUES
  ('Mkyong', 40),
  ('Ali', 28),
  ('Teoh', 18);