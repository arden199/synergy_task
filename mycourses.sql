DROP DATABASE IF EXISTS Users;
CREATE DATABASE Users;
GRANT ALL ON Users.* TO 'mycourses_dev'@'localhost';
USE Users;

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  id int(11) NOT NULL AUTO_INCREMENT,
  name varchar(30) NOT NULL,
  email varchar(30) NOT NULL,
  mobile_phone varchar(12) NOT NULL,
  phone varchar(12) NOT NULL,
  status tinyint(1) DEFAULT 0,
  PRIMARY KEY (id),
  UNIQUE KEY email (email)
);
CREATE TABLE `course` (
  code varchar(15) NOT NULL,
  name varchar(30) NOT NULL,
  PRIMARY KEY (code),
  UNIQUE KEY code (code)
);
CREATE TABLE `has_course` (
  user_id int(11) NOT NULL,
  course_code varchar(15) NOT NULL,
  PRIMARY KEY (user_id, course_code),
  FOREIGN KEY (user_id) REFERENCES user (id)
  ON DELETE CASCADE,
  FOREIGN KEY (course_code) REFERENCES course (code)
  ON DELETE CASCADE,
  UNIQUE KEY user_id (user_id, course_code)
);

DELIMITER //
CREATE PROCEDURE userCreateRecord(
    IN name_in varchar(30),
    IN email_in varchar(30),
    IN mobile_phone_in varchar(12),
    IN phone_in varchar(12),
    IN status_in tinyint(1))
    BEGIN
        INSERT INTO user (name, email, mobile_phone, phone, status )
        VALUES (name_in, email_in, mobile_phone_in, phone_in, status_in);
    END //


CREATE PROCEDURE userUpdateRecord(
    IN id_in int(11),
    IN name_in varchar(30),
    IN email_in varchar(30),
    IN mobile_phone_in varchar(12),
    IN phone_in varchar(12),
    IN status_in tinyint(1))
    BEGIN
        UPDATE user
            SET
                name = name_in,
                email = email_in,
                mobile_phone = mobile_phone_in,
                phone = phone_in,
                status = status_in
            WHERE id = id_in;
    END //



CREATE PROCEDURE userGetRecordById(IN id_in int(11))
    BEGIN
        SELECT * FROM user WHERE id = id_in;
    END //
CREATE PROCEDURE userGetRecordByEmail(IN email_in varchar(30))
    BEGIN
        SELECT * FROM user WHERE email = email_in;
    END //

CREATE PROCEDURE userDeleteRecordById(IN id_in int(11))
    BEGIN
        DELETE FROM user WHERE id = id_in;
    END //

CREATE PROCEDURE userGetAllRecords()
    BEGIN
        SELECT * FROM user ORDER BY id DESC;
    END //

CREATE PROCEDURE userFilterRecord(IN search varchar(30))
    BEGIN
        SELECT * FROM user WHERE NAME LIKE search;
    END //

CREATE PROCEDURE userGetCourses(IN user_id_in int(11))
    BEGIN
        SELECT * FROM course WHERE code IN
        (SELECT course_code FROM has_course WHERE user_id = user_id_in);
    END //

CREATE PROCEDURE coursesGetRecords()
    BEGIN
        SELECT * FROM course ;
    END //

CREATE PROCEDURE createHasCourseRecord(IN user_id_in int(11), IN course_code_in varchar(15))
    BEGIN
        INSERT IGNORE INTO has_course (user_id, course_code)
        VALUES (user_id_in, course_code_in);
    END //

CREATE PROCEDURE deleteHasCourseRecord(IN user_id_in int(11), IN course_code_in varchar(15))
    BEGIN
        DELETE FROM has_course WHERE user_id = user_id_in AND course_code = course_code_in;
    END //


CALL userCreateRecord('Vini Lini', 'vini@mail.com', '', '', 1);//
CALL userCreateRecord('Pen Kyx', 'kyx@mail.com', '', '', 1);//
CALL userCreateRecord('Emby Cados', 'cados@mail.com', '', '', 0);//
CALL userCreateRecord('Noise Make', 'make@mail.com', '', '', 1);//
CALL userCreateRecord('Foxy Dori', 'foxy@mail.com', '', '', 0);//
CALL userCreateRecord('Test One', 'one@mail.com', '', '', 0);//
CALL userCreateRecord('Test Two', 'two@mail.com', '', '', 1);//
CALL userCreateRecord('Test Three', 'three@mail.com', '', '', 1);//
CALL userCreateRecord('Test Four', 'fourt@mail.com', '', '', 0);//
CALL userCreateRecord('Test Five', 'five@mail.com', '', '', 1);//
CALL userCreateRecord('Test Six', 'six@mail.com', '', '', 0);//
CALL userCreateRecord('Test Seven', 'seven@mail.com', '', '', 1);//
CALL userCreateRecord('Test Eight', 'eight@mail.com', '', '', 1);//
CALL userCreateRecord('Test Nine', 'nine@mail.com', '', '', 1);//
CALL userCreateRecord('Test Ten', 'ten@mail.com', '', '', 0);//
CALL userCreateRecord('Test Eleven', 'eleven@mail.com', '', '', 0);//
CALL userCreateRecord('Test Twelve', 'twelve@mail.com', '', '', 1);//
CALL userCreateRecord('Test Thirteen', 'thirteen@mail.com', '', '', 1);//
CALL userCreateRecord('Test Fourteen', 'fourteen@mail.com', '', '', 0);//
CALL userCreateRecord('Test Fiveteen', 'fiveteen@mail.com', '', '', 1);//
CALL userCreateRecord('Test Sixteen', 'sixteen@mail.com', '', '', 0);//
CALL userCreateRecord('Test Seventeen', 'seventeen@mail.com', '', '', 1);//
CALL userCreateRecord('Test Eighteen', 'eighteen@mail.com', '', '', 1);//
CALL userCreateRecord('Test Nineteen', 'nineteen@mail.com', '', '', 1);//
CALL userCreateRecord('Test Twenty', 'twenty@mail.com', '', '', 0);//
CALL userCreateRecord('Test John', 'johno@mail.com', '', '', 0);//
CALL userCreateRecord('Test Smith', 'smiith@mail.com', '', '', 1);//
CALL userCreateRecord('Test Fith', 'fiith@mail.com', '', '', 1);//
CALL userCreateRecord('Test South', 'south@mail.com', '', '', 0);//
CALL userCreateRecord('Test North', 'north@mail.com', '', '', 1);//
CALL userCreateRecord('Test List', 'list@mail.com', '', '', 0);//
CALL userCreateRecord('Test Rest', 'rest@mail.com', '', '', 1);//
CALL userCreateRecord('Test Desd', 'desd@mail.com', '', '', 1);//
CALL userCreateRecord('Test Word', 'word@mail.com', '', '', 1);//
CALL userCreateRecord('Test Last', 'last@mail.com', '', '', 0);//
CALL userCreateRecord('Page Nator', 'page@mail.com', '', '', 1);//
CALL userCreateRecord('Just Record', 'just@mail.com', '', '', 0);//
CALL userCreateRecord('Gary Busey', 'busey@mail.com', '', '', 1);//
CALL userCreateRecord('Jeff Bridges', 'bridges@mail.com', '', '', 1);//
CALL userCreateRecord('Michael Cimino', 'cimino@mail.com', '', '', 0);//
CALL userCreateRecord('Roger Corman', 'corman@mail.com', '', '', 1);//
CALL userCreateRecord('Don Rickles', 'don@mail.com', '', '', 0);//
CALL userCreateRecord('Harold Stone', 'stone@mail.com', '', '', 0);//
CALL userCreateRecord('John Hoyt', 'hoyt@mail.com', '', '', 1);//
CALL userCreateRecord('Ray Milland', 'ray@mail.com', '', '', 1);//
CALL userCreateRecord('Bruno Dumont', 'dumont@mail.com', '', '', 0);//
CALL userCreateRecord('Alane Delhaye', 'alane@mail.com', '', '', 1);//
CALL userCreateRecord('Bernard Pruvost', 'bernard@mail.com', '', '', 0);//
CALL userCreateRecord('Lucy Caron', 'caron@mail.com', '', '', 1);//
CALL userCreateRecord('Philippe Jore', 'jore@mail.com', '', '', 1);//
CALL userCreateRecord('Robert Wiene', 'wiene@mail.com', '', '', 1);//
CALL userCreateRecord('Werner Krauss', 'krauss@mail.com', '', '', 0);//


INSERT INTO course (name, code) VALUES ('Python-Base', 'P012345');//
INSERT INTO course (name, code) VALUES ('Python-Database', 'P234567');//
INSERT INTO course (name, code) VALUES ('HTML', 'H345678');//
INSERT INTO course (name, code) VALUES ('Java-Base', 'J456789');//
INSERT INTO course (name, code) VALUES ('JavaScript-Base', 'JS543210');//
