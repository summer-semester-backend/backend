from django.db import models
from team.models import Team
from user.models import User


# Create your models here.

class Project(models.Model):
    projectID = models.AutoField(primary_key=True, editable=False)
    project_image = models.CharField(max_length=50)
    project_name = models.CharField(max_length=50)
    create_time = models.DateTimeField(auto_now_add=True)
    last_visit_time = models.DateTimeField()
    abandon_time = models.DateTimeField()
    is_active = models.ImageField(default=1)  # 1为可见,0为不可见（即在回收站）
    team = models.ForeignKey(
        Team,
        to_field='teamID',
        on_delete=models.CASCADE,
    )
    project_creator = models.ForeignKey(
        User,
        to_field='userID',
        on_delete=models.CASCADE,
    )

    # def to_dic(self):
    #     return {
    #         'project_name': self.project_name,
    #         'creator': self.creator.username,
    #     }
