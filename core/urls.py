from django.conf.urls import url
from django.contrib import admin
from core.views import ChatView, ChatLoginView, MessageCreateView, logout, create_user, redirect, MessagesView

app_name = 'core'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^chat/', ChatView.as_view(), name='chat'),
    url(r'^login/', ChatLoginView.as_view(), name='login'),
    url(r'^message_create/', MessageCreateView.as_view(), name='message_create'),
    url(r'^logout/', logout, name='logout'),
    url(r'^register/', create_user, name='register'),
    url(r'^messages/', MessagesView.as_view(), name='messages'),
    url(r'/', redirect, name='index'),
]
