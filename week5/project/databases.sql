CREATE DATABASE if not exists gans; 

USE gans;

drop table if exists cities;
CREATE TABLE IF NOT EXISTS cities (
 municipality  VARCHAR(255),
 iso_country varchar(255),
municipality_iso_country varchar(255),
primary key(municipality_iso_country )
); 


drop table if exists airports_cities;
CREATE TABLE IF NOT EXISTS airports_cities (
name  VARCHAR(255),
latitude_deg decimal, 
longitude_deg decimal, 
iso_country varchar(255),
iso_region varchar(255),
municipality varchar(255),
icao_code varchar(255),
iata_code varchar(255),
 municipality_iso_country varchar(255),
 PRIMARY KEY(icao_code),
 foreign key ( municipality_iso_country ) references cities( municipality_iso_country )

); 

drop table if exists arrivals;
CREATE TABLE IF NOT EXISTS arrivals (
arrival_id int auto_increment,
dep_airport VARCHAR(200),
sched_arr_loc_time datetime,
terminal varchar(255), 
status  varchar(255),
aircraft varchar(255),
icao_code varchar(255),
primary key(arrival_id),
foreign key(icao_code) references airports_cities(icao_code)
); 

drop table if exists weathers;
CREATE TABLE IF NOT EXISTS weathers (
weather_id int auto_increment,
datetime  datetime,
temperature decimal, 
wind decimal,
prob_perc decimal,
rain_qty decimal,
snow decimal,
municipality_iso_country varchar(255),
primary key(weather_id),
foreign key( municipality_iso_country ) references cities( municipality_iso_country )

); 


