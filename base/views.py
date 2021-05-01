from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse


from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.response import Response
from .serializers import TaskSerializer,UserSerializer
from .models import Task,User

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from notifications.signals import notify
# Create your views here.

"""
API Overview
"""
@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'List' : '/task-list/',
        'Detail View' : '/task-detail/<str:pk>/',
        'Create' : '/task-create/',
        'Update' : '/task-update/<str:pk>/',
        'Delete' : '/task-delete/<str:pk>/',
        'Inbox' : '/inbox/notifications/'
    }
    return Response(api_urls)
"""
Below Function going to display all the tasks store in the data base.
"""
@api_view(['GET'])
# @authentication_classes([SessionAuthentication, BasicAuthentication])
# @permission_classes([IsAuthenticated])
def taskList(request):
    tasks = Task.objects.filter(user=request.user)
    serializer = TaskSerializer(tasks, many = True)
    return Response(serializer.data)


"""
This Function going to display Detailed view of one particuler task with the help of pk.
"""
@api_view(['GET'])
# @authentication_classes([SessionAuthentication, BasicAuthentication])
# @permission_classes([IsAuthenticated])
def taskDetail(request, pk):
    task = Task.objects.get(id=pk)
    if(task.user == request.user):
        serializer = TaskSerializer(task, many = False)
        return Response(serializer.data)



@api_view(['POST'])
# @authentication_classes([SessionAuthentication, BasicAuthentication])
# @permission_classes([IsAuthenticated])
def taskCreate(request):
    serializer = TaskSerializer(data=request.data)
    notify.send(User.objects.get(id=1), recipient = User.objects.get(id=1), verb = f"Task created by user {request.user}")
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)



@api_view(['POST'])
# @authentication_classes([SessionAuthentication, BasicAuthentication])
# @permission_classes([IsAuthenticated])
def taskUpdate(request, pk):
    task = Task.objects.get(id = pk)
    serializer = TaskSerializer(instance=task, data=request.data)

    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['DELETE'])
# @authentication_classes([SessionAuthentication, BasicAuthentication])
# @permission_classes([IsAuthenticated])
def taskDelete(request, pk):
    task = Task.objects.get(id = pk)
    task.delete()
    return Response("Taks deleted successfully.")


