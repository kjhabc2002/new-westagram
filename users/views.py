import re
import jwt
import json
import bcrypt

from django.views     import View
from django.http      import JsonResponse

from .models          import User
from my_settings      import SECRET_KEY, ALGORITHM

class SignUpView(View):
    def post(self, request):
        try:
            data      = json.loads(request.body)
            email_reg = r"[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?"
            regex     = re.compile(email_reg)

            if len(data['password']) < 8 or not regex.match(data['email']):
                return JsonResponse({'message':'INVALID_FORMAT'}, status=400)
            if User.objects.filter(email=data['email']).exists():
                return JsonResponse({'message':'USER_ALREADY_EXIST'}, status=400)

            User(
                email    = data['email'],
                password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
                name     = data.get('name'),
                phone    = data.get('phone'),
                account  = data.get('account'),
            ).save()

            return JsonResponse({'message':'SUCCESS'}, status=201)            
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

class SignInView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            if not User.objects.filter(email=data['email']).exists():
                return JsonResponse({'message':'USER_DOES_NOT_EXIST'}, status=404)

            user = User.objects.get(email=data['email'])

            if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                token = jwt.encode({'id': user.id}, SECRET_KEY, algorithm=ALGORITHM)
                return JsonResponse({'token':token}, status=200)

            return JsonResponse({'message':'INVALID_PASSWORD'}, status=401)
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)