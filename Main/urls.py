from django.urls import path
from Main import views
from django.conf import settings
from django.conf.urls.static import static
from .views import ProductView, ProductDetailView, CustomerRegistrationView, ProfileView, plus_cart
from django.contrib.auth import views as auth_views
from .forms import LoginForm, MyPasswordResetForm, MyPschangeForm, MySetPasswordForm

urlpatterns = [
                  path('', ProductView.as_view(), name='home'),
                  path('product-detail/<int:pk>', ProductDetailView.as_view(), name='product-detail'),
                  # path('additem/',AddItemView.as_view(),name='additem'),
                  path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
                  path('cart/', views.show_cart, name='show-cart'),
                  path('pluscart/', views.plus_cart),
                  path('minuscart/', views.minus_cart),
                  path('removecart/', views.remove_cart),
                  path('buy/', views.buy_now, name='buy-now'),
                  path('profile/', ProfileView.as_view(), name='profile'),
                  path('address/', views.address, name='address'),
                  path('orders/', views.orders, name='orders'),
                  path('checkout/', views.checkout, name='checkout'),
                  path('checkout/<int:product_id>/', views.checkout_advance, name='checkout'),
                  path('paymentdone/', views.payment_done, name='paymentdone'),
                  path('kind/<slug:data>',views.kind,name='kind'),
                  path('kind/<int:pkid>/<int:kid>',views.skind,name='skind'),
                  path('search/',views.search,name='search'),
                  path('analyze/',views.university_picture,name='analyze'),
                  path('accounts/login/',
                       auth_views.LoginView.as_view(template_name='Main/login.html', authentication_form=LoginForm),
                       name='login'),
                  path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
                  path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name='Main/passwordchange.html',
                                                                                form_class=MyPschangeForm,
                                                                                success_url='/passchangdone/'),
                       name="passwordchange"),
                  path('passchangdone/',
                       auth_views.PasswordChangeDoneView.as_view(template_name='Main/passchangdone.html'),
                       name='passchangdone'),
                  path('password-reset/', auth_views.PasswordResetView.as_view(template_name='Main/password_reset.html',
                                                                               form_class=MyPasswordResetForm),
                       name='password_reset'),

                  path('password-reset/done/',
                       auth_views.PasswordResetDoneView.as_view(template_name='Main/password_reset_done.html'),
                       name='password_reset_done'),
                  path('password-reset-confirm/<uidb64>/<token>/',
                       auth_views.PasswordResetConfirmView.as_view(template_name='Main/password_reset_confirm.html',
                                                                   form_class=MySetPasswordForm),
                       name='password_reset_confirm'),
                  path('password-reset-complete',
                       auth_views.PasswordResetCompleteView.as_view(template_name='Main/password_reset_complete.html'),
                       name='password_reset_complete'),
                  path('registration/', CustomerRegistrationView.as_view(), name='customerregistration'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
