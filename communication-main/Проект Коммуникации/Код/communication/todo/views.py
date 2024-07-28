from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from roles.models import MyGroup, MyGroup
from users.models import User
from todo.models import ToDo

from .forms import Todo_form

from django.views import View
from django.views.generic import UpdateView, DeleteView, DetailView, CreateView

# Create your views here.

def index(request):
    return render(request, 'todo/lolkek.html', {})


class SendTasks(View):
    def get(self, request):
        if request.user.is_authenticated:
            users = User.objects.all()
            tasks = ToDo.objects.all()
            groups = MyGroup.objects.all()
        else:
            users = User.objects.none()
            tasks = ToDo.objects.none()
            groups = MyGroup.objects.none()

        return render(
            request,
            "todo/layout.html",
            {"users": users, 'tasks': tasks, 'groups': groups},
        )

    def post(self, request):
        user_id = request.POST.get("user")
        user = User.objects.get(id=user_id)

        group_id = request.POST.get("group")
        group = MyGroup.objects.get(id=group_id)

        task_description = request.POST.get("task")
        if task_description:
            ToDo.objects.create(
                task=task_description,
                employee=user,
                group = group,
                description=request.POST.get("description"),
                priority=request.POST.get("priority"),
                date=request.POST.get("date")
            )

        return redirect("send_tasks")

def update(request, task_id):
    task = ToDo.objects.get(id=task_id)
    task.is_complete = not task.is_complete
    task.save()
    return redirect('send_tasks')


def delete(request, task_id):
    task = ToDo.objects.get(id=task_id)
    task.delete()
    return redirect('send_tasks')

class Correction(UpdateView):
    template_name = 'todo/new_note.html'
    form_class = Todo_form
    success_url = '/todo/'
    model = ToDo
