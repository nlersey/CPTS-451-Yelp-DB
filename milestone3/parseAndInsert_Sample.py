import json
import psycopg2

def cleanStr4SQL(s):
    return s.replace("'","`").replace("\n"," ")

def int2BoolStr (value):
    if value == 0:
        return 'False'
    else:
        return 'True'

def insert2FriendTable():
    with open('yelp_user.JSON','r') as f:    # update path for the input file
        #outfile =  open('./yelp_user.SQL', 'w')  #uncomment this line if you are writing the INSERT statements to an output file.
        line = f.readline()

        #connect to yelpdb database on postgres server using psycopg2
        try:
             #TODO: remember to delete password
            conn = psycopg2.connect("dbname='yelpdb' user='postgres' host='localhost' password='cyber626'")
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()
        while line:
            data = json.loads(line)
            for friend in data['friends']:
                sql_str="INSERT INTO hasFriend (userID, friendID) VALUES ('" + data['user_id']  + "','" + friend + "') ON CONFLICT(user_id) DO NOTHING;"
                try:
                    cur.execute(sql_str)
                except Exception as error:
                    print("Insert to hasFriend failed!", error)
                    return

def insert2UserTable():
    with open('yelp_user.JSON','r') as f:
        line = f.readline()
        count_line = 0

        try:
             #TODO: remember to delete password
            conn = psycopg2.connect("dbname='yelpdb' user='postgres' host='localhost' password='cyber626'")
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()

        while line:
            data = json.loads(line)
            userID = cleanStr4SQL(data['user_id'])

            sql_str = "INSERT INTO usertable (user_id, yelping_since, uname, review_count, fans, average_stars, funny, useful, cool, userLongitude, userLatitude, totalLikes) " \
                + "VALUES ('" + userID + "','" + str(cleanStr4SQL(data['yelping_since'])) + "','" + str(cleanStr4SQL(data['name'])) + "','" \
                + str(0) + "','" + str(data['fans']) + "','" + str(data['average_stars']) + "','" + str(data['funny']) + "','" + str(data['useful']) + "','" + str(data['cool']) + "','" \
                + str(0) + "','" + str(0) + "','" + str(0) + "');"

            try:
                cur.execute(sql_str)
            except Exception as error:
                print('Insert to usertable failed!', error)

            conn.commit()

            line = f.readline()
            count_line +=1

        cur.close()
        conn.close()

    print(count_line)
    f.close()

def insert2BusinessCategorie(id, categories, cur):
    for category in categories:
        try:
            cur.execute("INSERT INTO categories (business_id, cname) VALUES (%s, %s);", (id,  cleanStr4SQL(category)))
        except Exception as error:
            print("Insert to busCat failed!", error)
            return False
    return True

def insert2BusinessHours(id, hours, cur):
    for day in hours.keys():
        open, close = hours[day].split('-')
        try:
            cur.execute("INSERT INTO Businesshours (business_id, day, opentime, closetime) " + " VALUES (%s, %s, %s, %s)", (id, day, open, close))
        except Exception as error:
            print("Insert to Hours failed!", error)
            return
    return True

def insert2NestedBusinessAttribute(business_id, attribute, upperkey, cur):
    for x in attribute.keys():
        if type(attribute[x]) == dict:
            if not insert2NestedBusinessAttribute(business_id, attribute[x], upperkey + ':' + x, cur):
                return False
        elif type(attribute[x]) == str and (attribute[x] == 'False' or attribute[x] == 'no' or attribute[x] == 'none'):
            continue
        else:
            try:
                cur.execute("INSERT INTO attribute (business_id, aname, avalue)"
                              + " VALUES (%s, %s, %s)",
                              (business_id, upperkey + ':' + x, attribute[x]) )
            except Exception as error:
                print("Insert into nested busAttr failed", error)
                return False
    return True

def insert2BusinessAttribute(business_id, attribute, cur):
    for x in attribute.keys():
        if type(attribute[x]) == dict:
            if not insert2NestedBusinessAttribute(business_id, attribute[x], x, cur):
                return False
        elif type(attribute[x]) == str and (attribute[x] == 'False' or attribute[x] == 'no' or attribute[x] == 'none'):
            continue
        else:
            try:
                cur.execute("INSERT INTO attribute (business_id, aname, avalue)"
                              + " VALUES (%s, %s, %s)",
                              (business_id, x, attribute[x]) )
            except Exception as error:
                print("Insert into busAttr failed", error)
                return False
    return True

def insert2BusinessTable():
    #reading the JSON file
    with open('yelp_business.JSON','r') as f:    # update path for the input file
        #outfile =  open('./yelp_business.SQL', 'w')  #uncomment this line if you are writing the INSERT statements to an output file.
        line = f.readline()
        count_line = 0

        #connect to yelpdb database on postgres server using psycopg2
        #TODO: remember to delete password
        try:
            conn = psycopg2.connect("dbname='yelpdb' user='postgres' host='localhost' password='cyber626'")
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()

        while line:
            data = json.loads(line)
            business_id = cleanStr4SQL(data['business_id'])
            # Generate the INSERT statement for the current business
            # The below INSERT statement is based on a simple (and incomplete) businesstable schema. Update the statement based on your own table schema and
            # include values for all businessTable attributes
            sql_str = "INSERT INTO business (business_id, bname, bstate, city, baddress, is_open, zipcode, numcheckin, review_count, stars, latitude, longitude) " \
                      + "VALUES ('" + business_id + "','" + str(cleanStr4SQL(data['name'])) + "','" + str(cleanStr4SQL(data['state'])) + "','" \
                       + str(cleanStr4SQL(data['city'])) + "','" + str(cleanStr4SQL(data['address']))  \
                      + "','" + str((data['is_open'])) + "','" + str((data['postal_code'])) + "','" + str(0) \
                      + "','" + str(0) + "','" + str((data['stars'])) +"','" + str((data['latitude'])) + "','" + str((data['longitude'])) + "');"
            
            try:
                print(sql_str)
                cur.execute(sql_str)
            except:
                print("Insert to business failed!")
            if not insert2BusinessHours(business_id, data['hours'], cur):
                return
            if not insert2BusinessCategorie(business_id, data['categories'], cur):
                return
            if not insert2BusinessAttribute(business_id, data['attributes'], cur):
                return
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

def insert2CheckinTable():
    with open('yelp_checkin.JSON','r') as f:
        line = f.readline()
        count_line = 0
        total = 0
        try:
             #TODO: remember to delete password
            conn = psycopg2.connect("dbname='yelpdb' user='postgres' host='localhost' password='cyber626'")
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()

        while line:
            data = json.loads(line)
            business_id = cleanStr4SQL(data['business_id'])
            # Generate the INSERT statement for the current checkin
            for day in data['time']:
                for time in data['time'][day]:
                    total += data['time'][day][time]
                sql_str = "INSERT INTO checkins (business_id, day, total) " + \
                       "VALUES ('" + business_id + "','" + str(day) + "','" + str(total)  +"');"
                total = 0
                try:
                    cur.execute(sql_str)
                except Exception as error:
                    print("Insert to checkins failed!", error)

            conn.commit()

            line = f.readline()
            count_line +=1

        cur.close()
        conn.close()

    print(count_line)
    f.close()

def insert2ReviewTable():

    with open('yelp_review.JSON','r') as f:
        line = f.readline()
        count_line = 0

        try:
             #TODO: remember to delete password
            conn = psycopg2.connect("dbname='yelpdb' user='postgres' host='localhost' password='cyber626'")
        except Exception as error:
            print('Unable to connect to the database!')
        cur = conn.cursor()

        while line:
            data = json.loads(line)
            # Generate the INSERT statement for the current ReviewTable
            sql_str = "INSERT INTO review (business_id, user_id, review_date, reviewtext, stars) " \
                      "VALUES ('" + str(cleanStr4SQL(data['business_id'])) + "','" + str(cleanStr4SQL(data['user_id'])) + "','" + str(data['date']) + "','" + \
                       str(cleanStr4SQL(data['text'])) + "','"  + str(data['stars'])  + "');"

            try:
                cur.execute(sql_str)
            except Exception as error:
                print("Insert to review failed!", error)

            conn.commit()

            line = f.readline()
            count_line +=1

        cur.close()
        conn.close()

    print(count_line)
    f.close()


insert2UserTable()
insert2FriendTable()
insert2BusinessTable()
insert2CheckinTable()
insert2ReviewTable()