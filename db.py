import peewee as pw
from peewee import *
import os

db_host = os.getenv('GENI_DB_HOST', '')
db_name = os.getenv('GENI_DB_NAME', '')
db_user = os.getenv('GENI_DB_USER', '')
db_passwd = os.getenv('GENI_DB_PASSWD', '')

myDB = pw.MySQLDatabase(db_name, host=db_host,
                        port=3306, user=db_user, passwd=db_passwd)

class TopProfiles(Model):
    profileId = CharField(primary_key=True) #PrimaryKeyField()
    profileLink = CharField()
    steps = IntegerField()
    profiles = IntegerField()

    class Meta:
        database = myDB
        db_table = 'geni_top_profiles'
        order_by = ('profiles',)

def saveProfile(record):
    print 'saveProfile is called'
    try:
        myDB.connect()
        #Check if existing profile
        profile = TopProfiles.select().where(TopProfiles.profileId == record['profileId']).get()
        if(profile.profiles < record['profiles']):
            #existing record, update counts
            q = TopProfiles.update(steps=record['steps'], profiles=record['profiles']).where(TopProfiles.profileId == record['profileId'])
            q.execute()
    except Exception as e:
        #No worries. new record
        profile = TopProfiles.create(
            profileId=record['profileId'],
            profileLink=record['profileLink'],
            steps=record['steps'],
            profiles=record['profiles']
        )
    myDB.close()

#.order_by(Tweet.created_date.desc()))
def getTopProfiles():
    try:
        myDB.connect()
        top = TopProfiles.select().order_by(TopProfiles.profiles.desc()).limit(50)
        steps = []
        count = 1
        for t in top:
            steps.append({'profileId':t.profileId,
                          'profileLink':t.profileLink,
                          'steps':t.steps,
                          'profiles':t.profiles
                          })
    except:
        traceback.print_exc(file=sys.stdout)
    myDB.close()
    return steps

def updateTop50(userLink, stepCount, totalProfiles):
    record = {}
    #Get GUID from public url
    url = userLink
    guid = url[url.rindex('/')+1:]
    record['profileId'] = guid
    record['profileLink'] = userLink
    record['steps'] = stepCount
    record['profiles'] = totalProfiles
    saveProfile(record)

myDB.connect()
TopProfiles.create_table(True)
myDB.close()
print 'db connect and tables created'