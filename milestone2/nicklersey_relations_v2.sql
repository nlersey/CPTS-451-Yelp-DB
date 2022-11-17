
CREATE TABLE 	user_ (	 
	user_id VARCHAR PRIMARY KEY,
	yelping_since DATE,
	name VARCHAR,
	tipCount INTEGER DEFAULT 0,   
	fans INTEGER,
	average_star DOUBLE PRECISION, 		
	funny  			INTEGER,
	useful 			INTEGER,
	cool 			INTEGER,
	userLongitude VARCHAR,
	totalLikes INTEGER DEFAULT 0
);

CREATE TABLE business(
	business_id		 VARCHAR PRIMARY KEY,
	name 			 VARCHAR,
	state			 VARCHAR,
	city 			 VARCHAR,
	address 		 VARCHAR,
	is_open 		 BOOLEAN,
	zipcode			 VARCHAR,
	numcheckin		 INTEGER DEFAULT 0,
	numtips			 INTEGER DEFAULT 0,	
	stars			 DOUBLE PRECISION,
	latitude		 DOUBLE PRECISION,
	longitude 		 DOUBLE PRECISION
);

CREATE TABLE hasFriend
(
	userID		 	VARCHAR NOT NULL,
	userID2		 	VARCHAR NOT NULL,
	PRIMARY KEY (userID2,userID),
	FOREIGN KEY (userID) REFERENCES user_(user_id),
	FOREIGN KEY (userID2) REFERENCES user_(user_id)
);

CREATE TABLE Tip(
	business_id     VARCHAR NOT NULL,
	user_id VARCHAR NOT NULL,
	tipDate  DATE NOT NULL,
	tipText	 VARCHAR,
	likes INTEGER,
	PRIMARY KEY(user_id,business_id,tipDate),
	FOREIGN KEY (user_id) REFERENCES user_(user_id),
	FOREIGN KEY (business_id) REFERENCES business(business_id)
);

CREATE TABLE categories(
	business_id VARCHAR NOT NULL,
	cname VARCHAR NOT NULL,
	PRIMARY KEY (business_id, cname),
	FOREIGN KEY (business_id) REFERENCES business(business_id)
);

CREATE TABLE hours(
	business_id		 VARCHAR NOT NULL,
	day				 VARCHAR NOT NULL,
	open			 TIME,
	close			 TIME,
	PRIMARY KEY(business_id, day),
	FOREIGN KEY (business_id) REFERENCES business(business_id) 

);

CREATE TABLE attribute(
	business_id		 VARCHAR NOT NULL,
	aname			 VARCHAR,
	value			 VARCHAR,
	PRIMARY KEY (business_id,aname),
	FOREIGN KEY (business_id) REFERENCES business(business_id)
);

CREATE TABLE checkins(
business_id	 	VARCHAR,
"datetime" 		TIMESTAMP , 
PRIMARY KEY (business_id, "datetime"),
FOREIGN KEY (business_id) REFERENCES business(business_id)
);