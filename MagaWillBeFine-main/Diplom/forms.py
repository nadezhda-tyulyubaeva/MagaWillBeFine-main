from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from .models import *
from django.contrib.auth import get_user_model


class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(required=True, label="E-mail*", widget=forms.EmailInput(attrs={'class': 'form-input'}))
    first_name = forms.CharField(required=True, label="Имя*", widget=forms.TextInput(attrs={'class': 'form-input'}))
    last_name = forms.CharField(required=True, label="Фамилия*", widget=forms.TextInput(attrs={'class': 'form-input'}))
    patronymic = forms.CharField(required=False, label="Отчество (при наличии)",
                                 widget=forms.TextInput(attrs={'class': 'form-input'}))
    username = forms.CharField(label="Логин*", widget=forms.TextInput(attrs={'class': 'form-input'}))
    agree = forms.BooleanField(label_suffix=' ', label=' ',
                               help_text='В соответствии с Федеральным законом от 27.06.2006 № 152-ФЗ "О персональных данных" даю согласие на обработку персональных данных**.')
    klass = forms.ChoiceField(label="Класс", choices=klass_Choices, required=False)

    class Meta:
        model = User
        fields = ('last_name', 'first_name', 'patronymic', 'klass', 'email', 'username', 'password1', 'password2',
                  'agree')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Такой E-mail уже существует!")
        return email


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин',
                               widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class FeedbackPostForm(forms.ModelForm):
    class Meta:
        model = Feedback_post
        fields = ['Feedback']


from django import forms
from .models import Invitation, Team, Team_Members, Profile


class InvitationForm(forms.ModelForm):
    class Meta:
        model = Invitation
        fields = ['Event_Plan_Position', 'Team', 'Team_Members', 'Profile']
        widgets = {
            'Event_Plan_Position': forms.HiddenInput(),
            'Team': forms.HiddenInput(),
            'Profile': forms.HiddenInput(),
        }

    def set_event(self, event, profile):
        if event.team:
            self.fields['Team'].queryset = Team.objects.filter(capitan=profile)
            self.fields['Team_Members'].queryset = Team_Members.objects.filter(Team_List__Team__capitan=profile)
            self.fields['Team_Members'].label = "Выберите состав"
        else:
            del self.fields['Team']
            del self.fields['Team_Members']


class EventForm(forms.ModelForm):
    team = forms.BooleanField(label_suffix=' ', label=' ',
                              help_text='Командное мероприятие.')
    name = forms.CharField(label='Название', max_length=254, widget=forms.TextInput(
        attrs={
            'style': 'width:100%'
        })
    )

    class Meta:
        model = Event
        fields = ['name', 'max_eventers', 'image', 'description', 'team', 'EventType', 'EducationLevel']

class EventPlanPositionForm(forms.ModelForm):
    class Meta:
        model = Event_Plan_Position
        fields = ['Event_Plan', 'Event', 'Date', 'Date_Plan', 'Description', 'Eventers_Plan', 'Date_Fact', 'Eventers_Fact']


class CancelInvitationForm(forms.ModelForm):
    class Meta:
        model = InvitationStatus
        fields = ['Status', 'Description']
        widgets = {
            'Description': forms.Textarea(attrs={'rows': 4, 'cols': 120})
        }
        labels = {
            'Description': 'Причина отмены',
            'Status': 'Измените статус'
        }

    def __init__(self, *args, **kwargs):
        super(CancelInvitationForm, self).__init__(*args, **kwargs)
        self.fields['Status'] = forms.ModelChoiceField(queryset=Status.objects.filter(name='Отменена'))
        self.fields['Status'].label = 'Измените статус'

class UpdateInvitationForm(forms.ModelForm):
    class Meta:
        model = InvitationStatus
        fields = ['Status', 'Description']
        widgets = {
            'Description': forms.Textarea(attrs={'rows': 4, 'cols': 120})
        }
        labels = {
            'Description': 'Комментарий',
            'Status': 'Измените статус'
        }

    def __init__(self, *args, **kwargs):
        super(UpdateInvitationForm, self).__init__(*args, **kwargs)
        self.fields['Status'].label = 'Измените статус'

