import mysql.connector

# Connexion au serveur MySQL (sans spécifier la base)
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password=""
)

cursor = db.cursor()

# Création de la base si elle n'existe pas
cursor.execute("CREATE DATABASE IF NOT EXISTS planify")
cursor.execute("USE planify")

# Table Plan
cursor.execute("""
CREATE TABLE IF NOT EXISTS Plan (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    hour_volume FLOAT,
    sms_volume INT,
    gb_volume FLOAT,
    price FLOAT NOT NULL,
    type VARCHAR(255)
)
""")

# Table Customer
cursor.execute("""
CREATE TABLE IF NOT EXISTS Customer (
    id INT AUTO_INCREMENT PRIMARY KEY,
    last_name VARCHAR(255),
    first_name VARCHAR(255),
    email VARCHAR(255),
    current_plan VARCHAR(255)
)
""")

# Table Consumption
cursor.execute("""
CREATE TABLE IF NOT EXISTS Consumption (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    date DATE NOT NULL,
    hour_volume FLOAT,
    sms_volume INT,
    gb_volume FLOAT,
    price FLOAT,
    customer_id INT,
    FOREIGN KEY (customer_id) REFERENCES Customer(id)
)
""")

db.commit()
cursor.close()
db.close()

print("Connexion OK")
