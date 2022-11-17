import json
import psycopg2

def cleanStr4SQL(s):
    return s.replace("'","`").replace("\n"," ")

def int2BoolStr (value):
    if value == 0:
        return 'False'
    else:
        return 'True'

def insert2BusinessTable():
    #reading the JSON file
    with open('C:/Users/nlers/Documents/451code/451private/milestone1/Yelp-CptS451/yelp_business.JSON','r') as f:    #TODO: update path for the input file
        #outfile =  open('./yelp_business.SQL', 'w')  #uncomment this line if you are writing the INSERT statements to an output file.
        line = f.readline()
        count_line = 0

        #connect to yelpdb database on postgres server using psycopg2
        #TODO: update the database name, username, and password
        try:
            conn = psycopg2.connect("dbname='milestone1db' user='postgres' host='localhost' password='cyber626'")
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()

        while line:
            data = json.loads(line)
            businessID = cleanStr4SQL(data['business_id'])
            # Generate the INSERT statement for the current business
            # TODO: The below INSERT statement is based on a simple (and incomplete) businesstable schema. Update the statement based on your own table schema and
            # include values for all businessTable attributes
            sql_str = "INSERT INTO Business (businessID, businessName, address, avgScore, city, numCheckins, reviewCount, reviewRating, businessState, stars, openStatus, zip, latitude, longitude) " \
                      + "VALUES ('" + businessID + "','" + cleanStr4SQL(data['name']) + "','" + cleanStr4SQL(data['address']) + "','" \
                      + str(0) + "','" + cleanStr4SQL(data['city']) + "','" + str(0)  \
                      + "','" + str(0) + "','" + str(0) + "','" + cleanStr4SQL(data['state']) + "','" + str(data['stars']) + "','" + str(data['is_open']) \
                      + "','" + str(data['postal_code']) + "','" + str(data['latitude']) + "','" + str(data['longitude']) + "');"
            try:
                cur.execute(sql_str)
            except:
                print("Insert to businessTABLE failed!")
            
            for item in data['categories']:
                insert2CategoryTable(businessID, cleanStr4SQL(item), conn, cur)

            for key,value in data['hours'].items():
                openTime = value.split('-')[0]
                closeTime = value.split('-')[1]
                insert2TimesTable(businessID, cleanStr4SQL(key), cleanStr4SQL(openTime), cleanStr4SQL(closeTime), conn, cur)

            conn.commit()
            # optionally you might write the INSERT statement to a file.
            # outfile.write(sql_str)

            line = f.readline()
            count_line +=1

        cur.close()
        conn.close()

    print(count_line)
    #outfile.close()  #uncomment this line if you are writing the INSERT statements to an output file.
    f.close()

def insert2UserTable():
    with open('C:/Users/nlers/Documents/451code/451private/milestone1/Yelp-CptS451/yelp_user.JSON','r') as f:
        line = f.readline()
        count_line = 0

        try:
            conn = psycopg2.connect("dbname='milestone1db' user='postgres' host='localhost' password='cyber626'")
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()

        while line:
            data = json.loads(line)
            userID = cleanStr4SQL(data['user_id'])
            # Generate the INSERT statement for the current user

            sql_str = "INSERT INTO UserTable (userID, name, avgStars, yelpingSince, latitude, longitude, numFans, votes) " \
                + "VALUES ('" + userID + "','" + cleanStr4SQL(data['name']) + "','" + str(data['average_stars']) + "','" \
                + cleanStr4SQL(data['yelping_since']) + "','" + str(0) + "','" + str(0) + "','" + str(data['fans']) + "','" + str(data['review_count']) + "');"

            try:
                cur.execute(sql_str)
            except Exception as error:
                print('Insert to UserTable failed!')

            conn.commit()

            line = f.readline()
            count_line +=1

        cur.close()
        conn.close()

    print(count_line)
    f.close()

def insert2CheckinTable():
    with open('C:/Users/nlers/Documents/451code/451private/milestone1/Yelp-CptS451/yelp_checkin.JSON','r') as f:
        line = f.readline()
        count_line = 0

        try:
            conn = psycopg2.connect("dbname='milestone1db' user='postgres' host='localhost' password='cyber626'")
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()

        while line:
            data = json.loads(line)
            businessID = cleanStr4SQL(data['business_id'])
            # Generate the INSERT statement for the current checkin
            for day in data['time']:
                for hour in data['time'][day]:
                    sql_str = "INSERT INTO CheckIn (checkInDay, checkInTime, checkInAmount, checkInBusinessID) " + \
                       "VALUES ('" + cleanStr4SQL(day) + "','" + cleanStr4SQL(hour) + "','" + str(data['time'][day][hour]) + "','" + \
                       businessID + "');"
                    try:
                        cur.execute(sql_str)
                    except Exception as error:
                        print("Insert to CheckinTable failed!")

            conn.commit()

            line = f.readline()
            count_line +=1

        cur.close()
        conn.close()

    print(count_line)
    f.close()

def insert2ReviewTable():

    with open('C:/Users/nlers/Documents/451code/451private/milestone1/Yelp-CptS451/yelp_review.JSON','r') as f:
        line = f.readline()
        count_line = 0

        try:
            conn = psycopg2.connect("dbname='milestone1db' user='postgres' host='localhost' password='cyber626'")
        except Exception as error:
            print('Unable to connect to the database!')
        cur = conn.cursor()

        while line:
            data = json.loads(line)
            # Generate the INSERT statement for the current ReviewTable
            sql_str = "INSERT INTO Review (reviewID, userID, businessID, stars, content) " \
                      "VALUES ('" + cleanStr4SQL(data['review_id']) + "','" + cleanStr4SQL(data['user_id']) + "','" + \
                      cleanStr4SQL(data['business_id']) + "','" + str(data['stars']) + "','" + cleanStr4SQL(data['text']) + "');"

            try:
                cur.execute(sql_str)
            except Exception as error:
                print("Insert to ReviewTable failed!")

            conn.commit()

            line = f.readline()
            count_line +=1

        cur.close()
        conn.close()

    print(count_line)
    f.close()

def insert2CategoryTable(businessID, name, dbconn, connCursor):
    sql_str = "INSERT INTO Category (businessID, name) " \
    "VALUES ('" + businessID + "','" + name + "');"

    try:
        connCursor.execute(sql_str)
    except Exception as error:
        print("Insert to CategoryTable failed!")

    dbconn.commit()


def insert2TimesTable(businessID, day, openTime, closeTime, dbconn, connCursor):
    sql_str = "INSERT INTO OpenTimes (businessID, day, openTime, closeTime) " \
    "VALUES ('" + businessID + "','" + day + "','" + openTime + "','" + closeTime + "');"

    try:
        connCursor.execute(sql_str)
    except Exception as error:
        print("Insert to OpenTimes failed!")

    dbconn.commit()

def insert2UserFavoriteTable(userID, businessID, dbconn, connCursor):
    sql_str = "INSERT INTO UserFavorite (userID, businessID) " \
    "VALUES ('" + userID + businessID + "');"

    try:
        connCursor.execute(sql_str)
    except Exception as error:
        print("Insert to UserFavoriteTable failed!")

    dbconn.commit()

def insert2UserFriendTable():
    with open('C:/Users/nlers/Documents/451code/451private/milestone1/Yelp-CptS451/yelp_user.JSON','r') as f:
        line = f.readline()
        count_line = 0

        try:
            conn = psycopg2.connect("dbname='milestone1db' user='postgres' host='localhost' password='cyber626'")
        except Exception as error:
            print('Unable to connect to the database!')

        cur = conn.cursor()

        while line:
            data = json.loads(line)

            userID = cleanStr4SQL(data['user_id'])
            for item in data['friends']:
                sql_str = "INSERT INTO UserFriend(userID, friendUserID) " \
                      "VALUES ('" + userID + "','" + cleanStr4SQL(item) + "');"

                try:
                    cur.execute(sql_str)
                except Exception as error:
                    print("Insert to UserFriend failed!")

                conn.commit()

            line = f.readline()
            count_line +=1

        cur.close()
        conn.close()

    print(count_line)
    f.close()

def update():
    with open('C:/Users/nlers/Documents/451code/451private/milestone1/Yelp-CptS451/yelp_business.JSON','r') as f:
        line = f.readline()
        count_line = 0

        try:
            conn = psycopg2.connect("dbname='milestone1db' user='postgres' host='localhost' password='cyber626'")
        except Exception as error:
            print('Unable to connect to the database!')

        cur = conn.cursor()

        while line:
            data = json.loads(line)

            businessID = cleanStr4SQL(data['business_id'])

            sql_str = "update business set latitude = " + str(data['latitude']) + " , longitude = " + str(data['longitude']) + " where businessID = '" + businessID + "';"

            try:
                cur.execute(sql_str)
            except Exception as error:
                print("Insert to business failed!")

            conn.commit()

            line = f.readline()
            count_line +=1

        cur.close()
        conn.close()

    print(count_line)
    f.close()

'''
insert2BusinessTable()
insert2UserTable()
insert2CheckInTable()
insert2ReviewTable()
insert2UserFriendTable()
'''

update()
#insert2BusinessTable()