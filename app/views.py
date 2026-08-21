import random

from django.contrib.auth import login
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect

from app.models import Product, Usermodel
from app.utils import generate_code, send_register_email


# Create your views here.

def index(request):
    return  render(request, "app/index.html")

def mahsulot(request):
    products = Product.objects.all()
    query = request.GET.get("qidir")
    if query:
        products = products.filter(Q(name__icontains=query) | Q(category__icontains=query))

    sort_option = request.GET.get("sort")
    if sort_option == 'low_price':
        products = products.order_by("price")
    elif sort_option == 'high_price':
        products = products.order_by("-price")
    context = {'products': products}
    return render(request, "app/mahsulotlar.html", context)

def blog(request):
    return render(request, "app/blog.html")

def about(request):
    return render(request, "app/biz-haqimizda.html")

def contact(request):
    return render(request, "app/aloqa.html")

def login_page(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = Usermodel.objects.filter(email=email).first()
        if not user:
            return render(request, "app/register.html", {"error" : "email does not exist"})

        login(request, user)

        return redirect('index')
    return render(request, "app/login.html")

def register_page(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")
        if int(password) != int(password2):
            return render(request, "app/register.html", {"error" : "passwords didn't match"})
        if Usermodel.objects.filter(name=name).exists():
            return render(request, "app/register.html", {"error" : "name already exists"})


        user = Usermodel.objects.create(name=name, email=email, password=password)

        code = generate_code()

        request.session["verify_user_id"] = user.id
        request.session["verify_code"] = str(code)

        send_register_email(to_email=user.email, code=code)

        return redirect('c')

    return render(request, "app/register.html")

def svat(request):
    return render(request, "app/savatcha.html")

def mahsulot_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

    context = {
        'product': product
    }
    return render(request, "app/mahsulot-detail.html", context)

def c_p(request):
    if request.POST.get('code') ==request.session.get('verify_code'):
        return redirect('login')
    user = Usermodel.objects.get(id=request.session.get('verify_user_id'))
    user.is_active = True
    request.session.pop('verify_code', None)
    request.session.pop('verify_user_id', None)
    return render(request, "app/confirm-password.html")

def f_p(request):
    if request.method == 'POST':
        email2 = request.POST.get("email2")
        user = Usermodel.objects.filter(email=email2).first()

        code = generate_code()

        request.session["verify_user_id"] = user.id
        request.session["verify_code"] = str(code)

        send_register_email(to_email=user.email, code=code)

        return redirect('r')
    return render(request, "app/forgot-password.html")

def r_p(request):
    if request.POST.get('code') ==request.session.get('verify_code'):
        return redirect('login')
    user = Usermodel.objects.get(id=request.session.get('verify_user_id'))
    user.is_active = True
    request.session.pop('verify_code', None)
    request.session.pop('verify_user_id', None)

    if request.method == "POST":
        password_new = request.POST.get("password_new")
        Usermodel.objects.filter(password=password_new).first()

        return redirect('login')
    return render(request, "app/reset-password.html")

# def users_info(request, pk):
#     user = get_object_or_404(Users, id=pk)
#     context = {'user': user }
#     return render(request, "app/users_info.html", context)