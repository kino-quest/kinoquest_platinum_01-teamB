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
    path('search/get-ski-resorts/', views.get_ski_resorts, name="get_ski_resorts_search"),
    path('instructor/schedule/get-ski-resorts/', views.get_ski_resorts, name="get_ski_resorts_instructor"),
    path('instructor/events/', views.instructor_events, name='instructor_events'),
    path('lesson/confirm/<int:lesson_id>/', views.lesson_confirm_view, name='lesson_confirm'),
    # 予約確定処理（POST専用）
    path('lesson/reserve/<int:lesson_id>/', views.lesson_reserve_view, name='lesson_reserve'),
    # 履歴
    path('lesson/history/', views.lesson_history_view, name='lesson_history'),
    path('lesson_cancel/<int:preference_id>/', views.lesson_cancel_view, name='lesson_cancel'),
    path('student-events/', views.student_events, name='student_events'),
    path('instructor/history/', views.instructor_history_view, name='instructor_history'),
    path('cancel_preference/<int:pref_id>/', views.cancel_preference, name='cancel_preference'),
    path('cancel_lesson/<int:lesson_id>/', views.cancel_lesson, name='cancel_lesson'),
]
