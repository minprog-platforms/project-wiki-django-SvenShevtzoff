from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"), 
    path("wiki/<str:title>", views.entry, name="entry"), 
    path("search_results", views.search_results, name="search_results"), 
    path("error", views.error, name="error"), 
    path("new_page", views.new_page, name="new"), 
    path("random", views.random, name="random"), 
    path("edit/<str:title>", views.edit_page, name="edit")
]
