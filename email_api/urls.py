from django.contrib import admin
from django.urls import path
from emails.views import SendSelectionEmailView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/send-selection-email/', SendSelectionEmailView.as_view(), name='send-selection-email'),
]