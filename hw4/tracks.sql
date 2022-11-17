DROP TABLE IF EXISTS Tracks; 

CREATE TABLE Tracks (
	major  VARCHAR(7),
	trackcode   VARCHAR(10),
	title  VARCHAR(30),
	PRIMARY KEY(major,trackcode) 
);


INSERT INTO Tracks (major,trackcode,title) VALUES ('CptS','SE','Software Engineering Track'),
												  ('CptS','SYS','Systems Track'),	
												  ('CptS','G','General Track'),	
												  ('EE','CE', 'Computer Engineering Track'),	
												  ('EE','ME', 'Microelectronics Track'),	
												  ('EE','POW','Power Track');