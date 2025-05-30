from django.urls import path
from . import views

urlpatterns = [
    # 新規作成
    path('signup/student/', views.student_signup_view, name="student_signup"),
    path('signup/instructor/', views.instructor_signup_view, name="instructor_signup"),
    # ログイン・ログアウト
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    # ユーザー設定
    path('user_setting/', views.user_setting, name="user_setting"),
]
