from django import forms
from recipes.models.comment import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Write your comment...',
                'class': 'form-control'
            }),
        }
        
        labels = {
            'text': '',
        }


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'Write your reply...',
                'class': 'form-control'
            }),
        }
        
        labels = {
            'text': '',
        }
