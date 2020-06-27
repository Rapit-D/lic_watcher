DROP TABLE lic_usage;

CREATE TABLE lic_usage(
id integer PRIMARY KEY autoincrement,
server varchar(100),
feature varchar(100),
current_date DATE,
current_time TIME,
current_users integer,
total_lic_available integer,
users_detail BLOB
);