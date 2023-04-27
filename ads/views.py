import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from rest_framework.viewsets import ModelViewSet

from ads.models import Category, Ad, User
from ads.serializers import AdSerializer
from lesson_27_homework import settings


def main_view(request):
    return JsonResponse({"status": "ok"}, status=200)


# _________________________________________________________________________
# model Category - ListView, DetailView, CreateView, UpdateView, DeleteView
# _________________________________________________________________________
@method_decorator(csrf_exempt, name='dispatch')
class CatListView(ListView):
    model = Category

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        response = []
        for category in self.object_list.order_by('name'):
            response.append(
                {
                    'id': category.id,
                    'name': category.name
                }
            )

        return JsonResponse(response, safe=False)


class CatDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        category = self.get_object()
        return JsonResponse({"id": category.id, "name": category.name})


@method_decorator(csrf_exempt, name='dispatch')
class CatCreateView(CreateView):
    model = Category
    fields = ['name']

    def post(self, request, *args, **kwargs):
        category_data = json.loads(request.body)

        new_category = Category.objects.create(**category_data)
        return JsonResponse({'id': new_category.id, 'name': new_category.name})


@method_decorator(csrf_exempt, name='dispatch')
class CatUpdateView(UpdateView):
    model = Category
    fields = ['name']

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        category_data = json.loads(request.body)

        self.object.name = category_data['name']
        self.object.save()
        return JsonResponse({'id': self.object.id, 'name': self.object.name})


@method_decorator(csrf_exempt, name='dispatch')
class CatDeleteView(DeleteView):
    model = Category
    success_url = '/'

    # работает от POST запроса
    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)


# ____________________________________________________________________________
# model Ad - ModelViewSet
# ___________________________________________________________________________

class AdViewSet(ModelViewSet):
    queryset = Ad.objects.order_by('-price')
    serializer_class = AdSerializer

    def list(self, request, *args, **kwargs):

        categories = request.GET.getlist("cat")
        if categories:
            self.queryset = self.queryset.filter(category_id__in=categories)

        text = request.GET.get('text')
        if text:
            self.queryset = self.queryset.filter(name__icontains=text)

        location = request.GET.get('location')
        if location:
            self.queryset = self.queryset.filter(author__location__name__icontains=location)

        price_from = request.GET.get('price_from')
        if price_from:
            self.queryset = self.queryset.filter(price__gte=price_from)

        price_to = request.GET.get('price_to')
        if price_to:
            self.queryset = self.queryset.filter(price__lte=price_to)

        return super().list(request, *args, **kwargs)
