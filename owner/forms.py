from django import forms
from .models import Item,Product,Orders

class ItemCreateForm(forms.ModelForm):
    class Meta:
        model=Item
        fields=["product_category"]

class ProductCreateForm(forms.ModelForm):
    class Meta:
        model=Product
        fields="__all__"
        widgets={
            "product_name":forms.TextInput(attrs={"class":"form-control"}),
            "price": forms.TextInput(attrs={"class": "form-control"}),
            "specs": forms.Textarea(attrs={"class": "form-control"})
        }
    def clean(self):
        cleaned_data=super().clean()
        price=cleaned_data.get("price")
        if price<10:
            msg="invalid price"
            self.add_error("price",msg)

class StatusUpdateForm(forms.ModelForm):
    class Meta:
        model=Orders
        fields=["product","status"]



