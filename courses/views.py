from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.http import HttpResponse, Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import UserForm, UserUpdateForm
from .connector import User, Course

import json
# Create your views here.


class UserListView(View):

    def get(self, request):
        page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 10))
        search = request.GET.get('search', None)
        users = None
        if search:
            users = User.filter(search)
        else:
            users = User.all()
        if not users:
            return render(request, 'courses/user_list.html')
        paginator = Paginator(users, limit)
        displayed_pages = []
        current_page = None
        try:
            current_page = paginator.page(page)
        except PageNotAnInteger:
            current_page = paginator.page(1)
        except EmptyPage:
            current_page = paginator.page(paginator.num_pages)
        if paginator.num_pages > 5 and current_page.number >= 4:
            displayed_pages = [i for i in range(current_page.number-2, 3+current_page.number)]
        elif paginator.num_pages <= 5:
            displayed_pages = [i for i in range(1, paginator.num_pages+1)]
        else:
            displayed_pages = [i for i in range(1, 6)]
        return render(
            request,
            'courses/user_list.html',
            {
                'current_page': current_page,
                'displayed_pages': displayed_pages
            })


class UserCreateView(View):

    def dispatch(self, *args, **kwargs):
        if self.request.is_ajax():
            return self.ajax(*args, *kwargs)
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        form = UserForm()
        return render(request, 'courses/create_user.html', {'form': form})

    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            User.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone'],
                mobile_phone=form.cleaned_data['mobile_phone'],
                status=form.cleaned_data['status']
                )
            return redirect(reverse('user_list'))
        return render(request, 'courses/create_user.html', {'form': form})

    def ajax(self, *args, **kwargs):
        post_dict = json.loads(self.request.POST['the_post'])
        post_dict.pop('csrfmiddlewaretoken')
        form = UserForm(post_dict)
        if form.is_valid():
            User.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone'],
                mobile_phone=form.cleaned_data['mobile_phone'],
                status=form.cleaned_data['status']
                )
            response = {'type': 'create'}
            return HttpResponse(json.dumps(response), content_type="application/json")
        else:
            errors = {}
            errors['err'] = form.errors
            errors['type'] = 'error'
            print(errors)
            return HttpResponse(json.dumps(errors))


class UserUpdateView(View):

    def dispatch(self, *args, **kwargs):
        if self.request.is_ajax():
            return self.ajax(kwargs['pk'], *args, *kwargs)
        return super().dispatch(*args, **kwargs)

    def get(self, request, pk):
        user = User.get('id', pk)
        if user is None:
            raise Http404('User not founded')
        user['courses_list'] = [course['code'] for course in Course.user_courses(pk)]
        form = UserUpdateForm(user, initial=user)
        courses = Course.user_courses(user['id'])
        return render(request, 'courses/update_user.html', {'form': form, 'courses': courses})

    def post(self, request, pk):
        user = User.get('id', pk)
        post_dict = request.POST.copy()
        post_dict.pop('courses', None)
        courses = post_dict.pop('courses_list', [])
        form = UserUpdateForm(user, post_dict)
        if form.is_valid():
            User.update(
                id=pk,
                name=user['name'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone'],
                mobile_phone=form.cleaned_data['mobile_phone'],
                status=form.cleaned_data['status']
                )
            User.add_courses(pk, courses)
            return redirect(reverse('user_list'))
        return render(request, 'courses/update_user.html', {'form': form})

    def ajax(self, pk, *args, **kwargs):
        user = User.get('id', pk)
        post_dict = json.loads(self.request.POST['the_post'])
        post_dict.pop('csrfmiddlewaretoken')
        post_dict.pop('courses', None)
        courses = post_dict.pop('courses_list', [])
        form = UserUpdateForm(user, post_dict)
        if form.is_valid():
            User.update(
                id=user['id'],
                name=user['name'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone'],
                mobile_phone=form.cleaned_data['mobile_phone'],
                status=form.cleaned_data['status']
                )
            User.add_courses(user['id'], courses)
            response = {'type': 'update'}
            return HttpResponse(json.dumps(response), content_type="application/json")
        else:
            errors = {}
            errors['err'] = form.errors
            errors['type'] = 'error'
            print(errors)
            return HttpResponse(json.dumps(errors))


class UserDeleteView(View):

    def dispatch(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    def post(self, request, pk):
        query_string = '?' + request.GET.urlencode()
        User.delete(int(pk))
        return redirect(reverse('user_list') + query_string)


class CoursesListView(View):

    def get(self, request):
        courses = Course.all()
        return render(request, 'courses/courses_list.html', {'courses': courses})
