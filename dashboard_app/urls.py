from django.urls import path
from . import views

urlpatterns = [
    # ダッシュボード - 受講者 - インストラクター
    path('student/', views.student_dashboard_view, name="student_dashboard"),
    path('instructor/', views.instructor_dashboard_view, name="instructor_dashboard"),
    # 日程調整
    path('instructor/schedule/', views.instructor_schedule, name="instructor_schedule"),
    path('search/', views.lesson_search, name='lesson_search'),
    # Ajaxエンドポイント
    path('instructor/schedule/get-ski-resorts/', views.get_ski_resorts, name="get_ski_resorts_instructor"),
    path('search/get-ski-resorts/', views.get_ski_resorts, name="get_ski_resorts_search"),
    path('instructor/events/', views.instructor_events, name='instructor_events'),
]
