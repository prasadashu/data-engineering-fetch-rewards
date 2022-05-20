-- Creation of user_logins table

CREATE TABLE IF NOT EXISTS user_logins(
    user_id             varchar(128),
    device_type         varchar(32),
    hashed_ip           varchar(256),
    hashed_device_id    varchar(256),
    locale              varchar(32),
    app_version         integer,
    create_date         date
);
