from rest_framework import serializers


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


class CreateGenreResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()


class UpdateGenreRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255)
    is_active = serializers.BooleanField()


class UpdateGenreResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255)
    is_active = serializers.BooleanField()


class DeleteGenreRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField()
