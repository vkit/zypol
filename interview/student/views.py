from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.views import APIView
from .models import Userprofile,Task
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import permission_classes
from .utils import check_availibity
from .serializers import AddTaskSerializer, UpdateStatusSerializer, ApproveTaskSerializer, RegisterSerializer, LoginSerializer


class Register(APIView):
    def post(self, request):
        try:
            data = request.POST
            serializer = RegisterSerializer(data=data)
            if not serializer.is_valid():
                st = {'STATUS': 'FAILURE', 'MESSAGE': 'INVALID DATA'}
                return Response({'meta': st})
            email = data.get('email')
            password = data.get('password')
            role = data.get('role')
            availability = check_availibity(username=data.get('email'))
            if availability:
                st = {'STATUS': 'FAILURE', 'MESSAGE': 'USER IS ALREADY EXISTS'}
                return Response({'meta': st}) 
            
            user = User.objects.create_user(username=email,password=password)
                
            userprofile = Userprofile.objects.create(user=user)

            token,created = Token.objects.get_or_create(user=user)
            lis = list()
            if token:
                data = {'user_id':user.id,'email':email,'token':token.pk,'role':role}
                lis.append(data)
            st = {'STATUS': 'SUCCESS', 'MESSAGE': 'REGISTER'}
            return Response({'meta': st, 'register': lis})
        except Exception as e:
            print e


class Login(APIView):
    def post(self, request):
        try:
            data = request.POST
            serializer = LoginSerializer(data=data)
            if not serializer.is_valid():
                st = {'STATUS': 'FAILURE', 'MESSAGE': 'INVALID DATA'}
                return Response({'meta': st})
            email = data.get('email')
            password = data.get('password')
            lis = list()
            availability = check_availibity(username=data.get('email'))
            if not availability:
                st = {'STATUS': 'FAILURE', 'MESSAGE': 'NO DATA'}
                return Response({'meta': st}) 
            user = authenticate(username=email, password=password)
            if user is not None:
                token,created = Token.objects.get_or_create(user=user)
                user_detail = {
                    'token':token.pk, 
                    'user':user.username,
                    'user_id': user.id
                }
                lis.append(user_detail)
                st = {'STATUS': 'SUCCESS', 'MESSAGE': 'LOGIN'}
                return Response({'meta': st,'data':lis})
        except  Exception as e:
            print e

class UpdateProfile(APIView):
    def get(self, request):
        try:
            user = request.user
            userprofile = Userprofile.objects.get(user=user)
            if userprofile.role == 3:
                userprofile.is_admin = True
                userprofile.save()
                st = {'STATUS': 'SUCCESS', 'MESSAGE': 'userprofile updated SUCCESFULLY'}
                return Response({'meta': st})
            elif userprofile.role == 2:
                userprofile.is_teacher = True
                userprofile.save()
                st = {'STATUS': 'SUCCESS', 'MESSAGE': 'userprofile updated SUCCESFULLY'}
                return Response({'meta': st})
            else:
                userprofile.is_student = True
                userprofile.save()
                st = {'STATUS': 'SUCCESS', 'MESSAGE': 'userprofile updated SUCCESFULLY'}
                return Response({'meta': st})
        except Exception as e:
            print e



class TaskAssign(APIView):
    def post(self, request):
        try:
            user = request.user
            data = request.POST
            serializer = AddTaskSerializer(data=data)
            if not serializer.is_valid():
                st = {'STATUS': 'FAILURE', 'MESSAGE': 'INVALID DATA'}
                return Response({'meta': st})
            lis=list()
            userprofile = Userprofile.objects.get(user=user)
            if userprofile.is_admin or userprofile.is_teacher:
                Task.objects.create(
                    task_headline = data.get('task_headline'),
                    task_body = data.get('task_body'),
                    user=user,
                    task_status=1
                )
                detail = {
                    'task_headline': data.get('task_headline'),
                    'task_body': data.get('task_body'),
                    'user': user.username,
                    'task_status': 1
                }
                lis.append(detail)
                st = {'STATUS': 'SUCCESS', 'MESSAGE': 'TASK CREATED SUCCESFULLY'}
                return Response({'meta': st, 'data': lis})
            else:
                st = {'STATUS': 'FAILURE', 'MESSAGE': 'YOU ARE NOT ADMIN OR TEACHER'}
                return Response({'meta': st})
        except Exception as e:
            print e

    def delete(self, request, task_id):
        try:
            user = request.user
            userprofile = Userprofile.objects.get(user=user)
            if userprofile.is_admin:
                task=Task.objects.filter(pk=task_id, user=user)
                if task.exists():
                    task.delete()
                    st = {'STATSU': 'SUCCESS', 'MESSAGE': 'SUCCESFULLY DELETED'}
                    return Response({'meta':st})
                else:
                    st = {'STATSU': 'FAILURE', 'MESSAGE': 'NO TASK TO DELETE'}
                    return Response({'meta':st})
            else:
                st = {'STATUS': 'FAILURE', 'MESSAGE': 'YOU ARE NOT ADMIN'}
                return Response({'meta': st})
        except Exception as e:
            print e


class UpdateStatus(APIView):
    def put(self, request):
            try:
                data = request.POST
                serializer = UpdateStatusSerializer(data=data)
                if not serializer.is_valid():
                    st = {'STATUS': 'FAILURE', 'MESSAGE': 'INVALID DATA'}
                    return Response({'meta': st})
                task=Task.objects.get(pk=data.get('task_id'))
                task.task_status = data.get('status')
                task.save()
                lis=list()
                data_detail = {
                    'status': data.get('status')
                }
                lis.append(data_detail)
                st = {'STATSU': 'SUCCESS', 'MESSAGE': 'SUCCESFULLY UPDATED'}
                return Response({'meta':st, 'data':lis})

            except Task.DoesNotExist:
                st = {'STATSU': 'FAILURE', 'MESSAGE': 'TASK DOENOT EXISTS'}
                return Response({'meta':st})



class ApproveTask(APIView):
    def put(self, request):
        data = request.POST
        user = request.user
        serializer = ApproveTaskSerializer(data=data)
        if not serializer.is_valid():
            st = {'STATUS': 'FAILURE', 'MESSAGE': 'INVALID DATA'}
            return Response({'meta': st})
        userprofile = Userprofile.objects.get(user=user)
        task = Task.objects.get(pk=data.get('task_id'))
        if userprofile.is_admin or userprofile.is_teacher:
            if task.task_status == 6:
                task.task_status = data.get('status')
                task.save()
                st = {'STATSU': 'SUCCESS', 'MESSAGE': 'SUCCESFULLY UPDATED'}
                return Response({'meta':st})
            else:
                st = {'STATSU': 'FAILURE', 'MESSAGE': 'TASK STILL UNDER PROGRESS'}
                return Response({'meta':st})
        else:
            st = {'STATSU': 'FAILURE', 'MESSAGE': 'YOU ARE NOT ADMIN OR TEACHER TO ARROVE'}
            return Response({'meta':st})


class TaskList(APIView):
    def get(self, request):
        try:
            user = request.user
            data = request.POST
            lis = []
            tasks=Task.objects.filter(user=user).exclude(task_status=6)
            for task in tasks:
                task_id = task.id
                task_headline = task.task_headline
                task_body = task.task_body
                task_status = task.task_status
                data_detail = {
                    'task_id': task_id,
                    'task_headline': task_headline,
                    'task_body': task_body,
                    'task_status': task_status
                } 
                lis.append(data_detail)
            st = {'STATUS':'SUCCESS', 'MESSAGE': 'TASKLIST'}
            return Response({"meta": st, 'task_list': lis})
        except Task.DoesNotExist:
            st = {'STATSU': 'FAILURE', 'MESSAGE': 'TASK DOENOT EXISTS'}
            return Response({'meta':st})

