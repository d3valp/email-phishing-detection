CREATE TABLE IF NOT EXISTS scored_messages (
    id INTEGER PRIMARY KEY,
    email_text TEXT NOT NULL,
    probability_phishing REAL NOT NULL,
    predicted_label TEXT NOT NULL,
    scored_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
SELECT predicted_label, COUNT(*) AS message_count
FROM scored_messages
GROUP BY predicted_label
ORDER BY message_count DESC;
