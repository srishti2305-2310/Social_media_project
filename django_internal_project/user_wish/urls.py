from django.urls import path
from user_wish.views import UserWishAdd,get_user_wish,user_wish_update,user_wish_delete


urlpatterns = [
    path('tag-wish/', UserWishAdd, name='tag-wish'),
    path('get-wish/', get_user_wish, name='get-wish'),
    path('<int:pk>/update/', user_wish_update, name='user-wish-update'),
    path('<int:pk>/delete/', user_wish_delete, name='user-wish-delete'),
]