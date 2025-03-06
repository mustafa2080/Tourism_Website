from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('<slug:post_slug>/', views.post_detail, name='post_detail'),
    path('category/<slug:category_slug>/', views.post_by_category, name='post_by_category'),
    path('tag/<slug:tag_slug>/', views.post_by_tag, name='post_by_tag'),
    path('like/<slug:post_slug>/', views.like_post, name='like_post'),
    path('dislike/<slug:post_slug>/', views.dislike_post, name='dislike_post'),  # مسار الكره
    path('add_comment/<slug:post_slug>/', views.add_comment, name='add_comment'),
    path('edit_comment/<int:comment_id>/', views.edit_comment, name='edit_comment'),  # مسار تعديل التعليق
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),  # مسار حذف التعليق
]