
from django.urls import path
from .views import ItemCreateView,ItemCategoryListView,ItemCategoryEditView,CategoryRemoveView,ProductCreateView,ProductListView,ProductEditView,ProductRemoveView

urlpatterns = [
    path('additem',ItemCreateView.as_view(),name="additem"),
    path('items',ItemCategoryListView.as_view(),name="listitems"),
    path('items/<int:pk>',ItemCategoryEditView.as_view(),name="updatecategory"),
    path("itemremove/<int:pk>",CategoryRemoveView.as_view(),name="removecategory"),
    path("addproduct",ProductCreateView.as_view(),name="addproduct"),
    path("products",ProductListView.as_view(),name="products"),
    path("product/<int:pk>",ProductEditView.as_view(),name="updateproduct"),
    path("productremove/<int:pk>",ProductRemoveView.as_view(),name="removeproduct")
    ]
