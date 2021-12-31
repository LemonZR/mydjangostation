from django.db import models


class TableData(models.Model):
    table_id = models.AutoField(primary_key=True)
    table_name = models.CharField(max_length=50)
    table_data = models.JSONField()

    def __str__(self):
        return self.table_name

    class Meta:
        ordering = ['table_id']


class TableDependence(models.Model):
    table_id = models.AutoField(primary_key=True)
    table_name = models.CharField(max_length=100)
    dependence = models.CharField(max_length=10000)

    def __str__(self):
        return self.table_name
