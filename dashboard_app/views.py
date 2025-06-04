from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from .forms import LessonDetailForm
from .models import SkiResort
# ダッシュボード - 受講者
@login_required
def student_dashboard_view(request):
    return render(request, 'dashboard_app/student_dashboard.html')

# ダッシュボード - インストラクター
@login_required
def instructor_dashboard_view(request):
    return render(request, 'dashboard_app/instructor_dashboard.html')

@login_required
def instructor_schedule(request):
    if not request.user.is_instructor:
        return render(request, 'error.html', {'message': 'インストラクターのみアクセス可能です。'})

    if request.method == 'POST':
        form = LessonDetailForm(request.POST)
        if form.is_valid():
            lesson_detail = form.save(commit=False)
            lesson_detail.instructor = request.user
            lesson_detail.save()
            return redirect('instructor_schedule')  # 登録後リダイレクト
        else:
            print("フォームエラー", form.errors)
    else:
        form = LessonDetailForm()

    return render(request, 'dashboard_app/instructor_schedule.html', {
        'form': form
    })

# Ajaxエンドポイント
def get_ski_resorts(request):
    print("Ajax!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    prefecture_id = request.GET.get('prefecture_id')
    ski_resorts = SkiResort.objects.filter(prefecture_id=prefecture_id).values('id', 'resort_name')
    return JsonResponse(list(ski_resorts), safe=False)
