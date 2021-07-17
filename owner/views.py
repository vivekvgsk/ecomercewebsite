from django.shortcuts import render,redirect
from .models import Item,Product
from .forms import ItemCreateForm,ProductCreateForm
from django.views.generic import TemplateView,CreateView,ListView,UpdateView,DeleteView,DetailView
from django.urls import reverse_lazy
# Create your views here.
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

class ItemCategoryListView(ListView):
    model=Item
    template_name="categorylist.html"
    context_object_name = "items"

class GetObjectMixin:
    def get_obect(self,id):
        return self.model.objects.get(id=id)

class ItemCategoryEditView(UpdateView):
    model=Item
    template_name="categoryupdate.html"
    form_class = ItemCreateForm
    success_url = reverse_lazy("listitems")

class CategoryRemoveView(DeleteView):
    model = Item
    template_name = "categorydelete.html"
    form_class = ItemCreateForm
    context_object_name="item"
    success_url = reverse_lazy("listitems")


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

class ProductListView(ListView):
    model=Product
    template_name="productlist.html"
    context_object_name = "products"

class ProductEditView(UpdateView):
    model = Product
    template_name = "productupdate.html"
    form_class = ProductCreateForm
    success_url = reverse_lazy("products")

class ProductRemoveView(DeleteView):
    model = Product
    template_name = "productdelete.html"
    context_object_name="product"
    success_url = reverse_lazy("products")