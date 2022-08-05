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
    available_list = [root, project, directory, uml, prototype, text]


class File(models.Model):
    fileID = models.AutoField(primary_key=True, editable=False)
    file_image = models.CharField(max_length=50, null=True)
    file_name = models.CharField(max_length=50)
    create_time = models.DateTimeField(auto_now_add=True)
    last_visit_time = models.DateTimeField(auto_now=True)
    abandon_time = models.DateTimeField(null=True)
    team = models.ForeignKey(
        Team,
        to_field='teamID',
        on_delete=models.CASCADE,
        null=True,
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

    def info(self):
        """文件基本信息"""
        return {
            'fileID': self.fileID,
            'fileName': self.file_name,
            'fileType': self.type,
            'fileImage': self.file_image,
            'fatherID': self.father.fileID if self.father is not None else '',
            'teamName': self.team.team_name if self.team is not None else '',
            'userName': self.file_creator.username,
            'createTime': self.create_time,
            'lastEditTime': self.last_visit_time,
        }

    def content(self):
        """文件夹下属文件信息, 或文件数据"""
        if self.is_dir():
            son_list = File.objects.filter(father=self)
            return list(map(lambda x: x.info(), son_list))
        else:
            return {'data': self.data}
