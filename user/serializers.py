from rest_framework import serializers

# from django.contrib.auth.models import User
from user.models import User


class UserSerializers(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'id', 'url', 'username', 'password', 'email', 'is_active', 'is_staff', 'is_superuser',
            'groups')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
