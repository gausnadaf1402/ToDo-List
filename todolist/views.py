from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .models import Task
from .serializers import ListSerializer
from rest_framework import status
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.utils.decorators import method_decorator

# Create your views here.
class TaskList(LoginRequiredMixin,ListView):
    model=Task                                  
    template_name='todolist/task_list.html'
    context_object_name='tasks'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()
        return context
    

class TaskDetail(DetailView):
    model=Task
    template_name='todolist/task_detail.html'
    context_object_name='task'

class TaskCreate(CreateView):
    model=Task
    template_name='todolist/task_form.html'
    fields='__all__'
    success_url=reverse_lazy('tasks')

class TaskUpdate(UpdateView):
    model=Task
    fields='__all__'
    success_url=reverse_lazy('tasks')

class TaskDelete(DeleteView):
    model=Task
    context_object_name='task'
    success_url=reverse_lazy('tasks')

class CustomLoginView(LoginView):
    model=Task
    fields='__all__'
    template_name='todolist/login.html'
    redirect_authenticated_user=True

    def get_success_url(self):
        return reverse_lazy('tasks')
 
class RegisterPage(FormView):
    model=Task
    template_name='todolist/register.html'
    redirect_authenticated_user=True
    form_class=UserCreationForm
    success_url=reverse_lazy('tasks')

    def form_valid(self,form):
        user=form.save()
        if user is not None:
            login(self.request,user)
        return super(RegisterPage,self).form_valid(form)






