from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from book.models import Users, Bookshelf


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Users
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "middle_name",
            "avatar",
            "password",
            "confirm_password"
        )

    def clean_username(self):
        username = self.cleaned_data["username"]
        if Users.objects.filter(username=username).exists():
            msg = 'this username already taken please choose another one'
            self.add_error('username', msg)
        return username

    def clean(self):
        if self.cleaned_data["password"] != self.cleaned_data["confirm_password"]:
            msg = "password and confirm_password must be match"
            self.add_error("confirm_password", msg)

        return self.cleaned_data

    def save(self):
        user = Users.objects.create(
            username=self.cleaned_data["username"],
            email=self.cleaned_data["email"],
            middle_name=self.cleaned_data["middle_name"],
            first_name=self.cleaned_data["first_name"],
            last_name=self.cleaned_data["last_name"],
            avatar=self.cleaned_data["avatar"],
        )
        user.set_password(self.cleaned_data["password"])
        user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())




class BookshelfForm(forms.ModelForm):
    class Meta:
        model = Bookshelf
        fields = "__all__"


class UserUpdateForm(ModelForm):
    class Meta:
        model = Users
        fields = ("first_name", "last_name", "middle_name", "email", "avatar", "username",)

class UserDeleteForm(forms.Form):
    SELECTION_CHOICES = [('Yes', 'Yes'), ('No', 'No')]
    delete = forms.ChoiceField(choices=SELECTION_CHOICES, widget=forms.RadioSelect)
