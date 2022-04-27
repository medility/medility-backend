from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import AddressList
from django.contrib.auth import get_user_model
User = get_user_model()


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('phone', 'password', 'name', 'email', 'gender', 'dob', 'primary_user_ref', 'user_type')
        extra_kwargs = {'password': {'write_only': True}, }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):

   
    class Meta:
        model = User
        fields = ('phone', 'name', 'gender', 'email', 'dob' )


class UserBasicInfoSerializer(serializers.ModelSerializer):

   
    class Meta:
        model = User
        fields = ('phone', 'name', 'gender', )


class AddressInfoForUserToNurseSerializer(serializers.ModelSerializer):
    user = UserBasicInfoSerializer()

    class Meta:
        model = AddressList
        fields = ('title', 'city', 'country', 'area', 'address1', 'pincode', 'user')


class AddressListSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressList
        fields = '__all__'

        def update(self, instance, validated_data):
            instance.city = validated_data('city', instance.city)
            instance.country = validated_data('country', instance.country)
            instance.area = validated_data('area', instance.area)
            instance.pincode = validated_data('pincode', instance.pincode)
            instance.address1 = validated_data('address1', instance.address1)
            instance.title = validated_data('title', instance.title)
            instance.save()
            return instance


class LoginUserSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        phone = attrs.get('phone')
        password = attrs.get('password')
        print(phone)
        print(password)
        if phone and password:
            if User.objects.filter(phone=phone).exists():
                user = authenticate(request=self.context.get('request'),
                                    phone=phone, password=password)
                
            else:
                msg = {'detail': 'Phone number is not registered.',
                       'register': False}
                raise serializers.ValidationError(msg)

            if not user:
                msg = {
                    'detail': 'Unable to log in with provided credentials.', 'register': True}
                raise serializers.ValidationError(msg, code='authorization')

        else:
            msg = 'Must include "username" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    """
    Used for both password change (Login required) and 
    password reset(No login required but otp required)

    not using modelserializer as this serializer will be used for for two apis
    """

    password_1 = serializers.CharField(required=True)
    # password_1 can be old password or new password
    password_2 = serializers.CharField(required=True)
    # password_2 can be new password or confirm password according to apiview


class ForgetPasswordSerializer(serializers.Serializer):
    """
    Used for resetting password who forget their password via otp varification
    """
    phone = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
   
