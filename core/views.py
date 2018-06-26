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
from django.forms import forms

from core.forms import LoginForm, MessageCreateForm, ChatUserCreationForm
from core.models import Message


class ChatView(LoginRequiredMixin, TemplateView):
    template_name = 'base.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        data['messages'] = Message.objects.all()
        data['title'] = "Тип чат"
        return data


class MessagesView(LoginRequiredMixin, TemplateView):
    template_name = 'messages.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        last_id = self.request.GET.get('last_id')

        messages = Message.objects.filter(id__gt=last_id).order_by('-id')

        data['messages'] =  messages
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

    def form_valid(self, form):
        super().form_valid(form)
        return JsonResponse({
            'id': self.object.id,
            'text': self.object.text,
            'author': self.object.author.username,
            'time': self.object.time,
            'rendered_template': render_to_string('message.html', {'m': self.object}, self.request)
        })

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('core:login'))

def redirect(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('core:chat'))
    else:
        return HttpResponseRedirect(reverse('core:login'))

def create_user(request):
    if request.method == 'POST':
        form = ChatUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('core:chat'))
        else:
            return HttpResponse("123")

    else:
        form = ChatUserCreationForm()
        return render(request, 'register.html', {'form': form})
