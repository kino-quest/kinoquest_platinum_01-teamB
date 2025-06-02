from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .forms import InstructorSignupForm, CustomPasswordChangeForm, LoginForm, StudentSignupForm, UserUpdateForm
from .models import CustomUser

# 新規登録処理 受講者用
def student_signup_view(request):
    # 新規登録フォームが送られてきた時
    if request.method == 'POST':
        signup_form = StudentSignupForm(request.POST)

        if signup_form.is_valid():
            # ユーザーを保存して、'user' 変数に代入する
            user = signup_form.save(commit=False) # 保存は確定させない
            # ロールを設定する
            user.role = CustomUser.Role.STUDENT
            # 変更を DB へ保存する
            user.save()
            # ログイン処理
            login(request, user)
            return redirect('dashboard')
    else:
        signup_form = StudentSignupForm()
    return render(request, 'accounts_app/student_signup.html', {'signup_form': signup_form})

# 新規登録処理 インストラクター用
def instructor_signup_view(request):
    # 新規登録フォームが送られてきた時
    if request.method == 'POST':
        signup_form = InstructorSignupForm(request.POST)

        if signup_form.is_valid():
            # ユーザーを保存して、'user' 変数に代入する
            user = signup_form.save(commit=False) # 保存は確定させない
            # ロールを設定する
            user.role = CustomUser.Role.INSTRUCTOR
            # 変更を DB へ保存する
            user.save()
            # ログイン処理
            login(request, user)
            return redirect('dashboard')
    else:
        signup_form = InstructorSignupForm()
    return render(request, 'accounts_app/instructor_signup.html', {'signup_form': signup_form})

# ログイン処理 - 受講者側
def student_login_view(request):
    # ログインフォームが送られてきた時
    if request.method == 'POST':
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            # 認証処理
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                print("ログイン失敗")
                login_form.add_error(None, 'メールアドレスまたはパスワードが違います')
    else:
        login_form = LoginForm()
    return render(request, 'accounts_app/student_login.html', {'login_form': login_form})

# ログイン処理 - インストラクター側
def instructor_login_view(request):
    # ログインフォームが送られてきた時
    if request.method == 'POST':
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            # 認証処理
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                print("ログイン失敗")
                login_form.add_error(None, 'メールアドレスまたはパスワードが違います')
    else:
        login_form = LoginForm()
    return render(request, 'accounts_app/instructor_login.html', {'login_form': login_form})

# ログアウト処理
@login_required
def logout_view(request):
    # ログアウト前にユーザー情報を保存
    user = request.user
    is_student = user.is_student
    is_instructor = user.is_instructor

    # ログアウト処理
    logout(request)

    # ユーザーの条件でリダイレクトさせる
    if is_student:
        return redirect('student_login')
    elif is_instructor:
        return redirect('instructor_login')

# ユーザー情報設定 / 更新 - 受講者用
@login_required
def student_setting(request):
    # 「更新ボタン」が押された時
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        password_form = CustomPasswordChangeForm(user=request.user, data=request.POST)

        user_valid = user_form.is_valid()
        password_valid = password_form.is_valid()

        if user_valid:
            user_form.save()
        
        if password_valid:
            user = password_form.save()
            #パスワード変更後にログアウトされるのを防ぐ
            update_session_auth_hash(request, user)
        if not user_valid and not password_valid:
            messages.error(request, '入力内容に誤りがあります。確認してください')

        # どちらも成功していたら「student_settings」へリダイレクト
        if user_valid and password_valid:
            messages.success(request, 'ユーザー情報を更新しました')
            return redirect('student_setting')
        
    user_form = UserUpdateForm(instance=request.user)
    password_form = CustomPasswordChangeForm(user=request.user)
    params = {
        'user_form': user_form,
        'password_form': password_form,
    }
    return render(request, 'accounts_app/student_setting.html', params)

# ユーザー情報設定 / 更新 - インストラクター用
@login_required
def instructor_setting(request):
    # 「更新ボタン」が押された時
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        password_form = CustomPasswordChangeForm(user=request.user, data=request.POST)

        user_valid = user_form.is_valid()
        password_valid = password_form.is_valid()

        if user_valid:
            user_form.save()
        
        if password_valid:
            user = password_form.save()
            #パスワード変更後にログアウトされるのを防ぐ
            update_session_auth_hash(request, user)
        if not user_valid and not password_valid:
            messages.error(request, '入力内容に誤りがあります。確認してください')

        # どちらも成功していたら「instructor_settings」へリダイレクト
        if user_valid and password_valid:
            messages.success(request, 'ユーザー情報を更新しました')
            return redirect('instructor_setting')
        
    user_form = UserUpdateForm(instance=request.user)
    password_form = CustomPasswordChangeForm(user=request.user)
    params = {
        'user_form': user_form,
        'password_form': password_form,
    }
    return render(request, 'accounts_app/instructor_setting.html', params)