use fxjdb;

set names utf8;

CREATE TABLE fxjdb.user (

	 uid INT UNSIGNED AUTO_INCREMENT,
	
	 uname VARCHAR(255) NOT NULL UNIQUE,
	
	 passwd VARCHAR(50) NOT NULL,
	
	 phone CHAR(11) NOT NULL,
	
	 email varchar(255) NOT NULL,
	
	PRIMARY KEY (uid)

) ENGINE=INNODB AUTO_INCREMENT=1000 DEFAULT CHARACTER SET utf8;
 

desc user;


-- 创建新用户
-- create user 'dj'@'%' identified by 'abc123';

-- 创建数据库
-- create database mydb default character set utf8;

-- 给用户授权
-- grant all on mydb.* to 'dj'@'%';

-- 刷新授权
-- flush privileges;

-- 查看用户
--select host,user from mysql.user; 

-- 重命名   
-- rename user dj to jj;

-- 修改密码
-- set password for 'jj'@'%' = password('123456')
