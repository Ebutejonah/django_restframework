from django.shortcuts import render, redirect
from rest_framework.views import APIView #class based view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from core.serializers import StudentSerializer, AdvocateSerializer
from core.models import Student, Advocate
from rest_framework.authtoken.models import Token
from django.contrib import messages
from django.contrib.auth.models import User
from rest_framework.decorators import api_view #function based view
from django.db.models import Q #for querying the database


@api_view(['GET', "POST"])
def advocate_list(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        print('Query:', query)
        if query == None:
            query = ''
        searched = Advocate.objects.filter(Q(username__icontains=query) | Q(bio__icontains=query))
        #advocate = Advocate.objects.all()
        serializers = AdvocateSerializer(searched, many=True)
        return Response(serializers.data)
    if request.method == 'POST':
        advocate=Advocate.objects.create(
            username = request.data['username'],
            bio = request.data['bio']
            )
        serializer = AdvocateSerializer(advocate, many=False)
        return Response(serializer.data)
    

@api_view(['GET', 'PUT', 'DELETE'])
def advocate(request,username):
    advocate = Advocate.objects.get(username=username)
    if request.method == 'GET':
        serializer = AdvocateSerializer(advocate, many=False)
        return Response(serializer.data)
    if request.method == 'PUT':
        advocate.username = request.data['username']
        advocate.bio = request.data['bio']
        advocate.save()
        serializer = AdvocateSerializer(advocate, many=False)
        return Response(serializer.data)
    if request.method == 'DELETE':
        advocate.delete()
        all_advocate = Advocate.objects.all()
        serializer = AdvocateSerializer(all_advocate, many=True)
        return Response(serializer.data)
    


class FirstView(APIView):
    permission_classes = (IsAuthenticated, )
    def get(self,request,*args,**kwargs):
        qs = Student.objects.all()
        serializer = StudentSerializer(qs, many=True)
        return Response(serializer.data)
    
    def post(self,request,*args,**kwargs):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    

def signup(request):
    if request.method == 'POST':
        username = request.POST['name']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Name already in use')
                return redirect('/')
            elif len(password1) < 8:
                messages.info(request, 'Password must have at least 8 characters')
                return redirect('/')
            else:
                new_user=User.objects.create_user(username=username, password=password1)
                user_model = User.objects.get(username = new_user.username)
                new_student = Student.objects.create(user=user_model,username=user_model.username,id_user=user_model.id)
                new_student.save()
                new_token = Token.objects.create(user=user_model)
                new_token.save()
                messages.info(request,'User created successfully')
                return redirect('/')
        else:
            messages.info(request, 'Passwords must match')
            return redirect('/')
    else:
        return render(request,'index.html')
