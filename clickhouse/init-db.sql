CREATE TABLE IF NOT EXISTS sensor_data
(
    timestamp DateTime,
    device    String,
    amperage  Float32
) ENGINE = MergeTree()
ORDER BY timestamp;
