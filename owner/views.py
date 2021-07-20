from django.shortcuts import render,redirect
from .models import Item,Product,Orders
from .forms import ItemCreateForm,ProductCreateForm,StatusUpdateForm
from django.views.generic import TemplateView,CreateView,ListView,UpdateView,DeleteView,DetailView
from django.urls import reverse_lazy
from customer.forms import LoginForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.db.models import Q
from .decorators import loginrequired
from django.utils.decorators import method_decorator
# Create your views here.


class LogInView(TemplateView):

    form_class=LoginForm
    template_name="signin.html"
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
                return redirect("listitems")
            else:
                messages.error(request, "Invalid User")
                return render(request, self.template_name, self.context)

        return render(request, self.template_name, self.context)

class LogoutView(TemplateView):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("login")

@method_decorator(loginrequired,name="dispatch")
class ItemCreateView(CreateView):
    model=Item
    form_class = ItemCreateForm
    template_name = "itemcreate.html"
    context={}
    def get(self,request,*args,**kwargs):
        form=self.form_class()
        self.context["form"]=form
        return render(request,self.template_name,self.context)
    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            form.save()
            print("success")
            return redirect('listitems')
        return render(request, self.template_name, self.context)

@method_decorator(loginrequired,name="dispatch")
class ItemCategoryListView(ListView):
    model=Item
    template_name="categorylist.html"
    context_object_name = "items"

class GetObjectMixin:
    def get_obect(self,id):
        return self.model.objects.get(id=id)

@method_decorator(loginrequired,name="dispatch")
class ItemCategoryEditView(UpdateView):
    model=Item
    template_name="categoryupdate.html"
    form_class = ItemCreateForm
    success_url = reverse_lazy("listitems")

@method_decorator(loginrequired,name="dispatch")
class CategoryRemoveView(DeleteView):
    model = Item
    template_name = "categorydelete.html"
    form_class = ItemCreateForm
    context_object_name="item"
    success_url = reverse_lazy("listitems")

@method_decorator(loginrequired,name="dispatch")
class ProductCreateView(CreateView):
    model=Product
    form_class = ProductCreateForm
    template_name = "productcreate.html"
    context={}
    def get(self,request,*args,**kwargs):
        form=self.form_class()
        self.context["form"]=form
        return render(request,self.template_name,self.context)
    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST,files=request.FILES)
        if form.is_valid():
            form.save()
            print("success")
            return redirect('products')
        return render(request, self.template_name, self.context)

@method_decorator(loginrequired,name="dispatch")
class ProductListView(ListView):
    model=Product
    template_name="productlist.html"
    context_object_name = "products"

@method_decorator(loginrequired,name="dispatch")
class ProductEditView(UpdateView):
    model = Product
    template_name = "productupdate.html"
    form_class = ProductCreateForm
    success_url = reverse_lazy("products")

@method_decorator(loginrequired,name="dispatch")
class ProductRemoveView(DeleteView):
    model = Product
    template_name = "productdelete.html"
    context_object_name="product"
    success_url = reverse_lazy("products")

@method_decorator(loginrequired,name="dispatch")
class ViewCustomerOrders(TemplateView):
    model=Orders
    template_name = "vieworders.html"
    context={}
    def get(self,request,*args,**kwargs):
        orders=self.model.objects.filter(Q(status="ordered")|Q(status="packed")|Q(status="shipped"))
        self.context["orders"]=orders
        return render(request, self.template_name, self.context)

@method_decorator(loginrequired,name="dispatch")
class StatusUpdateView(UpdateView):
    model=Orders
    form_class=StatusUpdateForm
    template_name = "status.html"
    success_url = reverse_lazy("orders")


