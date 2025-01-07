from django.db import models
from django.conf import settings
    

class EventGroup(models.Model):
    title = models.CharField(max_length=200)
    start_date = models.DateTimeField(null=True, blank=True, editable=False)
    end_date = models.DateTimeField(null=True, blank=True, editable=False)
    description = models.TextField()

    def __str__(self):
        return self.title


class EventDepartament(models.Model):
    departament = models.CharField(max_length=50)

    def __str__(self):
        return self.departament
    

class Event(models.Model):

    STATUS_CHOICES = [
        ('aberto', 'Aberto'),
        ('pendente', 'Pendente'),
        ('encerrado', 'Encerrado'),
    ]

    TYPE_CHOICES = [
        ('interno', 'Interno'),
        ('externo', 'Externo')
    ]

    title = models.CharField(max_length=200)
    location = models.CharField(max_length=200, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    duration = models.PositiveIntegerField(blank=True, null=True)
    kind = models.CharField(max_length=10, choices=TYPE_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='aberto')
    departament = models.ForeignKey(EventDepartament, on_delete=models.CASCADE, related_name='departaments', null=True, blank=True)
    main_group = models.ForeignKey(EventGroup, on_delete=models.CASCADE, related_name='groups', null=True, blank=True)
    description = models.TextField()
    photo = models.ImageField(upload_to='events/', blank=True, null=True)
    qrcode = models.ImageField(upload_to='qrcode/', blank=True, null=True)
    token = models.CharField(max_length=8, unique=True, blank=True, null=True)

    def __str__(self):
        return self.title