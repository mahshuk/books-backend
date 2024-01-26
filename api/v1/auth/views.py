import json
import requests


from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import AllowAny

from django.contrib.auth.models import User 

@permission_classes([AllowAny])
@api_view(["POST"])
def create(request):

    email = request.data["email"]
    name = request.data["name"]
    password = request.data["password"]
    

    if not User.objects.filter(username=email).exists():
        User.objects.create_user(
            username = email,
            first_name = name,
            password = password
        )
        

        headers= {
            "Content-Type" : "application/json"
        }
        


        protocol = "http://"
        if request.is_secure():
            protocol = "https://"

        host = request.get_host()

        url = protocol + host + "/api/v1/auth/token/"

        data = {
            "username" : email,
            "password" : password,
        }

        response = requests.post(url,headers=headers,data=json.dumps(data))

        if response.status_code==200:
            response_data = {
                "status_code" : 6000,
                "data" : response.json(),
                "message"  : "account created"
                }
            return Response(response_data)
        else:
            response_data = {
                "status_code" : 6001,
                "message" : "an error occured"
                }
            return Response(response_data)
    else : 
        response_data = {
            "status_code" : 6001,
            "message"  : "user already exists"
            }
        return Response(response_data)