from django import forms

from captcha import fields

from .models import Comment


class CommentForm(forms.ModelForm):
    note = forms.IntegerField(widget=forms.HiddenInput)
    parent = forms.IntegerField(widget=forms.HiddenInput, required=False)
    answer_to = forms.IntegerField(widget=forms.HiddenInput, required=False)

    class Meta:
        model = Comment
        fields = ('user', 'email', 'body', 'notification')


class SearchForm(forms.Form):
    query = forms.CharField(max_length=50)


class ContactForm(forms.Form):
    username = forms.CharField(max_length=50, required=False)
    sender = forms.EmailField()
    subject = forms.CharField(max_length=50)
    message = forms.CharField(widget=forms.Textarea)
    captcha = fields.CaptchaField(widget=fields.CaptchaTextInput)
