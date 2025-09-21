from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import chatbot, chat_page

urlpatterns = [
    path("", chat_page, name="chat_page"),
    path("chatbot/", chatbot, name="chatbot"),
]

# ✅ Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
