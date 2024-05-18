from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

EventType_Choices = (
    ("Интеллектуальный квиз", "Интеллектуальный квиз"),
    ("Музыкальный квиз", "Музыкальный квиз"),
    ("Спортивное мероприятие", "Спортивное мероприятие"),
    ("Классическая Мафия", "Классическая Мафия"),
    ("Своя Игра", "Своя Игра"),
    ("Интеллектуальная игра 100к1", "Интеллектуальная игра 100к1"),
    ("Брейн-ринг", "Брейн-ринг")
)

EducationLevel_Choices = (
    ("Младшее звено 1-4 классы", "Младшее звено 1-4 класс"),
    ("Среднее звено 5-7 классы", "Среднее звено 5-7 классы"),
    ("Старшее звено 8-11 классы", "Старшее звено 8-11 классы")
)

klass_Choices = (
    ('5А','5А'),
    ('5Б','5Б'),
    ('5В','5В'),
    ('5Г','5Г'),
    ('6А','6А'),
    ('6Б','6Б'),
    ('6В','6В'),
    ('6Г','6Г'),
    ('7А','7А'),
    ('7Б','7Б'),
    ('7В','7В'),
    ('7Г','7Г'),
    ('8А','8А'),
    ('8Б','8Б'),
    ('8В','8В'),
    ('8Г','8Г'),
    ('9А','9А'),
    ('9Б','9Б'),
    ('9В','9В'),
    ('9Г','9Г'),
    ('10А','10А'),
    ('10Б','10Б'),
    ('10В','10В'),
    ('10Г','10Г'),
    ('11А','11А'),
    ('11Б','11Б'),
    ('11В','11В'),
    ('11Г','11Г'),
)

Status_Choices = (
    ("На рассмотрении", "На рассмотрении"),
    ("Принята", "Принята"),
    ("Отклонена", "Отклонена"),
    ("Отменена", "Отменена"),
    ("Посещено", "Посещено")
)

class EventType(models.Model):
    name = models.CharField(max_length=100,
                            verbose_name='Наименование типа мероприятия',
                            choices=EventType_Choices)

    def __str__(self):
        return self.name


class EducationLevel(models.Model):
    name = models.CharField(max_length=100,
                            verbose_name='Наименование степени обучающихся (звена)',
                            choices=EducationLevel_Choices)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images', null=True, blank=True)
    patronymic = models.CharField(max_length=255, verbose_name='Отчество (если есть)', blank=True, null=True)
    klass = models.CharField(max_length=4, verbose_name='Класс обучающегося', choices=klass_Choices, blank=True)

    def __str__(self):
        return str(self.user)

class Team(models.Model):
    name = models.CharField(max_length=255)
    date_created = models.DateTimeField(blank=True, null=True)
    date_disbanded = models.DateTimeField(blank=True, null=True)
    capitan = models.ForeignKey(Profile, on_delete=models.SET_NULL, verbose_name="Капитан", blank=True, null=True)

    def __str__(self):
        return str(self.name)

class Event(models.Model):
    name = models.CharField(max_length=255)
    max_eventers = models.IntegerField(default=100)
    image = models.ImageField(upload_to='images', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    #вид мероприятия еще был, но пока без него, забыл что он должен закрывать
    team = models.BooleanField('Командное мероприятие', null=True, blank=True)
    EventType = models.ForeignKey('EventType', on_delete=models.CASCADE)
    EducationLevel = models.ForeignKey('EducationLevel', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)


class Event_Plan(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    Date_Start = models.DateField(null=True, blank=True)
    Date_End = models.DateField(null=True, blank=True)
    Responsible = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)


class Event_Plan_Position(models.Model):
    Event_Plan = models.ForeignKey('Event_Plan', on_delete=models.PROTECT)
    Event = models.ForeignKey('Event', on_delete=models.PROTECT)
    Date = models.DateField(null=True, blank=True)
    Date_Plan = models.DateField(null=True, blank=True)
    Date_Fact = models.DateField(null=True, blank=True)
    Description = models.TextField(null=True, blank=True)
    Eventers_Plan = models.IntegerField(null=True, blank=True)
    Eventers_Fact = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.Event)

class Invitation(models.Model):
    date_submitted = models.DateField(blank=True, null=True)
    Event_Plan_Position = models.ForeignKey('Event_Plan_Position', on_delete=models.CASCADE)
    Team = models.ForeignKey('Team', on_delete=models.CASCADE, null=True, blank=True)
    Team_Members = models.ForeignKey('Team_Members', on_delete=models.CASCADE, null=True, blank=True)
    Profile = models.ForeignKey('Profile', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        if self.Profile:
            return str(self.Profile)
        else:return str(self.Team)

class Team_List(models.Model):
    Team = models.ForeignKey('Team', on_delete=models.CASCADE)


class Team_Members(models.Model):
    Team_List = models.ForeignKey('Team_List', on_delete=models.CASCADE)
    Profile = models.ForeignKey('Profile', on_delete=models.CASCADE)


class Results(models.Model):
    Team_List = models.ForeignKey('Team_List', on_delete=models.CASCADE, null=True, blank=True)
    Invitation = models.ForeignKey('Invitation', on_delete=models.CASCADE)
    Result = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.Result)


class Post(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='images', null=True, blank=True)
    Profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    date_post = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name + ' | ' + str(self.Profile)

class Feedback(models.Model):
    Feedback = models.TextField(null=True, blank=True)
    Time_Submit = models.DateTimeField(null=True, blank=True)
    Profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    Event_Plan_Position = models.ForeignKey('Event_Plan_Position', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.Feedback)

class Feedback_post(models.Model):
    Feedback = models.TextField(null=True, blank=True)
    Time_Submit = models.DateTimeField(null=True, blank=True)
    Profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    Post = models.ForeignKey('Post', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.Feedback)

class Status(models.Model):
    name = models.CharField(max_length=255, verbose_name='Статус заявки', choices=Status_Choices, blank=True, default='На рассмотрении')

    def __str__(self):
        return str(self.name)

class InvitationStatus(models.Model):
    Invitation = models.ForeignKey('Invitation', on_delete=models.CASCADE)
    Status = models.ForeignKey('Status', on_delete=models.CASCADE)
    Profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    Status_Date = models.DateField(blank=True, null=True, auto_now_add=True)
    Description = models.CharField(max_length=255, blank=True, null=True)