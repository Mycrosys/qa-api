from django.urls import path
from journal import views

urlpatterns = [
    path('journal/', views.JournalList.as_view()),
    path('journal/<int:pk>/', views.JournalDetail.as_view())
]
