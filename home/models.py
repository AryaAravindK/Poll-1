from django.db import models

# Create your models here.
class Poll(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    valid_till = models.DateTimeField()

    def __str__(self):
        return self.title

class MCQ(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    question = models.TextField()
    optionA = models.CharField(max_length=200)
    optionB = models.CharField(max_length=200)
    optionC = models.CharField(max_length=200)
    optionD = models.CharField(max_length=200)
    correct_answer = models.CharField(max_length=200)

    def __str__(self):
        return self.question

class Descriptive(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()

    def __str__(self):
        return self.question

class UserInfo(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.name

class Response(models.Model):
    user_info = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
   
   
    score = models.IntegerField(default=0)
    
    submit_time = models.DateTimeField(auto_now_add=True,null=True ,blank=True)  # Changed to DateTimeField for precision

    def __str__(self):
        return f"{self.user_info.name} - {self.poll.title} - {self.score}"

   