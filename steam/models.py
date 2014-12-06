from django.db import models
from django.contrib.auth.models import User

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
    user = models.OneToOneField(User, primary_key=True)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    year = models.IntegerField()
    email = models.CharField(max_length=256)
    preference = models.CharField(max_length=1)
    gender = models.CharField(max_length=1)
    voter_score = models.IntegerField()
    
    def create(cls, newuser):
        profile = cls(user=user,first_name=first_name, last_name=last_name,
            year=year, email=email, preference=preference, gender=gender,
            voter_score=voter_score)
        return profile
    

    class Meta:
        db_table = 'profile'



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


class Question(models.Model):
    qid = models.IntegerField(primary_key=True)
    question_text = models.CharField(max_length=256)

    class Meta:
       
        db_table = 'question'

class Responses(models.Model):
    user = models.ForeignKey('Profile', db_column='user')
    qid = models.ForeignKey('Question', db_column='qid')
    answer = models.CharField(max_length=256)

    class Meta:
        
        db_table = 'responses'
        unique_together = ('user','qid')

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
     uid = models.ForeignKey('Profile', db_column='uid')
     match = models.ForeignKey('Match', db_column='match',related_name='match')
     #user2 = models.IntegerField()

     class Meta:
         db_table = 'vote'
         unique_together = ('uid','match')


class RewardsScale(models.Model):
     voter_score = models.IntegerField(primary_key=True)
     title = models.CharField(max_length=256)
     
     class Meta:
         db_table = 'rewardsscale'


