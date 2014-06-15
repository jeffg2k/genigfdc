import peewee as pw
from peewee import *
import os, traceback, sys
import datetime

db_host = os.getenv('GENI_DB_HOST', '')
db_name = os.getenv('GENI_DB_NAME', '')
db_user = os.getenv('GENI_DB_USER', '')
db_passwd = os.getenv('GENI_DB_PASSWD', '')
step_threshold = 50

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

class GeniProfile(Model):
    gid = PrimaryKeyField()
    profileId = CharField()
    profileName = CharField()
    profileLink = CharField()
    step = IntegerField()
    profiles = IntegerField()
    runDate = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = myDB
        db_table = 'geni_profiles'
        #primary_key = CompositeKey('profileId', 'step')
        indexes = (
            # create a unique index
            (('profileId', 'step'), True),
        )

class GeniJob(Model):
    jid = PrimaryKeyField()
    profileId = CharField()
    guid = CharField()
    apiKey = CharField()
    step = IntegerField()
    email = CharField()
    dbSave = CharField()
    status = IntegerField()

    class Meta:
        database = myDB
        db_table = 'geni_job'

def saveGeniProfile(stepData, name, guid, link):
    print 'saveGeniProfile is called'

    myDB.connect()
    try:
        #Check if existing profile
        profile = GeniProfile.select().where(GeniProfile.profileId == guid,
                                             GeniProfile.step == stepData['step']).get()
        if(profile != None):
            #existing record, update counts
            q = GeniProfile.update(profiles=stepData['total'], profileName = name).where(
                            GeniProfile.profileId == guid, GeniProfile.step == stepData['step'])
            q.execute()
    except Exception as e:
        #No worries. new record
        profile = GeniProfile.create(
                        profileId = guid,
                        profileName = name,
                        profileLink = link,
                        step = stepData['step'],
                        profiles = stepData['total']
                        )
        myDB.close()

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

def getTop10Profiles():
    steps = []
    try:
        myDB.connect()
        for i in range(1,11):
            rows = GeniProfile.select().where(GeniProfile.step == i).order_by(GeniProfile.profiles.desc())
            currentRow = 1
            for row in rows:
                if((currentRow == 1) or (currentRow > 1 and lastCount == row.profiles)) :
                    steps.append({'profileId':row.profileId,
                              'profileName':row.profileName,
                              'profileLink':row.profileLink,
                              'step':row.step,
                              'profiles':row.profiles
                              })
                else:
                    break
                currentRow = currentRow + 1
                lastCount = row.profiles
    except:
        traceback.print_exc(file=sys.stdout)
    myDB.close()
    data = {}
    data['top50'] = steps
    return steps

def getTop50Profiles(stepCount):
    steps = []
    try:
        myDB.connect()
        rows = GeniProfile.select().where(GeniProfile.step == stepCount).order_by(GeniProfile.profiles.desc()).limit(step_threshold)
        for row in rows:
            steps.append({'profileId':row.profileId,
                'profileName':row.profileName,
                'profileLink':row.profileLink,
                'step':row.step,
                'profiles':row.profiles
            })
    except:
        traceback.print_exc(file=sys.stdout)
    myDB.close()
    #data = {}
    #data['top50'] = steps
    #print data
    return steps

def getTop50StepProfiles(step):
    try:
        myDB.connect()
        top = GeniProfile.select(GeniProfile.step == step).order_by(GeniProfile.profiles.desc()).limit(step_threshold)
        for t in top:
            steps.append({'profileId':t.profileId,
                          'profileLink':t.profileLink,
                          'step':t.step,
                          'profiles':t.profiles
                          })
    except:
        traceback.print_exc(file=sys.stdout)
    myDB.close()
    return steps

def getJobs():
    jobs = None
    try:
        myDB.connect()
        jobs = GeniJob.select(GeniJob.status == 'N')
    except:
        traceback.print_exc(file=sys.stdout)
    myDB.close()
    return jobs

def updateJob(jid):
    try:
        myDB.connect()
        q = GeniJob.update(status='Y').where(GeniJob.jid == jid)
        q.execute()
    except:
        traceback.print_exc(file=sys.stdout)
    myDB.close()

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

myDB.connect()
TopProfiles.create_table(True)
GeniProfile.create_table(True)
GeniJob.create_table(True)
myDB.close()
print 'db connect and tables created'