CREATE DATABASE content_moderation;

USE content_moderation;

CREATE TABLE comments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    comment TEXT NOT NULL,
    toxicity_score INT NOT NULL,
    severity_category VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    moderation_status VARCHAR(20) DEFAULT 'Pending',
    is_flagged BOOLEAN DEFAULT FALSE
);

select * from comments;