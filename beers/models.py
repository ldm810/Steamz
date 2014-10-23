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

class Bar(models.Model):
    name = models.CharField(max_length=20, primary_key=True)
    address = models.CharField(max_length=20, blank=True)
    class Meta:
        # Without being set, the default table name will start with the app
        # name followed by '_'; we just want the simple table names here:
        db_table = u'bar'
    def __unicode__(self):
        # Allow objects to be shown using primary key, e.g., 'The Edge'
        # instead of 'Bar Object':
        return self.pk

class Drinker(models.Model):
    name = models.CharField(max_length=20, primary_key=True)
    address = models.CharField(max_length=20, blank=True)
    class Meta:
        db_table = u'drinker'
    def __unicode__(self):
        return self.pk

class Frequents(models.Model):
    drinker = models.ForeignKey(Drinker, db_column='drinker')
    bar = models.ForeignKey(Bar, db_column='bar')
    times_a_week = models.SmallIntegerField(null=True, blank=True)
    class Meta:
        db_table = u'frequents'
        unique_together = (('drinker', 'bar'),)

class Beer(models.Model):
    name = models.CharField(max_length=20, primary_key=True)
    brewer = models.CharField(max_length=20, blank=True)
    class Meta:
        db_table = u'beer'
    def __unicode__(self):
        return self.pk

class Serves(models.Model):
    bar = models.ForeignKey(Bar, db_column='bar')
    beer = models.ForeignKey(Beer, db_column='beer')
    price = models.DecimalField(null=True, max_digits=5, decimal_places=2, blank=True)
    class Meta:
        db_table = u'serves'
        unique_together = (('bar', 'beer'),)

class Likes(models.Model):
    drinker = models.ForeignKey(Drinker, db_column='drinker')
    beer = models.ForeignKey(Beer, db_column='beer')
    class Meta:
        db_table = u'likes'
        unique_together = (('drinker', 'beer'),)
