from django.urls import path
from store import views
from rest_framework_nested import routers


router = routers.DefaultRouter()
router.register('cars', views.CarViewSet, basename='car'),
router.register('carwithdealership', views.CarWithDealerShipViewSet),
router.register('companies', views.CompanyViewSet, basename='companies'),
router.register('customers', views.CustomerViewSet, basename='customers'),
router.register('dealers', views.DealerViewset, basename='dealers'),
router.register('carowners', views.CarOwnerViewset, basename='carowners')


car_routers = routers.NestedDefaultRouter(router, 'cars', lookup='car')
car_routers.register('reviews', views.ReviewViewSet, basename='car-review')

urlpatterns = router.urls + car_routers.urls
