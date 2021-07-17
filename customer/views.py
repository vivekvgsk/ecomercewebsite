from django.shortcuts import render,redirect
from .forms import CustomerRegistrationForm,LoginForm,PlaceOrderForm
from django.views.generic import TemplateView,CreateView,ListView,UpdateView,DeleteView,DetailView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from owner.models import Product,Cart,Orders
from django.db.models import Sum

# Create your views here.
class CustomerRegistrationView(CreateView):
    model = User
    form_class = CustomerRegistrationForm
    template_name = "register.html"

class SignInView(TemplateView):
    model=User
    form_class=LoginForm
    template_name="login.html"
    context={}
    def get(self,request,*args,**kwargs):
        form=self.form_class()
        self.context["form"]=form
        return render(request,self.template_name,self.context)
    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get("username")
            password=form.cleaned_data.get("password")
            user=authenticate(request,username=username,password=password)
            if user:
                login(request,user)
                return redirect("home")
            else:
                messages.error(request, "Invalid User")
                return render(request, self.template_name, self.context)

        return render(request, self.template_name, self.context)

class CustomerHome(TemplateView):
    context = {}
    template_name = "userhome.html"
    def get(self,request,*args,**kwargs):

        products=Product.objects.all()
        self.context["products"]=products
        return render(request,self.template_name,self.context)

class ProductDetail(DetailView):
    model=Product
    template_name="productdetail.html"
    context_object_name = "product"

def get_object(id):
    return Product.objects.get(id=id)

def add_to_cart(request,*args,**kwargs):
    pid = kwargs.get("id")
    product = get_object(pid)
    cart = Cart(product=product, user=request.user)  # ORM query for adding an element to a model(here Cart)
    cart.save()
    return redirect("cart")

class MyCart(TemplateView):
    model=Cart
    template_name = "mycart.html"
    context={}
    def get(self,request,*args,**kwargs):
        cart_items=self.model.objects.filter(user=request.user,status="Ordernotplaced")
        total = Cart.objects.filter(status='Ordernotplaced', user=request.user).aggregate(Sum('product__price'))
        cnt = Cart.objects.filter(user=request.user, status="Ordernotplaced").count()

        self.context={
            "cart_items":cart_items,
            "total":total.get("product__price__sum"),
            "cnt":cnt
        }
        return render(request, self.template_name, self.context)

class PlaceOrder(TemplateView):
    model=Cart
    template_name = "placeorder.html"
    context={}
    form_class=PlaceOrderForm
    def get(self,request,*args,**kwargs):
        pid=kwargs.get("id")
        product=Product.objects.get(id=pid)
        self.context={
            "form":self.form_class(initial={"product":product.product_name})
        }
        return render(request, self.template_name, self.context)
    def post(self,request,*args,**kwargs):
        pid = kwargs.get("id")
        product = Product.objects.get(id=pid)
        cid=kwargs.get("id")
        cart=self.model.objects.get(id=cid)
        form=self.form_class(request.POST)
        if form.is_valid():
            address=form.cleaned_data.get("address")
            product=product
            order=Orders(address=address,product=product,user=request.user)
            order.save()
            cart.status="oredrplaced"
            cart.save()
            return redirect("login")
        return render(request, self.template_name, self.context)

class MyOrders(TemplateView):
    model=Orders
    template_name = "myorders.html"
    context={}
    def get(self,request,*args,**kwargs):
        order_items=self.model.objects.filter(user=request.user)
        self.context["order_items"]=order_items
        return render(request, self.template_name, self.context)

def cancel_order(request,*args,**kwargs):
    pid=kwargs.get("id")
    product=Cart.objects.get(id=pid)
    print(product)
    product.status="cancelled"
    product.save()
    return redirect("myorders")

















