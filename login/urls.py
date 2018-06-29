from django.contrib import admin
from django.urls import path,include
from . import views
#urlpatterns = [
#    path('admin/', admin.site.urls),
#    path('calc/add/<int:x>/<int:y>',views.new_page),
#]

urlpatterns = [
       path('ipl/',views.login_page),
       path('login/userlogin',views.user_login),
       path('submitbet1/',views.submit_bet1),
       path('submitbet2/',views.submit_bet2),
       path('bettingHistory/',views.bettingHistory),
       path('updateResult1/',views.updateResult1),
       path('updateResult2/',views.updateResult1),
       path('change/',views.changePassword),
       path('changePasswordSubmit/',views.changePasswordSubmit),
       path('dashboard/',views.dashboard),
]