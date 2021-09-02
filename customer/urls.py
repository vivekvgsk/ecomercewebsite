from django.urls import path
from .views import CustomerRegistrationView,SignInView,CustomerHome,ProductDetail,add_to_cart,MyCart,PlaceOrder,MyOrders,cancel_order,RemoveCartView,SignoutView,Products,CancelledOrders,ProductSearchView,LaptopFilterView,GamingpcFilterView,CpuCabinetFilterView,GraphicCardFilterView
from django.views.generic import TemplateView

urlpatterns = [
    path("signup",CustomerRegistrationView.as_view(),name="signup"),
     path("test",TemplateView.as_view(template_name="indexx.html"),name="test"),
    path("signin",SignInView.as_view(),name="signin"),
    path("signout",SignoutView.as_view(),name="signout"),
    path("home",CustomerHome.as_view(),name="home"),
    path("product/<int:pk>",ProductDetail.as_view(),name="productdetail"),
    path("addtocart/<int:id>",add_to_cart,name="addtocart"),
    path("cart",MyCart.as_view(),name="cart"),
    path("removecart/<int:pk>",RemoveCartView.as_view(),name="removecart"),
    path("order/<int:cid>/<int:id>",PlaceOrder.as_view(),name="order"),
    path("listorder",MyOrders.as_view(),name="myorders"),
    path("cancelorder<int:id>",cancel_order,name="ordercancel"),
    path("products",Products.as_view(),name="product"),
    path("cancelledorders",CancelledOrders.as_view(),name="cancelledorders"),
    path("search",ProductSearchView.as_view(),name="search"),
    path("listproducts",LaptopFilterView.as_view(),name="listproducts"),
    path("gaminspcs",GamingpcFilterView.as_view(),name="gaminspcs"),
    path("cpucabinets",CpuCabinetFilterView.as_view(),name="cpucabinets"),
    path("graphiccards",GraphicCardFilterView.as_view(),name="graphiccards")

    ]