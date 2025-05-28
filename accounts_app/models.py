from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('instructor', 'Instructor'),
    ]
    # 以下２つは使わない、username を使用する
    first_name = None
    last_name = None
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    gender = models.CharField(max_length=1, choices=[('M', '男性'), ('F', '女性')], blank=False)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=20)
    postal_code = models.CharField(max_length=10, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    # emailを一意にしてログインIDとして使いたい場合
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # usernameも残しておく

    def __str__(self):
        return f"{self.role.title()} - {self.full_name}"


class InstructorProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='instructor_profile')

    self_introduction = models.TextField(blank=True)

    # スキル
    skill_ski = models.BooleanField(default=False)
    skill_snowboard = models.BooleanField(default=False)

    # 言語スキル
    spoken_japanese = models.BooleanField(default=False)
    spoken_english = models.BooleanField(default=False)
    spoken_chinese = models.BooleanField(default=False)
    spoken_other = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"InstructorProfile for {self.user.full_name}"
