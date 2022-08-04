from django.db import models
from team.models import Team
from user.models import User


class FType:
    root = 0
    project = 1
    directory = 2
    uml = 12
    prototype = 13
    text = 14


class File(models.Model):
    fileID = models.AutoField(primary_key=True, editable=False)
    file_image = models.CharField(max_length=50, null=True)
    file_name = models.CharField(max_length=50)
    create_time = models.DateTimeField(auto_now_add=True)
    last_visit_time = models.DateTimeField(auto_now=True)
    team = models.ForeignKey(
        Team,
        to_field='teamID',
        on_delete=models.CASCADE,
    )
    father = models.ForeignKey(
        'File',
        on_delete=models.CASCADE,
        null=True,
    )
    file_creator = models.ForeignKey(
        User,
        to_field='userID',
        on_delete=models.CASCADE,
    )
    data = models.TextField(default='')
    is_deleted = models.BooleanField(default=False)
    file_types = [
        (FType.root, 'root'),
        (FType.project, 'project'),
        (FType.directory, 'directory'),
        (FType.uml, 'uml'),
        (FType.prototype, 'prototype'),
        (FType.text, 'text'),
    ]
    type = models.IntegerField(choices=file_types)

    def deletable(self):
        return self.type >= FType.project

    def is_dir(self):
        return self.type <= FType.directory