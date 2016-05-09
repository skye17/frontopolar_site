from django.db import models

class Algorithm(models.Model):
    filename = models.CharField(default='', max_length=20, unique=True)
    name = models.CharField(default='Some algorithm', max_length=20)
    description = models.TextField(blank=True)
    algorithm = models.FileField(default='',upload_to='algorithms/')
    train_parameters = models.FileField(blank=True, null=True, upload_to='algorithms/train_params/')

class Dataset(models.Model):
    filename = models.CharField(default='', max_length=20, unique=True)
    name = models.CharField(default='Some dataset', max_length=20)
    data = models.FileField(default= '', upload_to='datasets/')
    description = models.TextField(blank=True)
    frequency = models.CharField(default='daily', max_length= 6, choices=[('daily', 'daily'), ('minute', 'minute')])
    columns = models.CharField(default='', max_length=200)
    date_format = models.CharField(blank=True, default="", max_length=50)
    class Meta:
        ordering = ['name']

class ExperimentResult(models.Model):
    info = models.TextField(default='')
    results_path = models.CharField(default='', max_length=100)

    @models.permalink
    def get_absolute_url(self):
        return ('algotesting:test_results', [str(self.pk)])
