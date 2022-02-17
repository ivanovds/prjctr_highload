import traceback

from rest_framework import serializers

from .models import Entry


class EntrySerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        ModelClass = self.Meta.model
        try:
            instance = ModelClass.objects.using('mongo').create(**validated_data)
        except TypeError:
            tb = traceback.format_exc()
            msg = (
                'Got a `TypeError` when calling `%s.%s.create()`. '
                'This may be because you have a writable field on the '
                'serializer class that is not a valid argument to '
                '`%s.%s.create()`. You may need to make the field '
                'read-only, or override the %s.create() method to handle '
                'this correctly.\nOriginal exception was:\n %s' %
                (
                    ModelClass.__name__,
                    ModelClass._default_manager.name,
                    ModelClass.__name__,
                    ModelClass._default_manager.name,
                    self.__class__.__name__,
                    tb
                )
            )
            raise TypeError(msg)
        return instance

    class Meta:
        model = Entry
        fields = '__all__'

