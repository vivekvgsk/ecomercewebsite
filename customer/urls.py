from django.urls import path
from .views import CustomerRegistrationView,SignInView,CustomerHome,ProductDetail,add_to_cart,MyCart,PlaceOrder,MyOrders,cancel_order,RemoveCartView,SignoutView
from django.views.generic import TemplateView

urlpatterns = [
    path("signup",CustomerRegistrationView.as_view(),name="signup"),
    path("login",TemplateView.as_view(template_name="signin.html"),name="login"),
    path("signin",SignInView.as_view(),name="signin"),
    path("signout",SignoutView.as_view(),name="signout"),
    path("home",CustomerHome.as_view(),name="home"),
    path("product/<int:pk>",ProductDetail.as_view(),name="productdetail"),
    path("addtocart/<int:id>",add_to_cart,name="addtocart"),
    path("cart",MyCart.as_view(),name="cart"),
    path("removecart/<int:pk>",RemoveCartView.as_view(),name="removecart"),
    path("order/<int:cid>/<int:id>",PlaceOrder.as_view(),name="order"),
    path("listorder",MyOrders.as_view(),name="myorders"),
    path("cancelorder<int:id>",cancel_order,name="ordercancel")

    ]