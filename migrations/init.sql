
CREATE TABLE IF NOT EXISTS detections (
    id SERIAL PRIMARY KEY,
    label TEXT,
    source_file TEXT,
    detected_at TIMESTAMP
);
