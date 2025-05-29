from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from .forms import LoginForm, SignupForm

# 新規登録処理
def signup_view(request):
    print("signup")

    # 新規登録フォームが送られてきた時
    if request.method == 'POST':
        print("post")
        signup_form = SignupForm(request.POST)
        # print(signup_form)
        if signup_form.is_valid():
            print("is_valid")
            user = signup_form.save()
            login(request, user)
            return redirect('signup')
    else:
        signup_form = SignupForm()
    return render(request, 'accounts_app/signup.html', {'signup_form': signup_form})

# ログイン処理
def login_view(request):
    print("login")

    if request.method == 'POST':
        print("------------POSTで受け取ったよ-------------------")
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            print("------------login_valid()-------------------")
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']

            # 認証処理
            user = authenticate(request, username=username, password=password)
            if user is not None:
                print("------------ログイン成功-------------------")
                login(request, user)
                return redirect('login')
            else:
                print("ログイン失敗")
                login_form.add_error(None, 'メールアドレスまたはパスワードが違います')
    else:
        login_form = LoginForm()
    return render(request, 'accounts_app/login.html', {'login_form': login_form})