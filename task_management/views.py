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


class TaskView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):

        # retrieve the requested user
        user = request.user

        # check if the requested user is manager or not
        if user.groups.filter(name='Manager').exists():

            # retrieve the details entered by user
            username = request.data.get("user")
            title = request.data.get("title")
            description = request.data.get("description")
            due_date = request.data.get("due_date")

            # check if user entered details or not
            if username is None or title is None or description is None or due_date is None:
                response = {
                    "status": False,
                    "message": "Provide details to assign Task",
                    "data": None
                }
                return Response(data=response,
                                status=status.HTTP_400_BAD_REQUEST)

            # check if the user provided by manager is present or not
            if User.objects.filter(username=username).exists():
                user_id = User.objects.get(username=username).id
                email = User.objects.get(username=username).email

                taskdata = {
                    "title": title,
                    "description": description,
                    "due_date": due_date,
                    "user": user_id
                    }

                # Save the data entered by user with serializer
                serializer = TaskSerializer(data=taskdata)
                if serializer.is_valid():

                    # notification to User by mail
                    subject = "Task Created "
                    message = "The task is created!Please check the task"
                    # send_mail(
                    #     subject,
                    #     message,
                    #     settings.EMAIL_HOST_USER,
                    #     [email],
                    #     fail_silently=False
                    # )
                    task = serializer.save()
                    response = {
                        "status": True,
                        "message": "Task created for Employee is successful!!"
                    }
                    return Response(data=response,
                                    status=status.HTTP_201_CREATED)

                # if there is issue in serializer then returns error
                else:
                    response = {
                        "status": False,
                        "message": serializer.errors,
                        "data": None
                    }
                    return Response(data=response,
                                    status=status.HTTP_400_BAD_REQUEST)

            # If user does not exist then response an error message
            else:
                response = {
                    "status": False,
                    "message": "User does not exist with given user",
                    "data": None
                }
                return Response(data=response,
                                status=status.HTTP_400_BAD_REQUEST)

        # returns response if User is not authorized to add task
        else:
            response = {
                    "status": False,
                    "message": "You are not authorized to create Tasks",
                    "data": None
                }
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):

        # retrieve the requested user
        user = request.user

        # check if the requested user is manager or not
        if user.groups.filter(name='Manager').exists():

            # retrieve the details entered by user
            username = request.data.get("user")
            title = request.data.get("title")
            description = request.data.get("description")
            due_date = request.data.get("due_date")

            # check if user entered details or not
            if username is None or title is None or description is None or due_date is None:
                response = {
                    "status": False,
                    "message": "Provide information which you want to update in Task",
                    "data": None
                }
                return Response(data=response,
                                status=status.HTTP_400_BAD_REQUEST)

            # check if the user provided by manager is present or not
            if Task.objects.filter(id=pk).exists():
                user = Task.objects.get(id=pk).user
                user_id = User.objects.get(username=user).id
                email = User.objects.get(username=user).email

                # dictionary for data entered by user
                taskdata = {
                    "title": title,
                    "description": description,
                    "due_date": due_date,
                    "user": user_id
                }

                # Save the data entered by user with serializer
                task = Task.objects.get(id=pk)
                serializer = TaskSerializer(task, data=taskdata)
                if serializer.is_valid():

                    # notification to User by mail
                    subject = "Task Updated "
                    message = "The task assigned to you is updated!Please check it"
                    # send_mail(
                    #     subject,
                    #     message,
                    #     settings.EMAIL_HOST_USER,
                    #     [email],
                    #     fail_silently=False
                    # )
                    serializer.save()
                    response = {
                        "status": True,
                        "message": "Task updated for Employee is successful!!"
                    }
                    return Response(data=response,
                                    status=status.HTTP_200_OK)

                # if there is issue in serializer then returns error
                else:
                    response = {
                        "status": False,
                        "message": serializer.errors,
                        "data": None
                    }
                    return Response(data=response,
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                # if the task does not present then returns error message
                response = {
                    "status": False,
                    "message": "task does not present in the list",
                    "data": None
                }
                return Response(data=response,
                                status=status.HTTP_400_BAD_REQUEST)

        # returns response if User is not authorized to add task
        else:
            response = {
                    "status": False,
                    "message": "You are not authorized to update Tasks",
                    "data": None
                }
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):

        # retrieve the requested user
        user = request.user

        # check if the requested user is manager or not
        if user.groups.filter(name='Manager').exists():

            # If title exists, then delete it.
            if Task.objects.filter(id=pk).exists():
                task = Task.objects.get(id=pk)
                task.delete()

                # returns success response of deletion of task
                response = {
                    "status": True,
                    "message": "Task successfully deleted"
                }
                return Response(data=response, status=status.HTTP_200_OK)

            # returns error if Task with given title does not exist
            else:
                response = {
                    "status": False,
                    "message": "Task with given id does not exist",
                    "data": None
                }
                return Response(data=response, status=status.HTTP_200_OK)

        # returns response if User is not authorized to add task
        else:
            response = {
                "status": False,
                "message": "You are not authorized to delete task",
                "data": None
            }
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):

        # Retrieve data of Tasks assigned to employees
        user = request.user
        # check that user is in Manager group or not
        if user.groups.filter(name="Manager").exists():
            manager = request.data.get("manager")

            # If the manager is none then returns an error message
            if manager is None:
                response = {
                    "status": False,
                    "message": "Provide manager to retrieve tasks",
                    "data": None
                }
                return Response(data=response,
                                status=status.HTTP_400_BAD_REQUEST)

            # retrieve the tasks assigned by manager
            if User.objects.filter(username=manager).exists():
                user_id = User.objects.get(username=manager).id
                tasks = Manager.objects.filter(manager=user_id)

                # add pagination in viewing Task
                paginator = CustomPagination()
                paginated_queryset = paginator.paginate_queryset(tasks, request)
                serializer = ManagerSerializer(paginated_queryset, many=True)

                # If serializer data is None then returns an response
                if serializer.data == []:
                    response = {
                        "status": True,
                        "message": "You did not assigned task",
                        "data": None
                    }
                    return Response(data=response, status=status.HTTP_200_OK)

                # returns success response of task assigned by manager
                response = {
                    "status": True,
                    "message": "List of tasks which you assigned",
                    "data": serializer.data
                }
                return paginator.get_paginated_response(data=response)

            # If user does not exist then returns an error response
            else:
                response = {
                    "status": False,
                    "message": "User does not exist with given name",
                    "data": None
                }
                return Response(data=response,
                                status=status.HTTP_400_BAD_REQUEST)

        # If requested user is not manager
        else:
            response = {
                "status": False,
                "message": "You are not authorized to view this task!!",
                "data": None
            }
            return Response(data=response,
                            status=status.HTTP_400_BAD_REQUEST)

