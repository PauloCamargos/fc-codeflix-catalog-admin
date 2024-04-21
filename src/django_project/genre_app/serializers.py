from rest_framework import serializers


# class SetField(serializers.ListField):
#     def to_internal_value(self, data):
#         return set(super().to_internal_value(data))


class GenreResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255)
    is_active = serializers.BooleanField()
    categories = serializers.ListField(child=serializers.UUIDField())


class ListGenreResponseSerializers(serializers.Serializer):
    data = GenreResponseSerializer(many=True)


class RetrieveGenreRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField()


class RetrieveGenreResponseSerializer(serializers.Serializer):
    data = GenreResponseSerializer(source="*")


class CreateGenreRequestSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    is_active = serializers.BooleanField(default=True)
    categories = serializers.ListField(child=serializers.UUIDField(), default=list())


class CreateGenreResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()


class UpdateGenreRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255)
    is_active = serializers.BooleanField()
    categories = serializers.ListField(child=serializers.UUIDField())


class UpdateGenreResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255)
    is_active = serializers.BooleanField()
    categories = serializers.ListField(child=serializers.UUIDField(), default=list())


class DeleteGenreRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField()
