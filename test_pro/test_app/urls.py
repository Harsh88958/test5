from django.urls import path
from . import views

urlpatterns = [
    path("initiate-payment/", views.initiate_payment, name="initiate_payment"),
    # path("process-payment/", views.check_transaction_status, name="process_payment"),
    # Add other URLs as needed
]
