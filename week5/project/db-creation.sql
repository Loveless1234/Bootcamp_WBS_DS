CREATE DATABASE if not exists gans; 

USE gans;

drop table if exists cities;
CREATE TABLE IF NOT EXISTS cities (
city_id INT,
city_name VARCHAR(200),
latitude_deg float, 
longitude_deg float, 
iso_country varchar(200),
iso_region varchar(200),
municipality varchar(200),
icao_code varchar(200),
iata_code varchar(200),
 municipality_iso_country varchar(200),
 PRIMARY KEY(city_id)

); 

drop table if exists arrivals;
CREATE TABLE IF NOT EXISTS arrivals (
dep_airport VARCHAR(200),
sched_arr_loc_time timestamp,
terminal int, 
status varchar(200),
aircraft varchar(200),
icao_code varchar(200)
); 

drop table if exists weathers;
CREATE TABLE IF NOT EXISTS weathers (
datetime  timestamp,
temperature float, 
wind float,
prob_perc float,
rain_qty float,
snow float,
municipality_iso_country varchar(200)

); 


select * from cities;
INSERT INTO cities (city_id, city_name) VALUES (1, 'hasjdhs');
