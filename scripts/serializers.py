from rest_framework import serializers
from scripts.models import Scripts


class ScriptsSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Scripts
        fields = ('url', 'id', 'script_name', 'script_file', 'script_args', 'script_type', 'script_author')
