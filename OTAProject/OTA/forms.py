# OTAProject/OTAApp/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, TravelAgency, Guide


class TravelAgencyRegistrationForm(UserCreationForm):
    agency_name = forms.CharField(max_length=100, required=True, label="旅行社名称")
    license_number = forms.CharField(max_length=50, required=True, label="营业执照号")
    address = forms.CharField(widget=forms.Textarea, required=False, label="地址")
    phone = forms.CharField(max_length=15, required=True, label="联系电话")

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email', 'phone']
        labels = {
            'username': '用户名',
            'email': '邮箱',
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'travel_agency'
        if commit:
            user.save()
            TravelAgency.objects.create(
                user=user,
                agency_name=self.cleaned_data['agency_name'],
                license_number=self.cleaned_data['license_number'],
                address=self.cleaned_data.get('address', '')
            )
        return user


class GuideRegistrationForm(UserCreationForm):
    guide_id = forms.CharField(max_length=50, required=True, label="导游证号")
    travel_agency = forms.ModelChoiceField(
        queryset=TravelAgency.objects.all(),
        empty_label="请选择旅行社",
        required=True,
        label="所属旅行社"
    )
    phone = forms.CharField(max_length=15, required=True, label="联系电话")

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email', 'phone']
        labels = {
            'username': '用户名',
            'email': '邮箱',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 动态获取所有已注册的旅行社
        self.fields['travel_agency'].queryset = TravelAgency.objects.all()

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'guide'
        if commit:
            user.save()
            Guide.objects.create(
                user=user,
                guide_id=self.cleaned_data['guide_id'],
                travel_agency=self.cleaned_data['travel_agency']
            )
        return user


class TouristRegistrationForm(UserCreationForm):
    phone = forms.CharField(max_length=15, required=True, label="联系电话")

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email', 'phone']
        labels = {
            'username': '用户名',
            'email': '邮箱',
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'tourist'
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, label="用户名")
    password = forms.CharField(widget=forms.PasswordInput, label="密码")