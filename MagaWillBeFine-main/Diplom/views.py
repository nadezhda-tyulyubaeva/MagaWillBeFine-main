from datetime import datetime

from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
from django.views import generic, View
from django.urls import reverse_lazy
from .forms import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import *
import calendar


def index(request):
    return render(request, 'index.html')


def events(request):
    return render(request, 'events.html')


def base(request):
    return render(request, 'base.html')


def login(request):
    return render(request, 'login.html')


class UserRegisterView(generic.CreateView):
    form_class = RegisterUserForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')


def LoginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        username.label = 'Логин'
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Неправильные учетные данные'
            form = LoginUserForm()
            context = {
                'form': form,
                'error_message': error_message
            }

        return render(request, '/home.html', context)

    else:
        form = LoginUserForm()

    context = {
        "form": form,
    }
    return render(request, "registration/login.html", context)


def registrat(request):
    data = {}

    if request.method == 'POST':

        form = RegisterUserForm(request.POST)

        if form.is_valid():
            user = form.save()
            user.save()

            profile = Profile.objects.create(user=user, klass=form.cleaned_data['klass'],
                                             patronymic=form.cleaned_data['patronymic'])
            profile.save()
            return redirect('login')
    else:
        form = RegisterUserForm()
        data['form'] = form
    return render(request, 'registration/registration.html', data)


class EventView(ListView):
    model = Event_Plan_Position
    template_name = 'posts.html'

class NewView(ListView):
    model = Post
    template_name = 'news.html'

def ReportView(request):
    status_invitation = InvitationStatus.objects.filter(Status__name='Посещено').order_by('Invitation__Event_Plan_Position__Event__name')
    positions = Event_Plan_Position.objects.all()

    for invitation in status_invitation:
        if invitation.Invitation.Team:
            team_members = Team_Members.objects.filter(Team_List__Team=invitation.Invitation.Team)

    context = {
        'status_invitation': status_invitation,
        'positions': positions,
        'team_members': team_members,
    }
    return render(request, 'reports.html', context)

class ResultsView(ListView):
    model = Results
    template_name = 'results.html'

    def get_queryset(self):
        return Results.objects.all().order_by('Invitation__Event_Plan_Position__Event__name')

class PostDetailView(DetailView):
    model = Post
    template_name = 'news_details.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['feedbacks'] = Feedback_post.objects.filter(Post=self.object)
        context['form'] = FeedbackPostForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        form = FeedbackPostForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.Profile = request.user.profile  # Assuming you have a Profile related to the User
            feedback.Time_Submit = datetime.now()
            feedback.Post = self.object
            feedback.save()
            return redirect('post_detail', pk=self.object.pk)
        context['form'] = form
        return self.render_to_response(context)

def cancel_invitation(request, pk):
    invitation = get_object_or_404(InvitationStatus, pk=pk)
    cancel_status = get_object_or_404(Status, name = 'Отменена')
    if request.method == 'POST':
        form = CancelInvitationForm(request.POST, instance=invitation)
        if form.is_valid():
            status = form.save(commit=False)
            status.Invitation = invitation.Invitation
            status.Profile = request.user.profile
            status.Status.name = 'Отменена'
            status.save()
            return redirect('profile')
    else:
        form = CancelInvitationForm()

    return render(request, 'cancel_invitation.html', {'form': form, 'invitation': invitation})

class InvitationView(View):
    def get(self, request, pk):
        event_plan_position = get_object_or_404(Event_Plan_Position, pk=pk)
        event = event_plan_position.Event
        form = InvitationForm(initial={
            'Event_Plan_Position': event_plan_position,
            'Profile': request.user.profile,
        })
        form.set_event(event, request.user.profile)
        return render(request, 'invitation_form.html', {
            'form': form,
            'event': event,
            'event_plan_position': event_plan_position
        })

    def post(self, request, pk):
        event_plan_position = get_object_or_404(Event_Plan_Position, pk=pk)
        event = event_plan_position.Event
        form = InvitationForm(request.POST, initial={
            'Event_Plan_Position': event_plan_position,
            'Profile': request.user.profile,
        })
        form.set_event(event, request.user.profile)
        if form.is_valid():
            invitation = form.save(commit=False)
            invitation.date_submitted = timezone.now()
            invitation.save()

            # Создайте запись в таблице InvitationStatus
            status = Status.objects.get(name='На рассмотрении')  # Убедитесь, что статус 'На рассмотрении' существует
            InvitationStatus.objects.create(
                Invitation=invitation,
                Status=status,
                Profile=request.user.profile,
                Description='Заявка подана и находится на рассмотрении.'
            )
            return redirect('posts')  # Укажите вашу страницу успеха
        return render(request, 'invitation_form.html', {
            'form': form,
            'event': event,
            'event_plan_position': event_plan_position
        })

def user_profile(request):
    profile = get_object_or_404(Profile, user=request.user.pk)

    status = InvitationStatus.objects.filter(Status__name='Посещено', Invitation__Profile__user=request.user.pk)
    event_result = Results.objects.filter(Invitation__Profile__user=request.user.pk)

    status_invitation = InvitationStatus.objects.filter(Invitation__Profile__user=request.user.pk).exclude(
        Status__name__in=['Посещено'])
    team = Team_Members.objects.get(Profile__user=request.user.pk)

    is_capitan = False

    if team.Team_List.Team.capitan == request.user.profile:
        is_capitan = True

    if is_capitan:
        capitan = 'Капитан'
    else:
        capitan = 'Участник'

    result_status = list(zip(status, event_result))

    context = {
        'user': request.user,
        'profile': profile,
        'result_status': result_status,
        'status_invitation': status_invitation,
        'team': team,
        'capitan': capitan
    }
    return render(request, 'profile.html', context)

def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('posts')
    else:
        form = EventForm()
    return render(request, 'create_event.html', {'form': form})

class EventPlanPositionCreateView(View):
    def get(self, request):
        form = EventPlanPositionForm()
        return render(request, 'create_event_plan.html', {'form': form})

    def post(self, request):
        form = EventPlanPositionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('posts')
        return render(request, 'create_event_plan.html', {'form': form})

class MonthlyEventPlanView(ListView):
    model = Event_Plan_Position
    template_name = 'monthly_event_plan.html'
    context_object_name = 'event_plan_positions'

    def get_queryset(self):
        current_date = now()
        first_day_of_month = current_date.replace(day=1)
        last_day_of_month = current_date.replace(day=calendar.monthrange(current_date.year, current_date.month)[1])
        return Event_Plan_Position.objects.filter(
            Event_Plan__Date_Start__lte=last_day_of_month,
            Event_Plan__Date_End__gte=first_day_of_month
        ).order_by('Date_Plan')

class EventPlanPositionUpdateView(UpdateView):
    model = Event_Plan_Position
    form_class = EventPlanPositionForm
    template_name = 'edit_event_plan_position.html'
    success_url = 'posts'

class InvitationStatusView(ListView):
    model = InvitationStatus
    template_name = 'invitation_status.html'

    def get_queryset(self):
        return InvitationStatus.objects.all().order_by('Invitation__Event_Plan_Position__Event__name', 'Status__name')

def update_invitation(request, pk):
    invitation = get_object_or_404(InvitationStatus, pk=pk)

    if request.method == 'POST':
        form = UpdateInvitationForm(request.POST, instance=invitation)
        if form.is_valid():
            status = form.save(commit=False)
            status.Invitation = invitation.Invitation
            status.Profile = request.user.profile
            status.save()
            return redirect('invitation_status')
    else:
        form = UpdateInvitationForm()

    return render(request, 'invitation_status_update.html', {'form': form, 'invitation': invitation})