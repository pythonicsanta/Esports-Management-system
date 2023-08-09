from django.db import models
from django.utils import timezone
from users.models import User
from django.urls import reverse

# Create your models here.
class Post(models.Model):
    MY_CHOICES = (
    ('SOLO', 'SOLO'),
    ('DUO', 'DUO'),
    ('SQUAD','SQUAD')
)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    match_date = models.DateTimeField(default=timezone.now)
    match_type=models.CharField(max_length=10,choices=MY_CHOICES,default='SOLO')
    description = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    num_seats = models.IntegerField(null=True)
    entry_fee = models.IntegerField(null=False,default=0)
    prize=  models.IntegerField(null=False,default=0)
    per_kill = models.CharField(max_length=10,default=0)
    room_details = models.CharField(max_length=60,default='Room id :--')


    def __str__(self):
        return f'{self.id} {self.author}\'s POST'

    def get_absolute_url(self):
        return reverse('post-detail',kwargs={'pk':self.pk})

class Participants(models.Model):
    post_id = models.ForeignKey(Post,on_delete=models.CASCADE)
    player_id = models.ForeignKey(User,on_delete=models.CASCADE)
    order_id = models.CharField(max_length=20,default= '',blank=False)
    mobilenumber = models.IntegerField(null=False,blank=True,default=8519002741)
    player1=models.CharField(max_length=10,default= '',blank=False)
    player2=models.CharField(max_length=10,default= '',blank=True)
    player3=models.CharField(max_length=10,default= '',blank=True)
    player4=models.CharField(max_length=10,default= '',blank=True)
    kills=models.IntegerField(blank=False,default=0)
    attendance=models.BooleanField(default=True)
    def __str__(self):
        return f'{self.player_id} Booked {self.post_id}'

class Slot(models.Model):
    post_id = models.ForeignKey(Post,on_delete=models.CASCADE)
    player_id = models.ForeignKey(User,on_delete=models.CASCADE)
    players = models.ForeignKey(Participants,on_delete=models.CASCADE)
    match = models.CharField(max_length=10,default= 'SOLO')
    slot_num = models.IntegerField(blank=True,default=1)
    booktime = models.DateTimeField(auto_now_add=True)
    order_id = models.CharField(max_length=20,default= '',blank=False)

    def __str__(self):
        return f'Post {self.post_id}'



class Result(models.Model):
    post_id=models.ForeignKey(Post,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='results',blank=True,null=True,verbose_name='Image')


    def __str__(self):
        return f'Result os post {self.post_id.id} by {self.post_id.author} '
