from django.contrib import admin

from app.models import *


admin.site.register(Profile)
admin.site.register(Question)
admin.site.register(Tag)
admin.site.register(Answer)
admin.site.register(QuestionsLikes)
admin.site.register(AnswersLikes)
