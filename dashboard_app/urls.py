from django.urls import path
from . import views

urlpatterns = [
    # ダッシュボード - 受講者 - インストラクター
    path('dashboard/student', views.student_dashboard_view, name="student_dashboard"),
    path('dashboard/instructor', views.instructor_dashboard_view, name="instructor_dashboard"),
    # 日程調整
    path('instructor/schedule/', views.instructor_schedule, name="instructor_schedule"),
    # Ajaxエンドポイント
    path('instructor/schedule/get-ski-resorts/', views.get_ski_resorts, name="get_ski_resorts"),
]
