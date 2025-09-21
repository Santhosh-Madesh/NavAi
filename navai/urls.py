from django.urls import path
from django.conf import settings
from django.views.static import serve
from django.urls import re_path
from django.conf.urls.static import static
from .views import chatbot, chat_page

urlpatterns = [
    path("", chat_page, name="chat_page"),
    path("chatbot/", chatbot, name="chatbot"),
]

# ✅ Serve media files in development
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
