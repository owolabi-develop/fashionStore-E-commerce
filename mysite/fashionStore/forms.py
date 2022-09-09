
from django import forms
from . models import User,Profile,AddressBook
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import PasswordResetForm,SetPasswordForm,PasswordChangeForm


class UserCreationForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field_name in self.fields:
            field = self.fields.get(field_name)
            self.fields[field_name].widget.attrs.update({'placeholder':field.label})
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('first_name','last_name','email','phoneNumber')
        widgets ={
            'subscribe':forms.CheckboxInput,
        }

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserPasswordResetForm(PasswordResetForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field_name in self.fields:
            field = self.fields.get(field_name)
            self.fields[field_name].widget.attrs.update({'placeholder':field.label})
    class Meta:
        model = User
        field = ('email',)

class UserSetPassword(SetPasswordForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field_name in self.fields:
            field = self.fields.get(field_name)
            self.fields[field_name].widget.attrs.update({'placeholder':field.label})

class ProfileForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field_name in self.fields:
            field = self.fields.get(field_name)
            self.fields[field_name].widget.attrs.update({'placeholder':field.label})
    class Meta:
        model = Profile
        fields = ("Profile_pic",)

class UserEditForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field_name in self.fields:
            field = self.fields.get(field_name)
            self.fields[field_name].widget.attrs.update({'placeholder':field.label})
    class Meta:
        model = User
        fields = ['first_name','last_name','email','username','Gender']

class UserChangePassword(PasswordChangeForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field_name in self.fields:
            field = self.fields.get(field_name)
            self.fields[field_name].widget.attrs.update({'placeholder':field.label})
    class Meta:
        model = User
        fields = "__all__"

class AddressBookForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field_name in self.fields:
            field = self.fields.get(field_name)
            self.fields[field_name].widget.attrs.update({'placeholder':field.label})
    
    class Meta:
        model = AddressBook
        fields = ("first_name","last_name","phoneNumber","Region","City","Delivery_address","zip_code","Additional_information","default_address",)
        widgets ={
            'default_address':forms.CheckboxInput,
        }







