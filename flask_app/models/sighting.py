from unittest import result
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Sighting:
    db_name="sightings"
    def __init__(self, db_data):
        self.id = db_data['id']
        self.location = db_data['location']
        self.description = db_data['description']
        self.date_made = db_data['date_made']
        self.numberOf = db_data['numberOf']
        self.user_id = db_data['user_id']
        self.creator= db_data['creator']
        self.dontTrust = db_data['dontTrust']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.users_who_is_skeptic = []
        self.users_who_is_skepticFullName = []

    @classmethod
    def save(cls, data):
        query = "INSERT INTO sightings (location, description, date_made, numberOf, creator,  user_id) VALUES (%(location)s, %(description)s, %(date_made)s, %(numberOf)s, %(user_fullname)s , %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM sightings WHERE sightings.id = %(sighting_id)s;"
        results =  connectToMySQL(cls.db_name).query_db(query, data)
        return  cls(results[0])

    @classmethod
    def update(cls, data):
        query = "UPDATE sightings SET location=%(location)s, description =  %(description)s, date_made=%(date_made)s, numberOf=%(numberOf)s WHERE sightings.id = %(sighting_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def updateSkeptic(cls, data):
        query = "UPDATE sightings SET dontTrust=%(dontTrust)s WHERE sightings.id = %(sighting_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)


    @classmethod
    def get_all(cls):
        query= "SELECT * FROM sightings LEFT JOIN users ON sightings.user_id = users.id;"
        results = connectToMySQL(cls.db_name).query_db(query)
        all_sightings= []
        for row in results:
            all_sightings.append(row)
        return all_sightings
    
    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM sightings WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @staticmethod
    def validate_sighting(sighting):
        is_valid = True
        if len(sighting['location'])<1:
            flash('Location is required!', "sighting")
            is_valid=False
        if len(sighting['description'])<1:
            flash('Enter what happened!', "sighting")
            is_valid=False
        if sighting['date_made'] == "":
            flash('Please enter a date', "sighting")
            is_valid=False
        if int(sighting['numberOf'], 10) < 1:
            flash('Number of Sasquatches should be bigger than 1', "sighting")
            is_valid=False
        return is_valid
    
    @classmethod
    def addSkeptic(cls, data):
        query = "INSERT INTO skeptics (sightings_id,users_id) VALUES (%(sighting_id)s,%(user_id)s);"
        return connectToMySQL('sightings').query_db(query,data)


    @classmethod
    def getUsersWhoIsSkeptic(cls, data):
        query = "SELECT * FROM skeptics LEFT JOIN sightings ON skeptics.sightings_id = sightings.id LEFT JOIN users ON skeptics.users_id = users.id WHERE sightings.id = %(sighting_id)s;"
        results = connectToMySQL('sightings').query_db(query,data)
        mySighting = Sighting.get_one(data)
        for row in results:
            mySighting.users_who_is_skeptic.append(row['email'])
            mySighting.users_who_is_skepticFullName.append(row['first_name'] + ' ' + row['last_name'])
        mySighting.dontTrust=len(mySighting.users_who_is_skeptic)
        return mySighting