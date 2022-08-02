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
        on_delete=models.CASCADE,
    )
    summary = models.CharField(
        max_length=65536,
        default=''
    )
    # team_root_file = models.ForeignKey(
    #     'file.File',
    #     on_delete=models.CASCADE,
    #     related_name='xx',
    #     null=True,
    # )

    def to_dic(self):
        return {
            'team_name': self.team_name,
            'creator': self.creator.username,
        }


class C:
    founder = 2
    manager = 1
    member = 0
    invited = -1

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
    auth_choices = [
        (C.founder, 'founder'),
        (C.manager, 'manager'),
        (C.member, 'member'),
        (C.invited, 'invited')
    ]
    authority = models.IntegerField(
        choices=auth_choices,
        default=0,
    )


class Invitation(models.Model):
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
    invite_url = models.CharField(max_length=30)
