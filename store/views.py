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
from django.core.exceptions import ObjectDoesNotExist

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
    serializer_class = CarOwnerSerializer

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
        if car_id:
            return Review.objects.filter(car_id=car_id)
        return Review.objects.filter(car_id__isnull=True)  # Fetch reviews where car_id is NULL

    def perform_create(self, serializer):
        car_id = self.kwargs.get('car_pk') or self.request.data.get('car_id')
        serializer.save(car_id=car_id if car_id else None) 


    
class FAQViewSet(BaseViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer



# Stripe Payment Views
stripe.api_key = "sk_test_51R7s8F09peBWzWCi6rEm8BcWJU0BOdjD2heuhjL3NWXPsMgzbd6SBdZN02kJLJbJJqnWFxzecnECxzMRqvTuVEur003En7iz3V" 

class CreateCheckoutSession(APIView):
    def post(self, request):
        try:
            car = Car.objects.get(id=request.data['car_id'])
            
            session_data = {
                'payment_method_types': ['card'],
                'line_items': [{
                    'price_data': {
                        'currency': request.data.get('currency', 'usd'),
                        'product_data': {
                            'name': f'{car.title} - {car.carmodel}',
                            'images': [car.image.url] if car.image else [],
                        },
                        'unit_amount': int(request.data['amount']),
                    },
                    'quantity': 1,
                }],
                'mode': 'payment',
                'success_url': f'{settings.FRONTEND_URL}/payment-success?session_id={{CHECKOUT_SESSION_ID}}',
                'cancel_url': f'{settings.FRONTEND_URL}/payment-canceled',
                'customer_email': request.data['user_email'],  # Prefills email
                'payment_intent_data': {
                    'receipt_email': request.data['user_email'],  # Ensures receipt is sent
                    'description': f'Purchase of {car.title} by {request.data["user_name"]}'
                },
                'metadata': {
                    'car_id': request.data['car_id'],
                    'carowner_id': request.data['carowner_id'],
                    'user_id': request.data['user_id'],
                    'user_email': request.data['user_email'],
                    'user_name': request.data['user_name']
                },
                'billing_address_collection': 'required',  # Changed to required
                'submit_type': 'pay',
            }

            session = stripe.checkout.Session.create(**session_data)
            return Response({'id': session.id})

        except Car.DoesNotExist:
            return Response({'error': 'Car not found'}, status=404)
        except KeyError as e:
            return Response({'error': f'Missing required field: {str(e)}'}, status=400)
        except ValueError as e:
            return Response({'error': f'Invalid amount value: {str(e)}'}, status=400)
        except stripe.error.StripeError as e:
            return Response({'error': f'Payment processing error: {str(e)}'}, status=400)
        except Exception as e:
            return Response({'error': f'Unexpected error: {str(e)}'}, status=500)   
            
class VerifyPayment(APIView):

    def get(self, request, session_id):
        print(f"\n=== ENTERING VERIFY PAYMENT ===")
        print(f"Initial session_id: {session_id}")
        try:
            # Clean the session ID more thoroughly
            session_id = session_id.strip('/')
            print(f"Cleaned session_id: {session_id}")
            
            if not session_id.startswith('cs_'):
                print("ERROR: Session ID doesn't start with 'cs_'")
                return Response({'error': 'Invalid session ID format'}, status=400)
                
            print("Retrieving Stripe session...")
            checkout_session = stripe.checkout.Session.retrieve(
                session_id,
                expand=['payment_intent']  # Get more details
            )
            
            # Debug logging
            print("\n=== STRIPE SESSION DETAILS ===")
            print(f"Session ID: {checkout_session.id}")
            print(f"Payment status: {checkout_session.payment_status}")
            print(f"Metadata: {checkout_session.metadata}")
            print(f"Payment intent: {checkout_session.payment_intent}")
            print(f"Amount total: {checkout_session.amount_total}")
            
            if checkout_session.payment_status == 'paid':
                print("\nPayment is PAID - handling successful payment")
                return self.handle_successful_payment(checkout_session)
            
            print("\nPayment NOT completed - handling failed payment")
            return self.handle_failed_payment(checkout_session)
            
        except stripe.error.StripeError as e:
            print("\n!!! STRIPE ERROR !!!")
            print(f"Error type: {type(e).__name__}")
            print(f"Error message: {str(e)}")
            return self.handle_stripe_error(e)
        except Exception as e:
            print("\n!!! UNEXPECTED ERROR !!!")
            import traceback
            traceback.print_exc()  # Log full traceback
            return self.handle_unexpected_error(e)
   
    def handle_successful_payment(self, checkout_session):
        print("\n=== HANDLING SUCCESSFUL PAYMENT ===")
        metadata = checkout_session.metadata
        print(f"Raw metadata: {metadata}")
        
        try:
            # Validate required metadata fields
            required_fields = ['car_id', 'carowner_id']
            print("\nValidating metadata fields...")
            for field in required_fields:
                print(f"Checking field: {field}")
                if field not in metadata:
                    print(f"MISSING FIELD: {field}")
                    raise ValueError(f"Missing required metadata field: {field}")
                print(f"Field {field} exists with value: {metadata[field]}")

            print("\nCreating car ownership record...")
            ownership = CarOwnerShip.objects.create(
                car_id=metadata['car_id'],
                carowner_id=metadata['carowner_id'],
            )
            print(f"Ownership record created: {ownership}")
            print(f"Ownership ID: {ownership.id}")
        
            print("\nFetching car details...")
            car = Car.objects.get(id=metadata['car_id'])
            print(f"Car found: {car}")

            print("\n=== PAYMENT VERIFICATION SUCCESS ===",{
                'status': 'success',
                'message': 'Payment verified and ownership recorded',
                'carowner_id': ownership.carowner_id,
                'car_id': car.id,
                'session': {
                    'id': checkout_session.id,
                    'payment_intent': checkout_session.payment_intent,
                    'amount_total': checkout_session.amount_total / 100  # Convert to dollars
                }
            })
            
            return Response({
                'status': 'success',
                'message': 'Payment verified and ownership recorded',
                'carowner_id': ownership.carowner_id,
                'car_id': car.id,
                'session': {
                    'id': checkout_session.id,
                    'payment_intent': checkout_session.payment_intent,
                    'amount_total': checkout_session.amount_total / 100  # Convert to dollars
                }
            })
            
        except ObjectDoesNotExist as e:
            print("\n!!! OBJECT NOT FOUND ERROR !!!")
            print(f"Error: {str(e)}")
            return Response({
                'status': 'error',
                'message': f'Related object not found: {str(e)}',
                'metadata': metadata
            }, status=404)
        except ValueError as e:
            print("\n!!! VALUE ERROR !!!")
            print(f"Error: {str(e)}")
            return Response({
                'status': 'error',
                'message': str(e),
                'metadata': metadata
            }, status=400)
        except Exception as e:
            print("\n!!! OWNERSHIP CREATION ERROR !!!")
            print(f"Error type: {type(e).__name__}")
            print(f"Error message: {str(e)}")
            return Response({
                'status': 'error',
                'message': f'Payment verified but failed to record ownership: {str(e)}',
                'metadata': metadata
            }, status=500)

    def handle_failed_payment(self, checkout_session):
        print("\n=== HANDLING FAILED PAYMENT ===")
        print(f"Payment status: {checkout_session.payment_status}")
        return Response({
            'status': 'failed',
            'message': 'Payment not completed',
            'session_id': checkout_session.id,
            'payment_status': checkout_session.payment_status
        }, status=400)

    def handle_stripe_error(self, error):
        print("\n=== HANDLING STRIPE ERROR ===")
        print(f"Error details: {str(error)}")
        return Response({
            'status': 'error',
            'message': f'Stripe error: {str(error)}',
            'error_type': type(error).__name__
        }, status=400)

    def handle_unexpected_error(self, error):
        print("\n=== HANDLING UNEXPECTED ERROR ===")
        print(f"Error details: {str(error)}")
        return Response({
            'status': 'error',
            'message': f'An unexpected error occurred: {str(error)}',
            'error_type': type(error).__name__
        }, status=500)


