from django import forms
from .connector import User, Course

import re


class UserForm(forms.Form):
    name = forms.CharField(max_length=30)
    email = forms.EmailField()
    phone = forms.CharField(max_length=12, min_length=12, required=False)
    mobile_phone = forms.CharField(max_length=12, min_length=12, required=False)
    status = forms.ChoiceField(choices=[('0', 'Inactive'), ('1', 'Active')], required=False)

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.get('email', email)
        if user:
            raise forms.ValidationError(
                'User with such email already exists',
                code='email_exist',
            )
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            if re.fullmatch(r'\+\d{11}', phone):
                return phone
            else:
                raise forms.ValidationError(
                    'Please write your phone in such format: '
                    '+ 0 000 000 00 00.(withou spaces)',
                    code='phone_mask_mismatch',
                )

    def clean_mobile_phone(self):
        mobile_phone = self.cleaned_data.get('mobile_phone')
        if mobile_phone:
            if re.fullmatch(r'\+\d{11}', mobile_phone):
                return mobile_phone
            else:
                raise forms.ValidationError(
                    'Please write your mobile phone in such format: '
                    '+ 0 000 000 00 00.(without spaces)',
                    code='mobile_phone_mask_mismatch',
                )


class UserUpdateForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    email = forms.EmailField()
    phone = forms.CharField(max_length=12, min_length=12, required=False)
    mobile_phone = forms.CharField(max_length=12, min_length=12, required=False)
    status = forms.ChoiceField(choices=[('0', 'Inactive'), ('1', 'Active')], required=False)
    courses = forms.ChoiceField(required=False)
    courses_list = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, required=False)

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_id = user['id']
        free_courses = Course.free_courses(user['id'])
        all_courses = Course.all()
        self.fields['courses'] = forms.ChoiceField(
            choices=[(course['code'], course['name']) for course in free_courses],
            required=False
            )
        self.fields['courses_list'] = forms.MultipleChoiceField(
            widget=forms.CheckboxSelectMultiple,
            choices=[(course['code'], course['name']) for course in all_courses],
            required=False
            )

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.get('email', email)
        if user and user['id'] != self.user_id:
            raise forms.ValidationError(
                'User with such email already exists',
                code='email_exist',
            )
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            if re.fullmatch(r'\+\d{11}', phone):
                return phone
            else:
                raise forms.ValidationError(
                    'Please write your phone in such format: '
                    '+ 0 000 000 00 00.(withou spaces)',
                    code='phone_mask_mismatch',
                )

    def clean_mobile_phone(self):
        mobile_phone = self.cleaned_data.get('mobile_phone')
        if mobile_phone:
            if re.fullmatch(r'\+\d{11}', mobile_phone):
                return mobile_phone
            else:
                raise forms.ValidationError(
                    'Please write your mobile phone in such format: '
                    '+ 0 000 000 00 00.(without spaces)',
                    code='mobile_phone_mask_mismatch',
                )
