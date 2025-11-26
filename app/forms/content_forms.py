import logging

from django import forms
from django.core.exceptions import ValidationError
from app.models import Question, Tag, Answer


logger = logging.getLogger(__name__)


class AskQuestionForm(forms.ModelForm):
    tags = forms.CharField(
        label="Tags",
        help_text="Comma separated values",
    )

    class Meta:
        model = Question
        fields = ("title", "text", "tags")

    def clean_tags(self):
        tags_str = self.cleaned_data["tags"]

        tags_list = [
            tag.strip()
            for tag in tags_str.strip().split(",") if tag.strip()
        ]

        if not tags_list:
            raise ValidationError("Tags cannot be empty")
        
        return tags_list
    
    def save(self, commit=True):
        question = super().save(commit=False)

        if commit:
            question.save()
            tags_names = self.cleaned_data["tags"]

            for name in tags_names:
                tag, _ = Tag.objects.get_or_create(name=name)
                question.tags.add(tag)

        return question


class AddAnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ("text",)