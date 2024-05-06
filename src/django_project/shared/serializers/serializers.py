from rest_framework import serializers


class ListOutputMetaSerializer(serializers.Serializer):
    page = serializers.IntegerField()
    per_page = serializers.IntegerField()
    total = serializers.IntegerField()


class PaginatedListResponseSerializer(serializers.Serializer):
    meta = ListOutputMetaSerializer(read_only=True)
