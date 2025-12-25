from django.views.generic import View
from django.views.generic.base import ContextMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http.request import HttpRequest
from django.http.response import HttpResponseNotAllowed

from django.core.cache import cache

from app.models import Profile, Tag


class PaginatorMixin(ContextMixin):
    objects_per_page = 10
    page_number_parameter = 'page'

    should_cache = False
    cache_key = "paginator"
    page_cache_limit = 3


    def dispatch(self, request: 'HttpRequest', *args, **kwargs):
        if request.method != 'GET':
            return HttpResponseNotAllowed(['GET'])
        
        return super().dispatch(request, *args, **kwargs)


    def get_page_object(self: 'View', object_list):
        paginator = Paginator(object_list, self.objects_per_page)
        page_number = self._get_page_number()

        try:
            page_object = paginator.page(page_number)
        except PageNotAnInteger:
            page_object = paginator.page(1)
        except EmptyPage:
            page_object = paginator.page(paginator.num_pages)

        return page_object
    
    def _get_page_number(self):
        return self.request.GET.get(self.page_number_parameter, 1)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["page_obj"] = self.get_page_object(self.get_object_list())

        return context
    

class StatisticsMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # context["best_members"] = Profile.objects.get_best_members()
        # context["best_tags"] = Tag.objects.get_best_tags()

        return context