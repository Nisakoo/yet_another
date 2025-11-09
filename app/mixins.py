from django.views.generic import View
from django.views.generic.base import ContextMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http.request import HttpRequest
from django.http.response import HttpResponseNotAllowed

from .models import (
    Profile,
    Tag
)


class PaginatorMixin:
    objects_per_page = 10
    page_number_parameter = 'page'


    def dispatch(self, request: 'HttpRequest', *args, **kwargs):
        if request.method != 'GET':
            return HttpResponseNotAllowed(['GET'])
        
        return super().dispatch(request, *args, **kwargs)


    def get_page_object(self: 'View', object_list):
        paginator = Paginator(object_list, self.objects_per_page)
        page_number = self.request.GET.get(self.page_number_parameter, 1)

        try:
            page_object = paginator.page(page_number)
        except PageNotAnInteger:
            page_object = paginator.page(1)
        except EmptyPage:
            page_object = paginator.page(paginator.num_pages)

        return page_object
    

class StatisticsMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        
        context["best_members"] = Profile.objects.get_best_members()
        context["best_tags"] = Tag.objects.get_best_tags()

        return context