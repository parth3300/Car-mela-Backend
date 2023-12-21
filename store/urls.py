from django.urls import path
from store import views
from rest_framework_nested import routers


router = routers.DefaultRouter()
router.register('carswithownership', views.CarWithOwnerShipViewSet, basename='car'),
router.register('carswithdealership', views.CarWithDealerShipViewSet),
router.register('companies', views.CompanyViewSet, basename='companies'),
router.register('customers', views.CustomerViewSet, basename='customers'),
router.register('dealers', views.DealerViewset, basename='dealers'),
router.register('carowners', views.CarOwnerViewset, basename='carowners')


carowner_routers = routers.NestedDefaultRouter(router, 'carswithownership', lookup='carwithownership')
carowner_routers.register('reviews', views.ReviewViewSet, basename='carwithowner-review')

cardealer_routers=routers.NestedDefaultRouter(router,'carswithdealership',lookup='carwithdealership')
cardealer_routers.register('reviews',views.ReviewViewSet,basename='carwithdealer-review')


urlpatterns = router.urls + carowner_routers.urls+cardealer_routers.urls
