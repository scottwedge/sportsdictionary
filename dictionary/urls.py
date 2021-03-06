from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('search/', views.SearchResultsView.as_view(), name='search'),
    path('terms/<slug:sport_slug>/', views.SportIndexView.as_view(), name='sport_index'),
    path('term/random/', views.random_term, name='random_term'),
    path('term/<slug:sport_slug>/<slug:term_slug>', views.TermDetailView.as_view(), name='term_detail'),
]
