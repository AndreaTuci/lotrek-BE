from rest_framework import serializers


class SendMessageSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=4096, required=False)
    image = serializers.ImageField(required=False)

    def validate(self, attrs):
        if 'text' not in attrs.keys() and 'image' not in attrs.keys():
            raise serializers.ValidationError({"error": "You must provide either a text or a image"})
        return attrs
