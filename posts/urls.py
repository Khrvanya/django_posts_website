from django.urls import path
 
# from .views import HomeView # , DateOrderHomeView, BackDateOrderHomeView
from .views import PostView, PostCreateView, PostsListView

app_name = 'posts'
urlpatterns = [
    path('<int:pk>/', PostView.as_view(), name='post-view'), 
    path('create_post/', PostCreateView.as_view(), name='createpost-view'),
    path('', PostsListView.as_view(), name='posts-view'),
   
]