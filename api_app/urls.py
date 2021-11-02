from django.urls import path
from .views import *


urlpatterns = [
    # admin url
    path('admin/advisor/', create_advisor),

    # user url
    path('user/register/', register_user),
    path('user/login/', login_view),
    path('user/logout/', logout_view),

    path('user/<user_id>/advisor/', advisor_list),
    path('user/<user_id>/advisor/booking/', booking_list),
    path('user/<user_id>/advisor/<advisor_id>/', book_call),
    
    path('user/all/', user_list),
    path('user/', current_user),
]
