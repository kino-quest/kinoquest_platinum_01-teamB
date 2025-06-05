import logging
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .forms import LessonDetailForm, LessonSearchForm
from .models import ActivityChoices, LessonDetail, SkiResort

logger = logging.getLogger(__name__)

# ダッシュボード - 受講者
@login_required
def student_dashboard_view(request):
    return render(request, 'dashboard_app/student_dashboard.html')

# ダッシュボード - インストラクター
@login_required
def instructor_dashboard_view(request):
    today = timezone.localtime().date()
    return render(request, 'dashboard_app/instructor_dashboard.html', {'today': today})

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

    return render(request, 'dashboard_app/instructor_schedule.html', {'form': form})

# Ajaxエンドポイント
def get_ski_resorts(request):
    print("get!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    prefecture_id = request.GET.get('prefecture_id')
    ski_resorts = SkiResort.objects.filter(prefecture_id=prefecture_id).values('id', 'resort_name')
    return JsonResponse(list(ski_resorts), safe=False)

# レッスンデータをJSONで返すビュー
@login_required
def instructor_events(request):
    lessons = LessonDetail.objects.filter(instructor=request.user)
    events = []

    for lesson in lessons:
        print(f"DEBUG lesson time_slot: {lesson.time_slot}, activity_name: {lesson.activity_type.activity_name}")
        # アクティビティタイプと時間帯から価格を取得
        if lesson.activity_type.activity_name == ActivityChoices.SKI:
            if lesson.time_slot == "morning":
                price = lesson.ski_morning_price
            elif lesson.time_slot == "afternoon":
                price = lesson.ski_afternoon_price
            elif lesson.time_slot == "full_day":
                price = lesson.ski_full_day_price
        elif lesson.activity_type.activity_name == ActivityChoices.SNOWBOARD:
            if lesson.time_slot == "morning":
                price = lesson.snowboard_morning_price
            elif lesson.time_slot == "afternoon":
                price = lesson.snowboard_afternoon_price
            elif lesson.time_slot == "full_day":
                price = lesson.snowboard_full_day_price
        else:
            price = 0  # 万が一未設定なら
        # Noneを0に置き換え
        price = price or 0

        # カレンダーに表示させるデータを整形
        events.append({
            "title": f"¥{price}",
            "start": f"{lesson.lesson_date}T09:00:00",  # 固定 or time_slot で調整してもOK
        })


    return JsonResponse(events, safe=False)

@login_required
def lesson_search(request):
    form = LessonSearchForm(request.GET or None)
    lessons = LessonDetail.objects.none()  # デフォルトは空

    if form.is_valid():
        # フォームの入力から検索条件を取得
        lesson_date = form.cleaned_data['lesson_date']
        ski_resort = form.cleaned_data['ski_resort']
        level = form.cleaned_data['level']
        lesson_type = form.cleaned_data['lesson_type']
        time_slot = form.cleaned_data['time_slot']

        # 厳密一致でフィルター
        lessons = LessonDetail.objects.select_related("activity_type").filter(
            lesson_date=lesson_date,
            ski_resort=ski_resort,
            level=level,
            lesson_type=lesson_type,
            time_slot=time_slot,
            #is_reserved=False,  # 予約済みじゃないやつ
        )
        for lesson in lessons:
            # activity_type_display をテンプレートで使えるよう追加
            lesson.activity_type_display = lesson.activity_type.get_activity_name_display()
            print(lesson.ski_morning_price)

    return render(request, 'dashboard_app/lesson_search.html', {
        'form': form,
        'lessons': lessons
    })

@login_required
def lesson_confirm_view(request, lesson_id):
    lesson = get_object_or_404(LessonDetail, id=lesson_id)
    return render(request, 'dashboard_app/lesson_confirm.html', {'lesson': lesson})