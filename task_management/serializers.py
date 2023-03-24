from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from task_management.models import Task, Manager


# Serializer of Task Model
class TaskSerializer(serializers.ModelSerializer):

    title = serializers.CharField(
        validators=[UniqueValidator(queryset=Task.objects.all())])

    class Meta:
        model = Task
        fields = "__all__"


# Serializer of Manager Models
class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manager
        fields = "__all__"
