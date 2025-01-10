-- Configurar el usuario root para aceptar conexiones desde cualquier host
ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY 'Ea7hava5*';
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;

-- Opcional: Crear tablas o datos iniciales
-- CREATE TABLE led_studio_table (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255));
