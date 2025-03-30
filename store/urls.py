from django.urls import path
from store import views
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('companies', views.CompanyViewSet)
router.register('cars', views.CarViewSet, basename='car')
router.register('customers', views.CustomerViewSet)
router.register('carowners', views.CarOwnerViewset, basename='carowner')
router.register('carownerships', views.CarOwnerShipViewSet)
router.register('dealerships', views.DealerShipViewSet)
router.register('reviews', views.ReviewViewSet, basename='general-review')

car_routers = routers.NestedDefaultRouter(
    router, 'cars', lookup='car')
car_routers.register('reviews', views.ReviewViewSet,
                     basename='car-review')

# Add the Stripe payment URLs
urlpatterns = [
    path('create-checkout-session/', views.CreateCheckoutSession.as_view(), name='create-checkout-session'),
    path('stripe-webhook/', views.stripe_webhook, name='stripe-webhook')

]

# Combine all URLs
urlpatterns += router.urls + car_routers.urls