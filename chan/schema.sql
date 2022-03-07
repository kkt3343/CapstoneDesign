/* 한번만 실행할 것! 반복 실행 시 기존 DB 날라감! */

DROP DATABASE IF EXISTS usedcardb;
DROP USER IF EXISTS dbAdmin;
CREATE USER dbAdmin IDENTIFIED WITH mysql_native_password by 'xoduqrb';
create database usedcardb;
grant all privileges on usedcardb.* to dbAdmin with grant option;
commit;

use usedcardb;

CREATE TABLE userTable(
	token VARCHAR(500),
	userid VARCHAR(20) PRIMARY KEY,
    userpw VARCHAR(20),
    username VARCHAR(20),
    email VARCHAR(40),
	age INTEGER,
    gender VARCHAR(10),
    isLogin bool DEFAULT false
);
CREATE TABLE Notification(
	noti_num INTEGER AUTO_INCREMENT PRIMARY KEY,
    userid VARCHAR(20),
    model VARCHAR(20),
    caryear_from INTEGER,
    caryear_to INTEGER,
    distance_from INTEGER,
    distance_to INTEGER,
    price_from INTEGER,
    price_to INTEGER
);
CREATE TABLE usedCar(
	carid INTEGER AUTO_INCREMENT,
	url VARCHAR(200),
    site VARCHAR(20),
    title VARCHAR(100),	
    carnumber VARCHAR(20),
	cartype VARCHAR(20),
    manufacturer VARCHAR(20),
    model VARCHAR(20),
    model_detail VARCHAR(20),
    price INTEGER,
	distance INTEGER,
    displacement VARCHAR(10),
    caryear VARCHAR(20),
    carcolor VARCHAR(20),
    carfuel VARCHAR(20),
    imglink VARCHAR(100),
    PRIMARY KEY (carid)
);

CREATE TABLE carModel(
	manufacturer VARCHAR(20),
    model VARCHAR(20),
    model_detail VARCHAR(50),
    PRIMARY KEY (manufacturer, model, model_detail)
);

CREATE TABLE KBModel(
	manufacturer1 VARCHAR(20),
    model1 VARCHAR(20),
    model_detail1 VARCHAR(50),
    manufacturer2 VARCHAR(20),
    model2 VARCHAR(20),
    model_detail2 VARCHAR(50)
);

CREATE TABLE KCarModel(
	manufacturer1 VARCHAR(20),
    model1 VARCHAR(20),
    model_detail1 VARCHAR(50),
    manufacturer2 VARCHAR(20),
    model2 VARCHAR(20),
    model_detail2 VARCHAR(50)
);

CREATE TABLE BobaeModel (
    manufacturer1 VARCHAR(20),
    model1 VARCHAR(20),
    model_detail1 VARCHAR(50),
    manufacturer2 VARCHAR(20),
    model2 VARCHAR(20),
    model_detail2 VARCHAR(50)
);

CREATE TABLE EncarModel(
	manufacturer1 VARCHAR(20),
    model1 VARCHAR(20),
    model_detail1 VARCHAR(50),
    manufacturer2 VARCHAR(20),
    model2 VARCHAR(20),
    model_detail2 VARCHAR(50)
);

CREATE TABLE testToken (
	token VARCHAR(500)
);