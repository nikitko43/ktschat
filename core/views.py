import json

from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseNotAllowed, HttpResponseBadRequest, HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.views.generic import TemplateView, CreateView
from django.forms import forms, model_to_dict

from django.contrib.auth import get_user_model
User = get_user_model()

from core.forms import LoginForm, MessageCreateForm, ChatUserCreationForm
from core.models import Message


class ChatView(LoginRequiredMixin, TemplateView):
    template_name = 'chat.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        data['messages'] = Message.objects.all()
        data['avatars'] = User.objects.filter(username__in=data['messages'].values_list('author')).all()
        data['users_avatars'] = data['avatars'].values_list('username', flat=True).exclude(avatar='')
        data['title'] = "Тип чат"
        return data


class MessagesView(LoginRequiredMixin, TemplateView):
    template_name = 'messages.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        last_id = self.request.GET.get('last_id')

        messages = Message.objects.filter(id__gt=last_id).order_by('id')

        data['messages'] = messages
        data['avatars'] = User.objects.filter(username__in=data['messages'].values_list('author')).all()
        data['users_avatars'] = data['avatars'].values_list('username', flat=True).exclude(avatar='')
        return data

class ChatLoginView(LoginView):
    template_name = 'login.html'
    form_class = LoginForm
    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['form_action'] = reverse('core:login')
        return data

    def get_success_url(self):
        return reverse('core:chat')

class MessageCreateView(CreateView):
    form_class = MessageCreateForm

    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(['post'])

    def get_success_url(self):
        return reverse('core:chat')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_invalid(self, form):
        return HttpResponse('')

    def form_valid(self, form):
        super().form_valid(form)
        return HttpResponse('')

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('core:login'))

def redirect(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('core:chat'))
    else:
        return HttpResponseRedirect(reverse('core:login'))

def register_user(request):
    if request.method == 'POST':
        form = ChatUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            print(form.cleaned_data['avatar'])
            return HttpResponseRedirect(reverse('core:chat'))
        else:
            return HttpResponse("123")

    else:
        form = ChatUserCreationForm()
        return render(request, 'register.html', {'form': form})

class RegisterUser(CreateView):
    form_class = ChatUserCreationForm

    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(['post'])

    def get_success_url(self):
        return reverse('core:chat')

    def form_invalid(self, form):
        return HttpResponse('Invalid form')

    def form_valid(self, form):
        super().form_valid(form)
        return HttpResponseRedirect(reverse('core:login'))

