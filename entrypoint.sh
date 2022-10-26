#!/bin/ash

# Secure entrypoint
chmod 600 /entrypoint.sh

# Initialize & Start MariaDB
mkdir -p /run/mysqld
chown -R mysql:mysql /run/mysqld
mysql_install_db --user=mysql --ldata=/var/lib/mysql
mysqld --user=mysql --console --skip-networking=0 &

# Wait for mysql to start
while ! mysqladmin ping -h'localhost' --silent; do echo 'not up' && sleep .2; done

mysql -u root << EOF
CREATE DATABASE solezonsolis;

CREATE TABLE solezonsolis.users (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    username varchar(255) NOT NULL UNIQUE,
    password varchar(255) NOT NULL
);

INSERT INTO solezonsolis.users (username, password) VALUES ('plank', '\$2b\$12\$04FYT3s0g3vew4W4oLf3IODwt2/HQnVwjDo2h66sFpHzC4/Wbqj/a');
INSERT INTO solezonsolis.users (username, password) VALUES ('bob', '\$2b\$12\$IFbxbjIY.8LXAgmYC6gUg.WgOjd1vIEAqefKFfO/QTZ6Ln0UZJaBO');
INSERT INTO solezonsolis.users (username, password) VALUES ('clem', '\$2b\$12\$L2VHtnrnS4EyedLq5UCS.uIylED2tqIVdDK0yHNRLq7jzv1YkxK6S');
INSERT INTO solezonsolis.users (username, password) VALUES ('alicia', '\$2b\$12\$ouERipMvblQrm4CqCstJQewv6Ne53xQRgCs75K5k4h5pSapcTrU9K');
INSERT INTO solezonsolis.users (username, password) VALUES ('sue', '\$2b\$12\$T.owvG2dG79XTIvQvh/3nO4Ow4WA7hQxKumVpQAHRHP42XVYrtXYC');

CREATE USER 'user'@'localhost' IDENTIFIED BY 'Gr33n73@mC4nG0D1e>:(';
GRANT SELECT, INSERT, UPDATE ON solezonsolis.users TO 'user'@'localhost';

FLUSH PRIVILEGES;
EOF

/usr/bin/supervisord -c /etc/supervisord.conf