from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing",views.create_listing,name="create_listing"),
    path("categories/",views.categories,name="categories"),
    path("crca",views.create_category,name="crca"),
    path("watchlist",views.watchlist,name="watchlist"),
    path("watch/<int:id>",views.watch,name="watch"),
    path("close/<int:id>",views.close,name="close"),
    path("get_category/<str:category>",views.get_category,name="get_category"),
    path("details/<int:id>",views.details,name="details"),
    path("process_comment/<int:id>",views.process_comment,name="process_comment"),
    path("process_bid/<int:id>",views.process_bid,name="process_bid"),
]
