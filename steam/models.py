from django.db import models

# If you have already designed a SQL database schema (a situation that Django
# calls "legacy databases"), you can create it first in a database with SQL,
# and then have Django inspect the database and generate a model for you.  Just
# type "./manage.py inspectdb" and copy and paste the relevant portion.
# Beware, however, that Django's behavior may not match you expect from your
# legacy database.  For example, Django does not support multi-column primary
# keys.  Therefore, with the model you get, you should always run "./manage.py
# sqlall YOUR_APP_NAME_HERE", examine the resulting SQL code, and revise your
# design accordingly.  In the end, the safest thing to do is to wipe your
# database clean (export any existing data that you would want to import
# later), and have Django create it for you from scratch with "./manage.py
# syncdb".



class Profile(models.Model):
    uid = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    year = models.IntegerField()
    email = models.CharField(max_length=256)
    preference = models.CharField(max_length=1)
    gender = models.CharField(max_length=1)
    verified = models.CharField(max_length=1)
    password = models.CharField(max_length=256)
    voter_score = models.IntegerField()
    school_key = models.ForeignKey('School', db_column='school_key') 

    class Meta:
        db_table = 'profile'

class School(models.Model):
    school_key_prime = models.IntegerField(primary_key=True)
    school_name = models.CharField(max_length=256)
    email_suffix = models.CharField(max_length=256)

    class Meta:
        db_table = 'school'

class AutoDateTimeField(models.DateTimeField):
    def pre_save(self, model_instance, add):
        return datetime.datetime.now()


class RequestFriendship(models.Model):
    initiator = models.ForeignKey('Profile', db_column='uid1',related_name='initiator')
    friended = models.ForeignKey('Profile', db_column='uid2',related_name='friended') 
    accepted = models.CharField(max_length=1)
    time_requested = models.DateTimeField()
    time_response = models.DateTimeField()
  
    class Meta:
        db_table = 'requestfriendship'
        unique_together = ('initiator','friended','time_requested')


class Friendship(models.Model):
    friend1 = models.ForeignKey('Profile', db_column='uid1',related_name='friend1') 
    friend2 = models.ForeignKey('Profile', db_column='uid2',related_name='friend2')

    class Meta:
        db_table = 'friendship'
        unique_together = ('friend1','friend2')


class Defriend(models.Model):
    defriend_initiator = models.ForeignKey('Profile', db_column='uid1',related_name='defriend_initiator')
    defriended = models.ForeignKey('Profile', db_column='uid2',related_name='defriended')
    time_defriended = models.DateTimeField() 

    class Meta:
        db_table = 'defriend'
        unique_together = ('defriend_initiator','defriended','time_defriended')


class Personality(models.Model):
    uid = models.ForeignKey('Profile', db_column='uid')
    type = models.CharField(max_length=1)
    score = models.IntegerField()

    class Meta:
       
        db_table = 'personality'

class Question(models.Model):
    qid = models.IntegerField(primary_key=True)
    question_text = models.CharField(max_length=256)
    type = models.CharField(max_length=128)

    class Meta:
       
        db_table = 'question'

class Responses(models.Model):
    uid = models.ForeignKey(Profile, db_column='uid')
    qid = models.ForeignKey(Question, db_column='qid')
    answer = models.CharField(max_length=1)

    class Meta:
        
        db_table = 'responses'
        unique_together = ('uid','qid')

class Match(models.Model):
     user1 = models.ForeignKey('Profile', db_column='uid1',related_name='related_column_uid1')
     user2 = models.ForeignKey('Profile', db_column='uid2',related_name='related_column_uid2' )
     accept1 = models.CharField(max_length=1, blank=True)
     accept2 = models.CharField(max_length=1, blank=True)
     date_set = models.DateTimeField()

     class Meta:
         
         db_table = 'match'
         unique_together = ('user1','user2')





class Vote(models.Model):
     y_or_n = models.CharField(max_length=1)
     uid = models.ForeignKey(Profile, db_column='uid')
     user1 = models.ForeignKey(Match, db_column='user1')
     user2 = models.IntegerField()

     class Meta:
         db_table = 'vote'
         unique_together = ('uid','user1','user2')


class RewardsScale(models.Model):
     voter_score = models.IntegerField(primary_key=True)
     title = models.CharField(max_length=1)
     
     class Meta:
         db_table = 'rewardsscale'


