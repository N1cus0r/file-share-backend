from rest_framework import serializers

from .models import SharedData


class SharedDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SharedData
        fields = ["title", "message", "file", "code"]

    def create(self, validated_data):
        if not validated_data.get("file"):
            raise serializers.ValidationError("File or was not supplied")

        if not validated_data.get("title"):
            validated_data["title"] = validated_data["file"].name

        return super().create(validated_data)
