from django.db import models
from django.contrib.auth.models import User

class Election(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return self.title

class Candidate(models.Model):
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    party = models.CharField(max_length=100)
    vote_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} ({self.party})"

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'election')  # Prevent multiple votes per election

class Query(models.Model):
    BRANCH_CHOICES = [
        ('CSE', 'CSE'),
        ('CIVIL', 'Civil'),
        ('ELECTRICAL', 'Electrical'),
        ('MECHANICAL', 'Mechanical'),
        ('BIO-TECH', 'Bio-Tech'),
    ]
    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    branch = models.CharField(max_length=20, choices=BRANCH_CHOICES)
    query = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.branch}"