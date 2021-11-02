from .models import *
from .serializers import *

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import jwt

# Create your views here.
@api_view(['POST'])
def create_advisor(request):
    serializer = AdvisorSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def register_user(request):
    serializer = UserSerializers(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        # return Response(serializer.data, status=status.HTTP_200_OK)

        token = user.token
        data = {'id' : user.id, 'token' : token}

        response = Response()
        response.set_cookie(key='token', value=token, httponly=True)
        response.data = data
        response.status_code = status.HTTP_200_OK

        return response
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login_view(request):
    email = request.data['email']
    password = request.data['password']

    if email is None or password is None:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.get(email=email)

    if user is None:
        return Response('User Not Found!', status=status.HTTP_400_BAD_REQUEST)

    if not user.check_password(password):
        return Response('Incorrect Password!', status=status.HTTP_401_UNAUTHORIZED)

    response = Response()
    
    token = request.COOKIES.get('token')

    if token is None:
        token = user.token
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])

        if int(user.id) != int(payload['id']):
            response.delete_cookie('token')

    except jwt.ExpiredSignatureError:
        token = user.token

    data = {'id' : user.id, 'token' : token}

    # response = Response()
    response.set_cookie(key='token', value=token, httponly=True)
    response.data = data
    response.status_code = status.HTTP_200_OK

    return response


@api_view(['POST'])
def logout_view(request):
    response = Response()
    response.delete_cookie('token')
    response.status_code = status.HTTP_200_OK
    return response


@api_view(['GET'])
def advisor_list(request, user_id):
    token = request.COOKIES.get('token')

    if not token:
        return Response('Your token is invalid,login', status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return Response('Your token is expired,login', status=status.HTTP_401_UNAUTHORIZED)
    
    if int(user_id) == int(payload['id']):
        advisors = Advisor.objects.all()
        serializer = AdvisorSerializer(advisors, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def book_call(request, user_id, advisor_id):
    token = request.COOKIES.get('token')

    if not token:
        return Response('Your token is invalid,login', status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return Response('Your token is expired,login', status=status.HTTP_401_UNAUTHORIZED)
    
    if int(user_id) == int(payload['id']):
        user = User.objects.get(id=user_id)
        advisor = Advisor.objects.get(id=advisor_id)

        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user, advisor=advisor)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def booking_list(request, user_id):
    token = request.COOKIES.get('token')

    if not token:
        return Response('Your token is invalid,login', status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return Response('Your token is expired,login', status=status.HTTP_401_UNAUTHORIZED)
    
    if int(user_id) == int(payload['id']):
        all_booking = Booking.objects.filter(user_id=user_id)
        serializer = ShowBookingSerializer(all_booking, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response(status=status.HTTP_401_UNAUTHORIZED)



@api_view(['GET'])
def user_list(request):
    token = request.COOKIES.get('token')

    if not token:
        return Response('Your token is invalid,login', status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return Response('Your token is expired,login', status=status.HTTP_401_UNAUTHORIZED)
    users_list = User.objects.all()
    serializer = UserSerializers(users_list, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def current_user(request):
    token = request.COOKIES.get('token')
    
    if not token:
        return Response('Your token is invalid,login', status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return Response('Your token is expired,login', status=status.HTTP_401_UNAUTHORIZED)

    user = User.objects.get(id=payload['id'])
    serializer = UserSerializers(user)
    return Response(serializer.data, status=status.HTTP_200_OK)

