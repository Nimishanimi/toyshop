from django .urls import path
from . import views

  
urlpatterns = [
 path('', views.index),
 path('about/', views.about),
 path('contact/', views.contact),
 path('register/', views.register),
 path('saveupdate/', views.saveupdate),
 path('login/', views.login),
 path('logout/', views.logout),
 path('product/', views.product),
 path('single/', views.single),
 path('payment/', views.payment),
 path('checkout/', views.checkout),
 path('cart/', views.cart),
 path('addcart/', views.addcart),
 path('cartupdate/', views.cartupdate),
 path('additem/', views.additem),
 path('demo/', views.demo),

 







##########################################################################################################################################
#################################################ADMIN####################################################################################
 path('adminindex/',views.admin_index),
 path('adminlogin/',views.admin_login),
 path('adminlogout/',views.admin_logout),
 path('inbox_details/',views.inbox_details),
 path('inbox/',views.inbox),
 path('edit/',views.edit),
 path('delete/',views.delete),
 path('toysave/',views.toysave),
 path('signup/',views.signup),
 path('forgetpassword/',views.forgetpassword),
 path('resetpassword/',views.reset),
 path('ajaxnew/',views.signup),
 path('view/',views.view),
 path('admregtable/', views.admregtable),
 path('pdf/', views.pdf),





 

]