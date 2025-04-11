from django.contrib import admin
from django.contrib.admin import ModelAdmin

from account.models import UserModel
from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm


@admin.action(description="Make user is staff")
def set_is_staff(self, request, queryset):
    queryset.update(is_staff=True)


class CustomUserChangeForm(UserChangeForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False)

    class Meta:
        model = UserModel
        fields = '__all__'

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = UserModel
        fields = ('email',)


class UserAdmin(admin.ModelAdmin):
    list_display = ['full_name', "is_staff"]
    search_fields = ['full_name']
    actions = [set_is_staff]
    model = UserModel
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm


admin.site.register(UserModel, UserAdmin)

