
CREATE TABLE 	usertable (	 
	user_id VARCHAR PRIMARY KEY,
	yelping_since DATE,
	uname VARCHAR,
	review_count INTEGER DEFAULT 0,   
	fans INTEGER,
	average_stars DOUBLE PRECISION, 		
	funny  			INTEGER,
	useful 			INTEGER,
	cool 			INTEGER,
	userLongitude VARCHAR,
	userLatitude VARCHAR,
	totalLikes INTEGER DEFAULT 0
);

CREATE TABLE business(
	business_id		 VARCHAR PRIMARY KEY,
	bname 			 VARCHAR,
	bstate			 VARCHAR,
	city 			 VARCHAR,
	baddress 		 VARCHAR,
	is_open 		 BOOLEAN,
	zipcode			 VARCHAR,
	numcheckin		 INTEGER DEFAULT 0,
	review_count		 INTEGER DEFAULT 0,
	stars			 DOUBLE PRECISION,
	latitude		 DOUBLE PRECISION,
	longitude 		 DOUBLE PRECISION
);

CREATE TABLE hasFriend
(
	userID		 	VARCHAR,
	friendID		 	VARCHAR ,
	PRIMARY KEY (userID,friendID),
	FOREIGN KEY (userID) REFERENCES usertable(user_id),
	FOREIGN KEY (friendID) REFERENCES usertable(user_id)
);

CREATE TABLE review(
	business_id     VARCHAR NOT NULL,
	user_id VARCHAR NOT NULL,
	review_date  DATE NOT NULL,
	reviewtext	 VARCHAR,
	stars INTEGER,
	PRIMARY KEY(user_id,business_id,review_date),
	FOREIGN KEY (user_id) REFERENCES usertable(user_id),
	FOREIGN KEY (business_id) REFERENCES business(business_id)
);

CREATE TABLE categories(
	business_id VARCHAR NOT NULL,
	cname VARCHAR NOT NULL,
	PRIMARY KEY (business_id, cname),
	FOREIGN KEY (business_id) REFERENCES business(business_id)
);

CREATE TABLE Businesshours(
	business_id		 VARCHAR NOT NULL,
	day				 VARCHAR NOT NULL,
	opentime			 TIME,
	closetime			 TIME,
	PRIMARY KEY(business_id, day),
	FOREIGN KEY (business_id) REFERENCES business(business_id) 

);

CREATE TABLE attribute(
	business_id		 VARCHAR NOT NULL,
	aname			 VARCHAR,
	avalue			 VARCHAR,
	PRIMARY KEY (business_id,aname),
	FOREIGN KEY (business_id) REFERENCES business(business_id)
);

CREATE TABLE checkins(
business_id	 	VARCHAR,
day 			VARCHAR, 
total 			INTEGER, 
PRIMARY KEY (business_id, day),
FOREIGN KEY (business_id) REFERENCES business(business_id)
);

CREATE TABLE zipcodedata(
	zipcode				VARCHAR,
	medianIncome		INTEGER,
	meanIncome			INTEGER,
	population			INTEGER,
	PRIMARY KEY (zipcode)
);
