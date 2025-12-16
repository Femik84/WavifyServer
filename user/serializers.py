from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for registering a new user.
    Accepts full_name, email, password, and optional bio & image.
    """
    password = serializers.CharField(write_only=True, min_length=6)
    bio = serializers.CharField(required=False, allow_blank=True)
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = ['full_name', 'email', 'password', 'bio', 'image']

    def create(self, validated_data):
        bio = validated_data.get('bio', None)
        image = validated_data.get('image', None)

        user = User.objects.create_user(
            email=validated_data['email'],
            full_name=validated_data['full_name'],
            password=validated_data['password'],
            bio=bio,
            image=image
        )
        return user


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    Accepts email and password.
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise serializers.ValidationError("Invalid email or password")
        else:
            raise serializers.ValidationError("Both email and password are required")

        attrs['user'] = user
        return attrs
