from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from task_management.models import Task
from task_management.models import Manager
from task_management.serializers import TaskSerializer, ManagerSerializer
from rest_framework.permissions import IsAuthenticated
from task_management.pagination import CustomPagination
from django.core.mail import send_mail
from django.conf import settings


class ViewTaskList(APIView):

    # This view is for displaying all the tasks assigned to Employee.
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        """
        If the request is sent by Employee then display the tasks assigned to
        them else send the error response.
        """
        user = request.user

        # check that user is in Employee Group or not
        if user.groups.filter(name='Employee').exists():

            # retrieve the data entered by user
            username = request.data.get("user")

            # If username is not provided then returns an error
            if username is None:
                response = {
                    "status": False,
                    "message": "Provide user to retrieve tasks",
                    "data": None
                }
                return Response(data=response,
                                status=status.HTTP_400_BAD_REQUEST)

            # check if username exists or not
            if User.objects.filter(username=username).exists():
                user_id = User.objects.get(username=username).id
                tasks = Task.objects.filter(user=user_id)

                # Add pagination to tasks queryset
                paginator = CustomPagination()
                paginated_queryset = paginator.paginate_queryset(tasks, request)
                serializer = TaskSerializer(paginated_queryset, many=True)

                # If No Task assigned to user
                if serializer.data == []:
                    response = {
                        "status": True,
                        "message": "You have no tasks to do",
                        "data": None
                    }
                    return Response(data=response, status=status.HTTP_200_OK)

                # return Task assigned to user
                response = {
                    "status": True,
                    "message": "List of Tasks which you have to complete",
                    "data": serializer.data
                }
                return paginator.get_paginated_response(data=response)

            # returns an error response if user does not exist
            else:
                response = {
                    "status": False,
                    "message": "User does not exist",
                    "data": None
                }
                return Response(data=response,
                                status=status.HTTP_400_BAD_REQUEST)

        # If there is no Employee with the user request.
        else:
            response = {
                "status": False,
                "message": "The requested user is not Employee so you can not view task ",
                "data": None
            }
            return Response(data=response,
                            status=status.HTTP_400_BAD_REQUEST)
