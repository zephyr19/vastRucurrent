from django.db import models

# Create your models here.


class MobileSensorReadings(models.Model):
    id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(blank=True, null=True, serialize=True)
    sid = models.IntegerField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    value = models.FloatField(blank=True, null=True)
    units = models.CharField(max_length=45, blank=True, null=True)
    uid = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return "{" + "timestamp: {0}, sid: {1}, longitude: {2}, latitude: {3}, value: {4}, units: {5}, uid: {6}".format(self.timestamp, self.sid, self.longitude, self.latitude, self.value, self.units, self.uid) + "}"

    class Meta:
        managed = False
        db_table = 'mobilesensorreadings'


class StaticSensorLocations(models.Model):
    sid = models.IntegerField(primary_key=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    def __str__(self):
        return "{" + "sid: {0}, latitude: {1}, longitude: {2}".format(self.sid, self.latitude, self.longitude) + "}"

    class Meta:
        managed = False
        db_table = 'staticsensorlocations'


class StaticSensorReadings(models.Model):
    id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(blank=True, null=True, serialize=True)
    sid = models.IntegerField(blank=True, null=True)
    value = models.FloatField(blank=True, null=True)
    units = models.CharField(max_length=45, blank=True, null=True)

    def __str__(self):
        return "{" + "timestamp: {0}, sid: {1}, value: {2}, units: {3}".format(self.timestamp, self.sid, self.value, self.units) + "}"

    class Meta:
        managed = False
        db_table = 'staticsensorreadings'
