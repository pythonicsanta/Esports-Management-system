from django.urls import path
from . views import PostListView,PostDetailView,PostCreateView,PostUpdateView,PostDeleteView
from . import views


urlpatterns = [
#    path('',views.home, name='blog-home'),
    path('',PostListView.as_view(), name='blog-home'),
    path('post/<int:pk>/',PostDetailView.as_view(), name='post-detail'),
    path('post/new/',PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update',PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete',PostDeleteView.as_view(), name='post-delete'),
#    path('post/<int:pk>/reg',SlotCreateView.as_view(), name='post-reg'),
    path('post/<int:pk>/book',views.slot_book, name='post-book'),
    path('post/<int:pk>/registerations',views.view_regeistered, name='post-registerations'),
    path('post/<int:pk>/roomdetails',views.room_details, name='post-room-details'),
    path('post/<int:pk>/result',views.match_result, name='post-result'),
    path('post/<int:pk>/resultpic',views.match_result_images, name='post-result-image'),
    path('about/',views.about, name='blog-about'),

    #url(r'^payment/', 'views.payment', name='payment'),
]
