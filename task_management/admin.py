from django.contrib import admin
from task_management.models import Task
from task_management.models import Manager


# Registration of Task Model
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "description", "created_date", "due_date",
                    "user"]


# Registration of Manager Model
@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ["manager", "Task", "employee"]
