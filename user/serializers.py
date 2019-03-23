from rest_framework import serializers

# from django.contrib.auth.models import User
from user.models import User


class UserSerializers(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'id', 'url', 'username', 'password', 'is_active', 'is_staff', 'is_superuser',
            'groups')
