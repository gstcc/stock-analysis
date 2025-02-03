DROP TABLE IF EXISTS userStocks;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    user VARCHAR(100) NOT NULL UNIQUE, 
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE userStocks (
    id INT PRIMARY KEY,
    stocks JSON,
    FOREIGN KEY (id) REFERENCES users(id) ON DELETE CASCADE
);

-- Can't remember my root password so this is currently not wokring
-- DELIMITER $$

-- CREATE TRIGGER after_user_insert
-- AFTER INSERT ON users
-- FOR EACH ROW
-- BEGIN
--     INSERT INTO userStocks (id, stocks)
--     VALUES (NEW.id, JSON_ARRAY());
-- END$$

-- DELIMITER ;
