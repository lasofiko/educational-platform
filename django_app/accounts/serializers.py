from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    role_display = serializers.CharField(source='get_role_display', read_only=True)

    class Meta:
        model = UserProfile
        fields = ('id', 'user', 'role', 'role_display', 'grade', 'target_score')


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    role = serializers.ChoiceField(
        choices=[UserProfile.ROLE_STUDENT, UserProfile.ROLE_PARENT],
        write_only=True,
        required=True,
    )
    grade = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    target_score = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'password', 'password2',
            'role', 'grade', 'target_score',
        )

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Пароли не совпадают."})

        role = attrs.get('role')
        grade = attrs.get('grade')
        valid_grades = {choice[0] for choice in UserProfile.GRADE_CHOICES}

        if role == UserProfile.ROLE_STUDENT:
            if grade is None:
                raise serializers.ValidationError({'grade': 'Укажите класс (8–11) для ученика.'})
            if grade not in valid_grades:
                raise serializers.ValidationError({'grade': 'Класс должен быть с 8 по 11.'})
        elif role == UserProfile.ROLE_PARENT:
            attrs['grade'] = None

        return attrs

    def create(self, validated_data):
        role = validated_data.pop('role')
        grade = validated_data.pop('grade', None)
        target_score = validated_data.pop('target_score', None)
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        profile, _ = UserProfile.objects.get_or_create(user=user)
        profile.role = role
        if role == UserProfile.ROLE_STUDENT:
            profile.grade = grade
        else:
            profile.grade = None
        if target_score is not None:
            profile.target_score = target_score
        profile.save()
        return user


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password2 = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({"new_password": "Пароли не совпадают."})
        return attrs