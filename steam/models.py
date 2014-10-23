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

    class Meta:
        managed = False
        db_table = 'profile'

class Personality(models.Model):
    uid = models.ForeignKey('Profile', db_column='uid')
    type = models.CharField(max_length=1)
    score = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'personality'

class Question(models.Model):
    qid = models.IntegerField(primary_key=True)
    question_text = models.CharField(max_length=256)
    type = models.CharField(max_length=128)

    class Meta:
        managed = False
        db_table = 'question'

class Responses(models.Model):
    uid = models.ForeignKey(Profile, db_column='uid')
    qid = models.ForeignKey(Question, db_column='qid')
    answer = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'responses'


# class Match(models.Model):
#     user1 = models.ForeignKey('Profile', db_column='uid')
#     user2 = models.ForeignKey('Profile', db_column='uid')
#     accept1 = models.CharField(max_length=1, blank=True)
#     accept2 = models.CharField(max_length=1, blank=True)
#     date_set = models.CharField(max_length=1, blank=True)

#     class Meta:
#         managed = False
#         db_table = 'match'


# class Vote(models.Model):
#     y_or_n = models.CharField(max_length=1)
#     uid = models.ForeignKey(Profile, db_column='uid')
#     user1 = models.ForeignKey(Match, db_column='user1')
#     user2 = models.IntegerField()

#     class Meta:
#         managed = False
#         db_table = 'vote'
