from rest_framework import serializers

class GreetingSerializer(serializers.Serializer):
    client_ip = serializers.CharField()
    location = serializers.CharField(max_length=100, default='Unknown')
    greeting = serializers.CharField()
