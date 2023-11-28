from django.urls import path
from store import views
from rest_framework_nested import routers


router = routers.DefaultRouter()
router.register('cars', views.CarViewSet),
router.register('companies', views.CompanyViewSet)


car_routers = routers.NestedDefaultRouter(router, 'cars', lookup='car')
car_routers.register('reviews', views.ReviewViewSet, basename='cars-reviews')

urlpatterns = router.urls + car_routers.urls
