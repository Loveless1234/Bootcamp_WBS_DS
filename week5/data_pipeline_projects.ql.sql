-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema gan
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema gan
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `gan` DEFAULT CHARACTER SET utf8 ;
USE `gan` ;

-- -----------------------------------------------------
-- Table `gan`.`cities`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `gan`.`cities` (
  `city_id` VARCHAR(100) NOT NULL,
  `city_name` VARCHAR(100) NULL,
  `country` VARCHAR(100) NULL,
  `airport_icao` VARCHAR(100) NULL,
  PRIMARY KEY (`city_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `gan`.`flight`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `gan`.`flight` (
  `arrival_airport` VARCHAR(100) NULL,
  `departure_airport` VARCHAR(100) NULL,
  `flight_number` VARCHAR(100) NULL,
  `arrival_timestamp` DATETIME NULL,
  `airline_name` VARCHAR(100) NULL,
  `cities_city_id` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`cities_city_id`),
  CONSTRAINT `fk_flight_cities`
    FOREIGN KEY (`cities_city_id`)
    REFERENCES `gan`.`cities` (`city_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `gan`.`weather`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `gan`.`weather` (
  `city_id` VARCHAR(100) NULL,
  `temperature` DECIMAL(10,8) NULL,
  `humidity` DECIMAL(5,5) NULL,
  `prob_rain` DECIMAL(5,5) NULL,
  `forecast_timestamp` DATETIME NULL,
  `cities_city_id` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`cities_city_id`),
  CONSTRAINT `fk_weather_cities1`
    FOREIGN KEY (`cities_city_id`)
    REFERENCES `gan`.`cities` (`city_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `gan`.`demographics`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `gan`.`demographics` (
  `city_id` VARCHAR(100) NOT NULL,
  `population` DECIMAL(15,10) NULL,
  `gdp` DECIMAL(10,10) NULL,
  `datetime_extraction` DATETIME NULL,
  `cities_city_id` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`city_id`, `cities_city_id`),
  INDEX `fk_demographics_cities1_idx` (`cities_city_id` ASC),
  CONSTRAINT `fk_demographics_cities1`
    FOREIGN KEY (`cities_city_id`)
    REFERENCES `gan`.`cities` (`city_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
