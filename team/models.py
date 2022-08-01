from django.db import models


from django.db import models

from user.models import User


class Team(models.Model):
    teamID = models.AutoField(primary_key=True, editable=False)
    team_name = models.CharField(max_length=50)
    team_avatar = models.ImageField(upload_to='team_avatar')
    create_time = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(
        User,
        to_field='userID',
        on_delete=models.CASCADE
    )
    manager = models.ForeignKey(
        User,
        to_field='userID',
        on_delete=models.CASCADE
    )
    team_root_file = models.ForeignKey(
        'file.File',
        on_delete=models.CASCADE,
        related_name='xx',
        null=True,
    )

    def to_dic(self):
        return {
            'team_name': self.team_name,
            'manager': self.manager.username,
        }


class Team_User(models.Model):
    team = models.ForeignKey(
        Team,
        to_field='teamID',
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        to_field='userID',
        on_delete=models.CASCADE,
    )
    founder = '0'
    manager = '1'
    member = '2'
    character_choices = [
        (founder, 'founder'),
        (manager, 'manager'),
        (member, 'member'),
    ]
    character = models.CharField(
        max_length=1,
        choices=character_choices,
        default=member,
    )

