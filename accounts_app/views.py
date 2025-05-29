from django.contrib.auth import login
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

    login_form = LoginForm()
    return render(request, 'accounts_app/login.html', {'login_form': login_form})