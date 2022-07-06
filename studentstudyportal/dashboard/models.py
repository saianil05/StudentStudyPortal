from pyexpat import model
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
#Database for notes
class Notes(models.Model): 
    user=models.ForeignKey(User,on_delete=models.CASCADE) #when user is delete then user related notes also get deleted 
    title=models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.title

    #to remove s example in admin database we will get s at the end ex user-->users groups now we create Notes db we get Notess in DB to remove s
    class Meta:
        verbose_name = "notes"
        verbose_name_plural="notes"

#databse foe homework
""""
class Homework(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    subject=models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    description=models.TextField()
    due=models.DateTimeField()
    is_finished=models.BooleanField(default=False)

    def __str__(self):
        return self.title
        """


#databas for todo
class Todo(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    title=models.CharField(max_length=100)
    is_finished=models.BooleanField(default=False)

    def __str__(self):
        return self.title

    