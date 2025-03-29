from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.core.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import *
from .serializers import *
from .filter import *
from rest_framework.parsers import MultiPartParser, FormParser
import stripe
from django.conf import settings
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

# Common ViewSet configuration
class BaseViewSet(ModelViewSet):
    def get_serializer_context(self):
        return {'request': self.request}

class CompanyViewSet(BaseViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'country']
    ordering_fields = ['since']

class CarViewSet(BaseViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = CarFilter
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'last_update']

class CustomerViewSet(BaseViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class CarOwnerViewset(BaseViewSet):
    parser_classes = (MultiPartParser, FormParser)
    queryset = CarOwner.objects.all()
    filter_backends = [DjangoFilterBackend]

    def get_serializer_class(self):
        return AdminCarOwnerSerializer if self.request.user.is_staff else CarOwnerSerializer

    @action(detail=False, methods=['GET', 'PATCH'], permission_classes=[IsAuthenticated])
    def me(self, request):
        carowner = get_object_or_404(CarOwner, user=request.user)
        
        if request.method == 'GET':
            return Response(self.get_serializer(carowner).data)
        
        if carowner.user != request.user:
            raise PermissionDenied("You don't have permission to perform this action.")
            
        serializer = self.get_serializer(carowner, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class CarOwnerShipViewSet(BaseViewSet):
    queryset = CarOwnerShip.objects.all()
    serializer_class = CarOwnerShipSerializer
    filterset_class = CarOwnerShipFilter

class DealerShipViewSet(BaseViewSet):
    queryset = DealerShip.objects.all()
    serializer_class = DealerShipSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['dealership_name']
    ordering_fields = ['ratings']

class ReviewViewSet(BaseViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        car_id = self.kwargs.get('car_pk')
        return Review.objects.filter(car_id=car_id)

    def perform_create(self, serializer):
        car_id = self.kwargs.get('car_pk') or self.request.data.get('car_id')
        if not car_id:
            raise PermissionDenied("Car ID must be provided.")
        serializer.save(car_id=car_id)

# Stripe Payment Views
stripe.api_key = settings.STRIPE_SECRET_KEY

class CreateCheckoutSession(APIView):

    def post(self, request):
        try:
            data = {
                'payment_method_types': ['card'],
                'line_items': [{
                    'price_data': {
                        'currency': request.data.get('currency', 'usd'),
                        'product_data': {'name': f'Car Purchase - ID: {request.data["car_id"]}'},
                        'unit_amount': int(request.data['amount']),
                    },
                    'quantity': 1,
                }],
                'mode': 'payment',
                'success_url': f'{settings.FRONTEND_URL}/payment-success?session_id={{CHECKOUT_SESSION_ID}}',
                'cancel_url': f'{settings.FRONTEND_URL}/payment-canceled',
                'metadata': {
                    'car_id': request.data['car_id'],
                    'carowner_id': request.data['carowner_id'],
                    'user_id': request.user.id
                }
            }
            session = stripe.checkout.Session.create(**data)
            return Response({'id': session.id})
        except Exception as e:
            return Response({'error': str(e)}, status=400)

@csrf_exempt
def stripe_webhook(request):
    try:
        event = stripe.Webhook.construct_event(
            request.body,
            request.META['HTTP_STRIPE_SIGNATURE'],
            settings.STRIPE_WEBHOOK_SECRET
        )
        
        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            metadata = session.metadata
            
            # Create ownership record
            CarOwnerShip.objects.create(
                car_id=metadata.car_id,
                carowner_id=metadata.carowner_id
            )
            
            # Mark car as sold
            car = Car.objects.get(id=metadata.car_id)
            car.carowner_id = metadata.carowner_id
            car.save()
            
        return HttpResponse(status=200)
        
    except Exception as e:
        print(f"Stripe webhook error: {str(e)}")
        return HttpResponse(status=400)