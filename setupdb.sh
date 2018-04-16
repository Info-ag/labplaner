#!/bin/bash
###########################################
# Script used to setup the local database.
# You might have to run this as root.
###########################################


mysql -e "CREATE USER 'test'@'localhost' IDENTIFIED BY '123456';";
mysql -e "CREATE DATABASE base CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;";
mysql -e "GRANT ALL PRIVILEGES ON base.* TO 'test'@'localhost';";
mysql -e "FLUSH PRIVILEGES;";
