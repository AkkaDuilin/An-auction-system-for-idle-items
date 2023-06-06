from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from .models import CartInfo
from user_part.decorator import login as user_login

# Create your views here.

