from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from .models import InstructorProfile

User = get_user_model()

# 共通のCSSクラス
COMMON_INPUT_CLASS = '''
    mt-1
    block
    w-full
    px-3
    py-2
    border
    border-gray-300
    rounded-md shadow-sm
    focus:outline-none
    focus:ring-indigo-500
    focus:border-indigo-500
    sm:text-sm
'''

# 新規登録処理 受講者側
class StudentSignupForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = [
            'username',
            'gender',
            'date_of_birth',
            'postal_code',
            'address',
            'phone_number',
            'email',
        ]

        widgets = {
            'gender': forms.RadioSelect,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 「：」をなしにする
        self.label_suffix = ''
        
        field_settings = {
            'username': '名前を入力してください',
            'gender': '性別',
            'date_of_birth': '例 : 1990-01-01',
            'postal_code': '例 : 123-4567',
            'address': '住所',
            'phone_number': '例 : 090-1234-5678',
            'email': '例 : your_email@example.com',
            'password': 'パスワードを入力してください',
        }

        # UserCreationForm が生成する password1 と password2 のフィールドにも適用する
        password_fields = {
            'password1': 'パスワードを入力してください',
            'password2': 'パスワード(確認用)を入力してください',
        }
        
        # 各フィールドに共通のCSSクラスとプレースホルダーを設定する
        for field_name, placeholder in field_settings.items():
            # password フィールドは UserCreationForm が生成するためチェックする
            if field_name in self.fields:
                field = self.fields[field_name]
                field.widget.attrs['class'] = COMMON_INPUT_CLASS
                field.widget.attrs['placeholder'] = placeholder

        # password1 と password2 にも適用する
        for field_name, placeholder in password_fields.items():
            if field_name in self.fields:
                field = self.fields[field_name]
                field.widget.attrs['class'] = COMMON_INPUT_CLASS
                field.widget.attrs['placeholder'] = placeholder
        
        self.fields['username'].label = '名前'
        self.fields['gender'].label = '性別'
        # ラジオボタンのクラスを個別に設定する
        self.fields['gender'].widget.attrs['class'] = 'flex items-center space-x-4'

        # 「----」のデフォルト表示を非表示にする
        self.fields['gender'].choices = [('M', '男性'), ('F', '女性')]

        self.fields['date_of_birth'].label = '生年月日'
        self.fields['postal_code'].label = '郵便番号'
        self.fields['address'].label = '住所'
        self.fields['phone_number'].label = '電話番号'
        self.fields['email'].label = 'メール'
        self.fields['password1'].label = 'パスワード'
        self.fields['password2'].label = 'パスワード(確認用)'

# 新規登録処理 インストラクター側
class InstructorSignupForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = [
            'username',
            'gender',
            'date_of_birth',
            'phone_number',
            'email',
        ]

        widgets = {
            'gender': forms.RadioSelect,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 「：」をなしにする
        self.label_suffix = ''
        
        field_settings = {
            'username': '名前を入力してください',
            'gender': '性別',
            'date_of_birth': '例 : 1990-01-01',
            'phone_number': '例 : 090-1234-5678',
            'email': '例 : your_email@example.com',
            'password': 'パスワードを入力してください',
        }

        # UserCreationForm が生成する password1 と password2 のフィールドにも適用する
        password_fields = {
            'password1': 'パスワードを入力してください',
            'password2': 'パスワード(確認用)を入力してください',
        }
        
        # 各フィールドに共通のCSSクラスとプレースホルダーを設定する
        for field_name, placeholder in field_settings.items():
            # password フィールドは UserCreationForm が生成するためチェックする
            if field_name in self.fields:
                field = self.fields[field_name]
                field.widget.attrs['class'] = COMMON_INPUT_CLASS
                field.widget.attrs['placeholder'] = placeholder

        # password1 と password2 にも適用する
        for field_name, placeholder in password_fields.items():
            if field_name in self.fields:
                field = self.fields[field_name]
                field.widget.attrs['class'] = COMMON_INPUT_CLASS
                field.widget.attrs['placeholder'] = placeholder
        
        self.fields['username'].label = '名前'
        self.fields['gender'].label = '性別'
        # ラジオボタンのクラスを個別に設定する
        self.fields['gender'].widget.attrs['class'] = 'flex items-center space-x-4'

        # 「----」のデフォルト表示を非表示にする
        self.fields['gender'].choices = [('M', '男性'), ('F', '女性')]

        self.fields['date_of_birth'].label = '生年月日'
        self.fields['phone_number'].label = '電話番号'
        self.fields['email'].label = 'メール'
        self.fields['password1'].label = 'パスワード'
        self.fields['password2'].label = 'パスワード(確認用)'

# ログイン処理
class LoginForm(forms.Form):
    username = forms.CharField(
        label='名前',
        widget=forms.TextInput(attrs={
            'class': COMMON_INPUT_CLASS,
            'placeholder': '名前を入力してください'
        })
    )
    password = forms.CharField(
        label='パスワード',
        widget=forms.PasswordInput(attrs={
            'class': COMMON_INPUT_CLASS,
            'placeholder': 'パスワードを入力してください'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''
        self.user = None

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:
            self.user = authenticate(username=username, password=password)

            if self.user is None:
                raise forms.ValidationError("名前またはパスワードが正しくありません。")

        return cleaned_data

    def get_user(self):
        return self.user

# 編集処理
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = [
            'profile_image',
            'username',
            'gender',
            'date_of_birth',
            'postal_code',
            'address',
            'phone_number',
            'email',
        ]

        widgets = {
            'gender': forms.RadioSelect,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 「：」をなしにする
        self.label_suffix = ''

        field_settings = {
            'profile_image': '画像',
            'username': '名前を入力してください',
            'gender': '性別',
            'date_of_birth': '例 : 1990-01-01',
            'postal_code': '例 : 123-4567',
            'address': '住所',
            'phone_number': '例 : 090-1234-5678',
            'email': '例 : your_email@example.com',
            'password': 'パスワードを入力してください',
        }

        for field_name, placeholder in field_settings.items():
            # password フィールドは UserCreationForm が生成するためチェックする
            if field_name in self.fields:
                field = self.fields[field_name]
                field.widget.attrs['class'] = COMMON_INPUT_CLASS
                field.widget.attrs['placeholder'] = placeholder
        
        self.fields['profile_image'].label = '画像'
        self.fields['username'].label = '名前'
        self.fields['gender'].label = '性別'
        self.fields['gender'].widget.attrs['class'] = 'flex items-center space-x-4'
        self.fields['gender'].choices = [('M', '男性'), ('F', '女性')]
        self.fields['date_of_birth'].label = '生年月日'
        self.fields['postal_code'].label = '郵便番号'
        self.fields['address'].label = '住所'
        self.fields['phone_number'].label = '電話番号'
        self.fields['email'].label = 'メール'

# 編集 PasswordChangeFormをカスタマイズ(オーバーライド)
class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''

        field_settings = {
            'old_password': '現在のパスワードを入力してください',
            'new_password1': '新しいパスワードを入力してください',
            'new_password2': '確認用の新しいパスワードを入力してください',
        }

        for field_name, placeholder in field_settings.items():
            field = self.fields[field_name]
            field.widget.attrs['class'] = COMMON_INPUT_CLASS
            field.widget.attrs['placeholder'] = placeholder

        self.fields['old_password'].label = '現在のパスワード'
        self.fields['new_password2'].label = '新しいパスワード確認'

# 編集
class InstructorProfileForm(forms.ModelForm):
    class Meta:
        model = InstructorProfile
        fields = [
            'self_introduction',
            'skill_ski',
            'skill_snowboard',
            'spoken_japanese',
            'spoken_english',
            'spoken_chinese',
            'spoken_other',
        ]
        widgets = {
            'self_introduction': forms.Textarea(attrs={'rows': 4})
        }
        labels = {
            'self_introduction': 'インストラクター紹介',
            'skill_ski': 'レッスン可能な種目：スキー',
            'skill_snowboard': 'レッスン可能な種目：スノーボード',
            'spoken_japanese': '話せる言語：日本語',
            'spoken_english': '話せる言語：英語',
            'spoken_chinese': '話せる言語：中国語',
            'spoken_other': '話せる言語：その他',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''

        for field_name, field in self.fields.items():
            # テキスト入力とテキストエリアに共通クラスを適用
            if isinstance(field.widget, (forms.TextInput, forms.Textarea)):
                field.widget.attrs['class'] = COMMON_INPUT_CLASS
            # チェックボックスには別のクラスを適用
            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-checkbox h-5 w-5 text-sky-600'
            # ラベルとウィジェットのクラスを分けて設定したい場合 (例: ラジオボタンなど)
            # else:
            #    field.widget.attrs['class'] = 'some-other-class'