from django.shortcuts import render,redirect
from .forms import CustomerRegistrationForm,LoginForm,PlaceOrderForm
from django.views.generic import TemplateView,CreateView,ListView,UpdateView,DeleteView,DetailView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from owner.models import Product,Cart,Orders,Item
from django.db.models import Sum
from django.core.mail import send_mail
from django.db.models import Q
from .filters import ProductFilter
from django.utils.decorators import method_decorator
from .decorators import loginrequired

from django.conf import settings

# Create your views here.
class CustomerRegistrationView(CreateView):
    model = User
    form_class = CustomerRegistrationForm
    template_name = "register.html"
    success_url = reverse_lazy("signin")

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

class SignoutView(TemplateView):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("signin")

@method_decorator(loginrequired,name="dispatch")
class CustomerHome(TemplateView):
    context = {}
    template_name = "userhome.html"
    def get(self,request,*args,**kwargs):
        cnt = Cart.objects.filter(user=request.user, status="Ordernotplaced").count()
        products=Product.objects.all()
        self.context={
            "products":products,
            "cnt":cnt
        }
        # self.context["products"]=products

        return render(request,self.template_name,self.context)

@method_decorator(loginrequired,name="dispatch")
class ProductDetail(DetailView):
    model=Product
    template_name="productdetail.html"
    context_object_name = "product"

def get_object(id):
    return Product.objects.get(id=id)

@loginrequired
def add_to_cart(request,*args,**kwargs):
    pid = kwargs.get("id")
    product = get_object(pid)
    cart = Cart(product=product, user=request.user)  # ORM query for adding an element to a model(here Cart)
    cart.save()
    return redirect("cart")

@method_decorator(loginrequired,name="dispatch")
class RemoveCartView(DeleteView):
    model=Cart
    template_name = "removecart.html"
    success_url=reverse_lazy("cart")

@method_decorator(loginrequired,name="dispatch")
class MyCart(TemplateView):
    model=Cart
    template_name = "mycart.html"
    context={}
    def get(self,request,*args,**kwargs):
        cart_items=self.model.objects.filter(user=request.user,status="Ordernotplaced")
        products = Product.objects.all()
        total = Cart.objects.filter(status='Ordernotplaced', user=request.user).aggregate(Sum('product__price'))
        cnt = Cart.objects.filter(user=request.user, status="Ordernotplaced").count()

        self.context={
            "cart_items":cart_items,
            "total":total.get("product__price__sum"),
            "cnt":cnt,
            "products":products
        }
        return render(request, self.template_name, self.context)

# class PlaceOrder(TemplateView):
#     model=Cart
#     template_name = "placeorder.html"
#     context={}
#     form_class=PlaceOrderForm
#     def get(self,request,*args,**kwargs):
#         pid=kwargs.get("id")
#         product=Product.objects.get(id=pid)
#         self.context={
#             "form":self.form_class(initial={"product":product.product_name})
#         }
#         return render(request, self.template_name, self.context)
#     def post(self,request,*args,**kwargs):
#         pid = kwargs.get("id")
#         product = Product.objects.get(id=pid)
#         cid=kwargs.get("id")
#         cart=self.model.objects.get(id=cid)
#         form=self.form_class(request.POST)
#         if form.is_valid():
#             address=form.cleaned_data.get("address")
#             email = request.user.email
#             print(email)
#
#             product=product
#             order=Orders(address=address,product=product,user=request.user)
#             order.save()
#             cart.status="oredrplaced"
#             cart.save()
#
#             send_mail(
#                 'Order Confirmation',
#                 'you sucessfully orderd the item.',
#                 'vivekvgsk@gmail.com',
#                 [email],
#                 fail_silently=False,
#             )
#             return redirect("myorders")
#         return render(request, self.template_name, self.context)

@method_decorator(loginrequired,name="dispatch")
class MyOrders(TemplateView):
    model=Orders
    template_name = "myorders.html"
    context={}
    def get(self,request,*args,**kwargs):

        order_items=self.model.objects.filter(Q(user=request.user) & Q(status="ordered") | Q(status="packed") | Q(status="shipped"))
        cnt = Cart.objects.filter(user=request.user, status="Ordernotplaced").count()
        self.context={
            "order_items":order_items,
            "cnt":cnt
        }
        return render(request, self.template_name, self.context)

@loginrequired
def cancel_order(request,*args,**kwargs):
    pid=kwargs.get("id")
    product=Orders.objects.get(id=pid)
    print(product)
    product.status="cancelled"
    product.save()
    return redirect("myorders")

@method_decorator(loginrequired,name="dispatch")
class PlaceOrder(TemplateView):
    model=Cart
    template_name = "placeorder.html"
    context={}
    form_class=PlaceOrderForm
    def get(self,request,*args,**kwargs):
        pid=kwargs.get("id")
        product=Product.objects.get(id=pid)
        cnt = Cart.objects.filter(user=request.user, status="Ordernotplaced").count()
        self.context={
            "form":self.form_class(initial={"product":product.product_name}),
            "cnt":cnt
        }
        return render(request, self.template_name, self.context)
    def post(self,request,*args,**kwargs):
        pid = kwargs.get("id")
        product = Product.objects.get(id=pid)
        cid=kwargs.get("cid")
        cart=self.model.objects.get(id=cid)
        form=self.form_class(request.POST)
        if form.is_valid():
            address=form.cleaned_data.get("address")
            email = request.user.email
            print(email)

            product=product
            order=Orders(address=address,product=product,user=request.user)
            order.save()
            cart.status="oredrplaced"
            cart.save()
            msg="you have successfully ordered" + product.product_name + "worth Rs:"+ str(product.price)
            send_mail(
                'Order Confirmation',
                msg,
                'vivekvgsk@gmail.com',
                [email],
                fail_silently=False,
            )
            return redirect("myorders")
        return render(request, self.template_name, self.context)

class Products(TemplateView):
    context = {}
    template_name = "products.html"
    def get(self,request,*args,**kwargs):

        products=Product.objects.all()
        self.context={
            "products":products

        }
        # self.context["products"]=products

        return render(request,self.template_name,self.context)

@method_decorator(loginrequired,name="dispatch")
class CancelledOrders(TemplateView):
    model=Orders
    template_name = "cancelledorders.html"
    context={}
    def get(self,request,*args,**kwargs):
        cancelled_items=self.model.objects.filter(user=request.user,status="cancelled")
        cnt = Cart.objects.filter(user=request.user, status="Ordernotplaced").count()
        self.context={
            "cancelled_items":cancelled_items,
            "cnt":cnt
        }
        return render(request, self.template_name, self.context)

class ProductSearchView(TemplateView):
    def get(self,request,*args,**kwargs):

        search=request.GET.get('search')
        print(search)

        product=Product.objects.filter((Q(product_name__icontains=search) | Q(price__icontains=search)))
        product_filter=ProductFilter(request.GET,queryset=product)
        return render(request,"searchresult.html",{"filter":product_filter})



class LaptopFilterView(TemplateView):
    model=Product
    template_name = "filterproducts.html"
    context={}
    def get(self,request,*args,**kwargs):
        # list_items=request.GET.get("listitems")
        # print(list_items)
        laptops=self.model.objects.filter(category__product_category="LAPTOP")
        cnt = Cart.objects.filter(user=request.user, status="Ordernotplaced").count()


        self.context={
            "laptops":laptops,
            "cnt":cnt

        }

        return render(request, self.template_name, self.context)

class GamingpcFilterView(TemplateView):
    model=Product
    template_name = "filterproducts.html"
    context={}
    def get(self,request,*args,**kwargs):
        # list_items=request.GET.get("listitems")
        # print(list_items)

        gpcs = self.model.objects.filter(category__product_category="GAMING PC")
        cnt = Cart.objects.filter(user=request.user, status="Ordernotplaced").count()
        self.context={

            "gpcs":gpcs,
            "cnt":cnt
        }

        return render(request, self.template_name, self.context)

class CpuCabinetFilterView(TemplateView):
    model=Product
    template_name = "filterproducts.html"
    context={}
    def get(self,request,*args,**kwargs):
        # list_items=request.GET.get("listitems")
        # print(list_items)

        cpus = self.model.objects.filter(category__product_category="CPU CABINET")
        cnt = Cart.objects.filter(user=request.user, status="Ordernotplaced").count()
        self.context={

            "cpus":cpus,
            "cnt":cnt
        }

        return render(request, self.template_name, self.context)

class GraphicCardFilterView(TemplateView):
    model=Product
    template_name = "filterproducts.html"
    context={}
    def get(self,request,*args,**kwargs):
        # list_items=request.GET.get("listitems")
        # print(list_items)

        gcs = self.model.objects.filter(category__product_category="GRAPHIC CARD")
        cnt = Cart.objects.filter(user=request.user, status="Ordernotplaced").count()
        self.context={

            "gcs":gcs,
            "cnt":cnt
        }

        return render(request, self.template_name, self.context)


















