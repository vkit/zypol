from rest_framework import serializers
from django.contrib.auth.models import User

class RegisterSerializer(serializers.Serializer):
	email = serializers.EmailField()
	role = serializers.IntegerField()
	password = serializers.CharField(min_length=8)

class LoginSerializer(serializers.Serializer):
	email = serializers.EmailField()
	password = serializers.CharField(min_length=8)



class AddTaskSerializer(serializers.Serializer):
    task_headline = serializers.CharField(max_length=100)
    task_body = serializers.CharField(max_length=1000)

class UpdateStatusSerializer(serializers.Serializer):
	status = serializers.IntegerField()
	task_id = serializers.IntegerField()

class ApproveTaskSerializer(serializers.Serializer):
	task_id = serializers.IntegerField()
	status = serializers.IntegerField()