from rest_framework import permissions, generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import login
from knox.auth import TokenAuthentication
from knox.views import LoginView as KnoxLoginView
# from blissedmaths.utils import phone_validator, password_generator, otp_generator
from .models import AddressList
from .serializers import (CreateUserSerializer, ChangePasswordSerializer, UserSerializer, LoginUserSerializer, ForgetPasswordSerializer, AddressListSerializer)
from accounts.models import User, PhoneOTP
from django.shortcuts import get_object_or_404
from django.db.models import Q
import requests, random, os
from twilio.rest import Client
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.viewsets import ModelViewSet

from rest_framework.views import APIView



class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        print('login hit')
        serializer = LoginUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        if user.last_login is None :
            user.first_login = True
            user.save()
            
        elif user.first_login:
            user.first_login = False
            user.save()
            
        login(request, user)
        return super().post(request, format=None)

class UserAPI(generics.RetrieveAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class Family(APIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        # primary_ref = request.GET.get('username', False)
        family_list = User.objects.filter(primary_user_ref=request.user)
        user_serializer = UserSerializer(family_list, many=True)
        return Response({'family': user_serializer.data})




class ChangePasswordAPI(generics.UpdateAPIView):
    """
    Change password endpoint view
    """
    authentication_classes = (TokenAuthentication, )
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get_object(self, queryset=None):
        """
        Returns current logged in user instance
        """
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get('password_1')):
                return Response({
                    'status': False,
                    'current_password': 'Does not match with our data',
                }, status=status.HTTP_400_BAD_REQUEST)

            self.object.set_password(serializer.data.get('password_2'))
            self.object.password_changed = True
            self.object.save()
            return Response({
                "status": True,
                "detail": "Password has been successfully changed.",
            })

        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)



def send_otp(phone):
    """
    This is an helper function to send otp to session stored phones or 
    passed phone number as argument.
    """

    if phone:
        
        # key = otp_generator()
        phone = str(phone)
        key = random.randint(999, 9999)
        otp_key = str(key)
        #link = f'https://2factor.in/API/R1/?module=TRANS_SMS&apikey=fc9e5177-b3e7-11e8-a895-0200cd936042&to={phone}&from=wisfrg&templatename=wisfrags&var1={otp_key}'
   
        #result = requests.get(link, verify=False)

        return otp_key
    else:
        return False



def send_otp_forgot(phone):
    if phone:
        # key = otp_generator()
        key = random.randint(999, 9999)
        phone = str(phone)
        otp_key = str(key)
        user = get_object_or_404(User, phone__iexact = phone)
        if user.name:
            name = user.name
        else:
            name = phone

        #link = f'https://2factor.in/API/R1/?module=TRANS_SMS&apikey=fc9e5177-b3e7-11e8-a895-0200cd936042&to={phone}&from=wisfgs&templatename=Wisfrags&var1={name}&var2={otp_key}'
   
        #result = requests.get(link, verify=False)
        #print(result)
      
        return otp_key
    else:
        return False


def sendOtpToMobile(mobile, key):
    # account_sid = 'AC2ecf619af2a5b8759815f98127923789'
    # auth_token = '9942ab793572341c377ddab10181cd1d'
    # client = Client(account_sid, auth_token)
    #
    # message = client.messages \
    #     .create(
    #     body="Your otp is "+str(key),
    #     from_='IV-SBNS',
    #     to='+91'+str(mobile)
    # )
    #
    # print(message.sid)
    requests.get("https://2factor.in/API/V1/21674fc2-c371-11eb-8089-0200cd936042/SMS/" + mobile + "/" + key)


# def sendOtpWith2Fctr():
#     url =


############################################################################################################################################################################################
################################################################################################################################################################



class ValidatePhoneSendOTP(APIView):
    '''
    This class view takes phone number and if it doesn't exists already then it sends otp for
    first coming phone numbers'''

    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone')
        if phone_number:
            phone = str(phone_number)
            user = User.objects.filter(phone__iexact = phone)
            if user.exists():
                return Response({'status': False, 'detail': 'Phone Number already exists'})
                 # logic to send the otp and store the phone number and that otp in table. 
            else:
                otp = send_otp(phone)
                print(phone, otp)
                if otp:
                    otp = str(otp)
                    count = 0
                    old = PhoneOTP.objects.filter(phone__iexact = phone)
                    if old.exists():
                        old = old.first()
                        count = old.count
                        old.count = count + 1
                        old.otp = otp
                        old.save()
                        print(old.count)

                    else:
                        count = count + 1
               
                        PhoneOTP.objects.create(
                             phone =  phone, 
                             otp =   otp,
                             count = count
        
                             )
                    if count > 7:
                        return Response({
                            'status' : False, 
                             'detail' : 'Maximum otp limits reached. Kindly support our customer care or try with different number'
                        })
                    
                    
                else:
                    return Response({
                                'status': 'False', 'detail' : "OTP sending error. Please try after some time."
                            })
                sendOtpToMobile(phone, otp)
                return Response({
                    'status': True, 'detail': 'Otp has been sent successfully.'
                })
        else:
            return Response({
                'status': 'False', 'detail' : "I haven't received any phone number. Please do a POST request."
            })


class ValidateOTP(APIView):
    '''
    If you have received otp, post a request with phone and that otp and you will be redirected to set the password
    
    '''

    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone', False)
        otp_sent   = request.data.get('otp', False)

        if phone and otp_sent:
            old = PhoneOTP.objects.filter(phone__iexact = phone)
            if old.exists():
                old = old.first()
                otp = old.otp
                if str(otp) == str(otp_sent):
                    old.logged = True
                    old.save()

                    return Response({
                        'status' : True, 
                        'detail' : 'OTP matched, kindly proceed to save password'
                    })
                else:
                    return Response({
                        'status' : False, 
                        'detail' : 'OTP incorrect, please try again'
                    })
            else:
                return Response({
                    'status' : False,
                    'detail' : 'Phone not recognised. Kindly request a new otp with this number'
                })


        else:
            return Response({
                'status' : 'False',
                'detail' : 'Either phone or otp was not recieved in Post request'
            })


class PhoneNumberExist(APIView):
    def get(self, request, *args, **kwargs):
        phone = request.GET.get('phone', False)
        if phone:
            phone = str(phone)
            user = User.objects.filter(phone__iexact = phone)
            if user.exists():
                return Response({'status': False, 'detail': 'Phone Number already have account associated. Kindly try forgot password'})
            return Response({'status': True, 'detail': 'Please continue registration process'})
        return Response({'status': False, 'detail': 'Please provide mobile number'})


class Register(APIView):

    '''Takes phone and a password and creates a new user only if otp was verified and phone is new'''

    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone', False)
        password = request.data.get('password', False)
        name = request.data.get('name', False)
        dob = request.data.get('dob', False)
        email = request.data.get('email', False)
        gender = request.data.get('gender', False)
        familyref = request.data.get('familyRef', False)
        print(phone)
        print(password)
        print(name)
        print(dob)
        print(email)
        print(gender)
        print(familyref)

        if phone and password and name and dob and email and gender:
            phone = str(phone)
            user = User.objects.filter(phone__iexact = phone)
            if user.exists():
                return Response({'status': False, 'detail': 'Phone Number already have account associated. Kindly try forgot password'})
            else:
                old = PhoneOTP.objects.filter(phone__iexact = phone)
                if old.exists():
                    old = old.first()
                    old.logged = True
                    old.save()
                    if old.logged:
                        Temp_data = {'phone': phone, 'password': password, 'name': name, 'dob': dob, 'email': email, 'gender': gender, 'primary_user_ref': familyref }

                        serializer = CreateUserSerializer(data=Temp_data)
                        serializer.is_valid(raise_exception=True)
                        user = serializer.save()
                        user.save()

                        old.delete()
                        return Response({
                            'status' : True, 
                            'detail' : 'Congrats, user has been created successfully.'
                        })

                    else:
                        return Response({
                            'status': False,
                            'detail': 'Your otp was not verified earlier. Please go back and verify otp'

                        })
                else:
                    return Response({
                    'status' : False,
                    'detail' : 'Phone number not recognised. Kindly request a new otp with this number'
                })




        else:
            return Response({
                'status' : 'False',
                'detail' : 'Please provide all mandate(*) fields'
            })


        



    
class ValidatePhoneForgot(APIView):
    '''
    Validate if account is there for a given phone number and then send otp for forgot password reset'''

    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone')
        if phone_number:
            phone = str(phone_number)
            user = User.objects.filter(phone__iexact = phone)
            if user.exists():
                otp = send_otp_forgot(phone)
                print(phone, otp)
                if otp:
                    otp = str(otp)
                    count = 0
                    old = PhoneOTP.objects.filter(phone__iexact = phone)
                    if old.exists():
                        old = old.first()
                        k = old.count
                        if k > 10:
                            return Response({
                                'status' : False, 
                                'detail' : 'Maximum otp limits reached. Kindly support our customer care or try with different number'
                            })
                        old.count = k + 1
                        old.save()

                        return Response({'status': True, 'detail': 'OTP has been sent for password reset. Limits about to reach.'})
                    
                    else:
                        count = count + 1
               
                        PhoneOTP.objects.create(
                             phone =  phone, 
                             otp =   otp,
                             count = count,
                             forgot = True, 
        
                             )
                        return Response({'status': True, 'detail': 'OTP has been sent for password reset'})
                    
                else:
                    return Response({
                                    'status': 'False', 'detail' : "OTP sending error. Please try after some time."
                                })
            else:
                return Response({
                    'status' : False,
                    'detail' : 'Phone number not recognised. Kindly try a new account for this number'
                })
                

# class AddressListView(ModelViewSet):
#     queryset = AddressList.objects.all()
#     serializer_class = AddressListSerializer

class AddressListView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        address_qs = AddressList.objects.filter(user=request.user)
        address_serializer = AddressListSerializer(address_qs, many=True)
        return Response({'status': True, 'address': address_serializer.data})


    def post(self, request, *args, **kwargs):
        # user_id = request.data.get('username', None)
        # print(user_id)
        # title = request.data.get('title', None)
        # city = request.data.get('city', None)
        # country = request.data.get('country', None)
        # area = request.data.get('area', None)
        # pincode = request.data.get('pincode', None)
        # address1 = request.data.get('address1', None)
        # user = User.objects.get(phone=user_id)
        address_info_req = request.data 
        address_info_req['user'] = self.request.user.id
        # addrees_info = {'title': title, 'user': user.pk, 'city': city, 'country': country, 'area': area, 'pincode': pincode, 'address1': address1}
        address_serializer = AddressListSerializer(data=address_info_req)
        if address_serializer.is_valid():
            address_serializer.save()
            return Response({'status': True, 'message': 'Address saved successfully'})
        if address_serializer.errors:
            print(address_serializer.errors)
        return Response({'status': False, 'message': 'Unable to save address'})

    def put(self, request, *args, **kwargs):
        address_info = request.data
        user_id = self.request.user.id 
        address_info['user'] = user_id
        # user_id = request.data.get('username', None)
        id = request.data.get('id', None)
        # print(user_id)
        # title = request.data.get('title', None)
        # city = request.data.get('city', None)
        # country = request.data.get('country', None)
        # area = request.data.get('area', None)
        # pincode = request.data.get('pincode', None)
        # address1 = request.data.get('address1', None)
        # user = User.objects.get(phone=user_id)
        # addrees_info = {'user': user.pk, 'title': title, 'city': city, 'country': country, 'area': area, 'pincode': pincode, 'address1': address1}
        address_instance = AddressList.objects.get(user=user_id, id=id)
        address_serializer = AddressListSerializer(data=address_info, instance=address_instance)
        if address_serializer.is_valid():
            address_serializer.save()
            return Response({'status': True, 'message': 'Address updated successfully'})
        if address_serializer.errors:
            print(address_serializer.errors)
        return Response({'status': False, 'message': 'Unable to update address'})

    def delete(self, request, *args, **kwargs):
        user_id = request.user
        id = request.GET.get('id', None)
        # user = User.objects.get(phone=user_id)
        address_instance = AddressList.objects.get(user=user_id, id=id)
        address_instance.delete()
        address_instance = AddressList.objects.filter(user=user_id)
        address_serializer = AddressListSerializer(address_instance, many=True)
        return Response({'status': True, 'address': address_serializer.data})

# class ValidatePhoneSendOTP(APIView):
#     '''
#     This class view takes phone number and if it doesn't exists already then it sends otp for
#     first coming phone numbers'''

#     def post(self, request, *args, **kwargs):
#         phone_number = request.data.get('phone')
#         if phone_number:
#             phone = str(phone_number)
#             user = User.objects.filter(phone__iexact = phone)
#             if user.exists():
#                 return Response({'status': False, 'detail': 'Phone Number already exists'})
#                  # logic to send the otp and store the phone number and that otp in table. 
#             else:
#                 otp = send_otp(phone)
#                 print(phone, otp)
#                 if otp:
#                     otp = str(otp)
#                     count = 0
#                     old = PhoneOTP.objects.filter(phone__iexact = phone)
#                     if old.exists():
#                         count = old.first().count
#                         old.first().count = count + 1
#                         old.first().save()
                    
#                     else:
#                         count = count + 1
               
#                         PhoneOTP.objects.create(
#                              phone =  phone, 
#                              otp =   otp,
#                              count = count
        
#                              )
#                     if count > 7:
#                         return Response({
#                             'status' : False, 
#                              'detail' : 'Maximum otp limits reached. Kindly support our customer care or try with different number'
#                         })
                    
                    
#                 else:
#                     return Response({
#                                 'status': 'False', 'detail' : "OTP sending error. Please try after some time."
#                             })

#                 return Response({
#                     'status': True, 'detail': 'Otp has been sent successfully.'
#                 })
#         else:
#             return Response({
#                 'status': 'False', 'detail' : "I haven't received any phone number. Please do a POST request."
#             })


class ForgotValidateOTP(APIView):
    '''
    If you have received an otp, post a request with phone and that otp and you will be redirected to reset  the forgotted password
    
    '''

    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone', False)
        otp_sent   = request.data.get('otp', False)

        if phone and otp_sent:
            old = PhoneOTP.objects.filter(phone__iexact = phone)
            if old.exists():
                old = old.first()
                if old.forgot == False:
                    return Response({
                        'status' : False, 
                        'detail' : 'This phone havenot send valid otp for forgot password. Request a new otp or contact help centre.'
                     })
                    
                otp = old.otp
                if str(otp) == str(otp_sent):
                    old.forgot_logged = True
                    old.save()

                    return Response({
                        'status' : True, 
                        'detail' : 'OTP matched, kindly proceed to create new password'
                    })
                else:
                    return Response({
                        'status' : False, 
                        'detail' : 'OTP incorrect, please try again'
                    })
            else:
                return Response({
                    'status' : False,
                    'detail' : 'Phone not recognised. Kindly request a new otp with this number'
                })


        else:
            return Response({
                'status' : 'False',
                'detail' : 'Either phone or otp was not recieved in Post request'
            })


class ForgetPasswordChange(APIView):
    '''
    if forgot_logged is valid and account exists then only pass otp, phone and password to reset the password. All three should match.APIView
    '''

    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone', False)
        otp   = request.data.get("otp", False)
        password = request.data.get('password', False)

        if phone and otp and password:
            old = PhoneOTP.objects.filter(Q(phone__iexact = phone) & Q(otp__iexact = otp))
            if old.exists():
                old = old.first()
                if old.forgot_logged:
                    post_data = {
                        'phone' : phone,
                        'password' : password
                    }
                    user_obj = get_object_or_404(User, phone__iexact=phone)
                    serializer = ForgetPasswordSerializer(data = post_data)
                    serializer.is_valid(raise_exception = True)
                    if user_obj:
                        user_obj.set_password(serializer.data.get('password'))
                        user_obj.active = True
                        user_obj.save()
                        old.delete()
                        return Response({
                            'status' : True,
                            'detail' : 'Password changed successfully. Please Login'
                        })

                else:
                    return Response({
                'status' : False,
                'detail' : 'OTP Verification failed. Please try again in previous step'
                                 })

            else:
                return Response({
                'status' : False,
                'detail' : 'Phone and otp are not matching or a new phone has entered. Request a new otp in forgot password'
            })




        else:
            return Response({
                'status' : False,
                'detail' : 'Post request have parameters mising.'
            })

