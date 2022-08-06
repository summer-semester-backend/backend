from django.db import models


from django.db import models

from user.models import User


class Team(models.Model):
    teamID = models.AutoField(primary_key=True, editable=False, verbose_name='团队ID')
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
    root_file = models.ForeignKey(
        'file.File',
        on_delete=models.CASCADE,
        related_name='xx',
        null=True,
    )
    # team_root_file = models.ForeignKey(
    #     'file.File',
    #     on_delete=models.CASCADE,
    #     related_name='xx',
    #     null=True,
    # )

    def info(self):
        return {
            'teamID': int(self.teamID),
            'teamName': self.team_name,
            'createTime': str(self.create_time)[:10],
            'creator': self.creator.username,
        }


class C:
    founder = 2
    manager = 1
    member = 0
    invited = -1

    @staticmethod
    def trans(auth):
        if auth == C.founder:
            return '创建者'
        if auth == C.manager:
            return '管理员'
        if auth == C.member:
            return '成员'
        if auth == C.invited:
            return '已被邀请'
        print(auth)
        assert '程序不应该' == '来到这里'


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
    invite_code = models.CharField(max_length=100,null=True)
    create_time = models.DateTimeField(auto_now_add=True,null=True)