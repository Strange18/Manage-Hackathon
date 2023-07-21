from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

# email needed to be sent after user creation


# Create your models here.
class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    venue = models.CharField(max_length=255)
    time = models.DateField()
    registration_required = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class registration_form(models.Model):
    team_name = models.CharField(max_length=255)
    leade_name = models.CharField(max_length=255)
    member_2 = models.CharField(max_length=255)
    member_3 = models.CharField(max_length=255, null=True, blank=True)
    member_4 = models.CharField(max_length=255, null=True, blank=True)
    leader_contact = models.CharField(max_length=15)
    leader_email = models.EmailField()
    project_idea = models.CharField(max_length=255)
    project_description = models.TextField(null=True, blank=True)
    tools_to_be_used = models.TextField()
    for_event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return self.team_name


@receiver(post_save, sender=registration_form)
def create_user(sender, instance, created, **kwargs):
    """
    A signal receiver function to create a new user when a RegistrationForm instance is saved.
    """
    if created:
        # Create a new user with the team_name as the username and '12345' as the default password
        word = get_random_string(10)
        username_processing = 'Team-' + instance.team_name
        user = User.objects.create(username=username_processing)
        user.set_password(word)
        user.save()


class submission_form(models.Model):
    team_name = models.ForeignKey(User, on_delete=models.CASCADE)
    git_repo = models.URLField()
    drive_link = models.URLField()
    description = models.TextField()

    def __str__(self):
        return self.team_name.username


class Result(models.Model):
    team_name = models.ForeignKey(User, on_delete=models.CASCADE)
    points = models.PositiveIntegerField()
    suggestion = models.TextField()
    comments = models.TextField()

    def __str__(self):
        return f'{self.team_name}-{self.points}'


class Mentor(models.Model):
    mentor_name = models.CharField(max_length=255)
    expertise = models.TextField()
    contact = models.CharField(max_length=15)
    available_time = models.TextField()

    def __str__(self):
        return self.mentor_name


class Track(models.Model):
    team = models.ForeignKey(User, on_delete=models.CASCADE)
    comments = models.TextField()

    def __str__(self):
        return self.team.username


class Notification(models.Model):
    main_heading = models.CharField(max_length=255)
    information = models.TextField()

    def __str__(self):
        return self.main_heading