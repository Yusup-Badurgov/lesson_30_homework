from django.db.models import Count, Q
from django.shortcuts import render

# Create your views here.
import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from ads.models import Category, Ad, User
from lesson_27_homework import settings
from users.models import Location


@method_decorator(csrf_exempt, name='dispatch')
class UserListView(ListView):
    model = User

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        paginator = Paginator(
            self.object_list.order_by('username').annotate(total_ads=Count('ad', filter=Q(ad__is_published=True))),
            settings.TOTAL_ON_PAGE)
        page_number = request.GET.get('page', 1)

        page_obj = paginator.get_page(page_number)

        users = []
        for user in page_obj:
            users.append(
                {
                    'id': user.id,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'username': user.username,
                    "role": user.role,
                    "age": user.age,
                    "total_ads": user.total_ads
                }
            )

        response = {
            'total': page_obj.paginator.count,
            'num_pages': page_obj.paginator.num_pages,
            'items': users
        }
        return JsonResponse(response, safe=False)


class UserDetailView(DetailView):
    model = User

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        return JsonResponse({
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            "role": user.role,
            'location': [loc.name for loc in user.location.all()],
            "age": user.age
        })


@method_decorator(csrf_exempt, name='dispatch')
class UserCreateView(CreateView):
    model = User
    fields = '__all__'

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        locations = data.pop('location')
        user = User.objects.create(**data)

        for loc_name in locations:
            loc, _ = Location.objects.get_or_create(name=loc_name)
            user.location.add(loc)
        return JsonResponse({
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            "role": user.role,
            'location': [loc.name for loc in user.location.all()],
            "age": user.age})


@method_decorator(csrf_exempt, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = '__all__'

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        ad_data = json.loads(request.body)

        if 'first_name' in ad_data:
            self.object.first_name = ad_data['first_name']
        if 'last_name' in ad_data:
            self.object.last_name = ad_data['last_name']
        if 'username' in ad_data:
            self.object.username = ad_data['username']
        if 'age' in ad_data:
            self.object.age = ad_data['age']
        if 'location' in ad_data:
            self.object.location.all().clear()
            for loc_name in ad_data['location']:
                loc, _ = Location.objects.get_or_create(name=loc_name)
                self.object.location.add(loc)
        self.object.save()

        self.object.save()
        return JsonResponse(
            {
                'id': self.object.id,
                'first_name': self.object.first_name,
                'last_name': self.object.last_name,
                'username': self.object.username,
                "role": self.object.role,
                'location': [loc.name for loc in self.object.location.all()],
                "age": self.object.age}
        )


@method_decorator(csrf_exempt, name='dispatch')
class UserDeleteView(DeleteView):
    model = User
    success_url = '/'

    # работает от POST запроса
    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
