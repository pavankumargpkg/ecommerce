import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .models import *

##used csrf_exempt to use on the local tunnel

# @csrf_exempt
# def loginPage(request):
#     page = "login"

#     if request.user.is_authenticated:
#         return redirect("store")

#     if request.method == "POST":
#         username = request.POST.get("username").lower()
#         password = request.POST.get("password")

#         try:
#             user = User.objects.get(username=username)
#         except:
#             messages.error(request, "User does not exist")

#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             login(request, user)
#             return redirect("store")

#         else:
#             messages.error(request, "Username or email is incorrect")

#     context = {"page": page}
#     return render(request, "store/login_register.html", context)
class loginPage(View):
    page = "login"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("store")
        context = {"page": self.page}
        return render(request, "store/login_register.html", context)

    def post(self, request):
        username = request.POST.get("username").lower()
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("store")

        else:
            messages.error(request, "Username or email is incorrect")

        context = {"page": self.page}
        return render(request, "store/login_register.html", context)

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(loginPage, self).dispatch(*args, **kwargs)


# def logoutUser(request):
#     logout(request)
#     return redirect("store")


class logoutUser(View):
    def get(self, request):
        logout(request)
        return redirect("store")


# @csrf_exempt
# def registerPage(request):
#     form = UserCreationForm()

#     if request.method == "POST":
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.username = user.username.lower()
#             user.save()
#             customer = Customer.objects.create(
#                 user=user, name=user.username, email=request.POST.get("email").lower
#             )
#             login(request, user)
#             return redirect("store")
#         else:
#             messages.error(request, "An error occured during registration")

#     context = {"form": form}
#     return render(request, "store/login_register.html", context)

def search_view(request):
    query = request.GET.get('q')
    results = []

    if query:
        # Perform search query using the query string
        results = Product.objects.filter(name__icontains=query)

    context = {
        'query': query,
        'results': results
    }

    return render(request, 'store/search_results.html', context)

class registerPage(View):
    form = UserCreationForm()

    def get(self, request):
        context = {"form": self.form}
        return render(request, "store/login_register.html", context)

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            Customer.objects.create(
                user=user, name=user.username, email=request.POST.get("email").lower
            )
            login(request, user)
            return redirect("store")
        else:
            messages.error(request, "An error occured during registration")

        context = {"form": self.form}
        return render(request, "store/login_register.html", context)

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(registerPage, self).dispatch(*args, **kwargs)


def store(request):
    products = Product.objects.all()

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        context = {
            "products": products,
            "order": order,
        }
    else:
        context = {
            "products": products,
        }
    return render(request, "store/store.html", context)


@login_required(login_url="login")
def cart(request):

    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    items = order.orderitem_set.all()

    context = {
        "items": items,
        "order": order,
    }
    return render(request, "store/cart.html", context)


@csrf_exempt
@login_required(login_url="login")
def checkout(request):

    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    items = order.orderitem_set.all()

    if request.method == "POST":
        order.transaction_id = datetime.datetime.now().timestamp()
        order.complete = True
        order.save()
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=request.POST.get("address"),
            city=request.POST.get("city"),
            state=request.POST.get("state"),
            zip_code=request.POST.get("zipcode"),
        )
        messages.success(request, "Your order has been successfully completed!")
        return redirect("store")

    context = {
        "items": items,
        "order": order,
    }
    return render(request, "store/checkout.html", context)


@login_required(login_url="login")
def addItem(request, pk):
    customer = request.user.customer
    product = Product.objects.get(id=pk)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    orderItem.quantity = orderItem.quantity + 1

    orderItem.save()

    messages.success(request, "Your Item is successfully added!")
    return redirect(request.META["HTTP_REFERER"])


@login_required(login_url="login")
def removeItem(request, pk):
    customer = request.user.customer
    product = Product.objects.get(id=pk)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    orderItem.quantity = orderItem.quantity - 1

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    messages.success(request, "Your Item has been removed successfully!")
    return redirect(request.META["HTTP_REFERER"])

