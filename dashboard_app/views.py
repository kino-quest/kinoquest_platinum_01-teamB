from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# ダッシュボード - 受講者
@login_required
def student_dashboard_view(request):
    return render(request, 'dashboard_app/student_dashboard.html')

# ダッシュボード - インストラクター
@login_required
def instructor_dashboard_view(request):
    return render(request, 'dashboard_app/instructor_dashboard.html')
