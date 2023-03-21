from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import Group
from django.contrib.auth.models import User


# Serializer for user registration
class RegistrationSerializer(serializers.ModelSerializer):

    # Define the model and fields for the serializer
    class Meta:
        model = User
        fields = ["email", "username", "password", "user_type"]
        extra_kwarg = {"password": {"write_only": True}}

    # Use a validator to ensure email is unique
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())])

    # Use a password field to ensure password is write_only and encrypted
    password = serializers.CharField(
        style={"input_type": "password", "write_only": True}
    )

    # define User_type to check user is employee or manager
    user_type = serializers.IntegerField(required=True)

    # Create a new user with the validated data
    def create(self, validated_data):
        user_type = validated_data.pop('user_type')
        user = User.objects.create_user(**validated_data)
        if user_type == 1:
            group = Group.objects.get(name='Employee')
            group.user_set.add(user)
        else:
            group = Group.objects.get(name='Manager')
            group.user_set.add(user)
        return user
