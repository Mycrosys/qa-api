from django.urls import path
from issues import views

urlpatterns = [
    path('issues/', views.IssueList.as_view()),
    path('issues/<int:pk>/', views.IssueDetail.as_view())
]
