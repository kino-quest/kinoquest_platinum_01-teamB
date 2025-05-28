from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

# 新規登録
class SignupForm(UserCreationForm):
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
            'password1',
            'password2'
        ]

        widgets = {
            'gender': forms.RadioSelect,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 「：」をなしにする
        self.label_suffix = ''
        
        field_settings = {
            'username': '名前',
            'gender': '性別',
            'date_of_birth': '生年月日',
            'postal_code': '郵便番号',
            'address': '住所',
            'phone_number': '電話番号',
            'email': 'メール',
            'password1': 'パスワード',
            'password2': 'パスワード(確認用)',
        }

        for field_name, placeholder in field_settings.items():
            field = self.fields[field_name]
            field.widget.attrs['class'] = 'block text-sm font-medium text-gray-700 mb-1'
            field.widget.attrs['placeholder'] = placeholder

        self.fields['username'].label = '名前'
        self.fields['gender'].label = '性別'

        # 「----」のデフォルト表示を非表示にする
        self.fields['gender'].choices = [('M', '男性'), ('F', '女性')]
        self.fields['date_of_birth'].label = '生年月日'
        self.fields['postal_code'].label = '郵便番号'
        self.fields['address'].label = '住所'
        self.fields['phone_number'].label = '電話番号'
        self.fields['email'].label = 'メール'
        self.fields['password1'].label = 'パスワード'
        self.fields['password2'].label = 'パスワード(確認用)'

