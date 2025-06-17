# sales_enquiry/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    DSEDashboardView,
    EnquiryCreateView,
    EnquiryUpdateView,
    EnquiryDetailView,
)

urlpatterns = [
    # Login and Logout URLs
    # CORRECTED TEMPLATE PATH HERE:
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),
    # Your existing application URLs
    path("dashboard/", DSEDashboardView.as_view(), name="dse_dashboard"),
    path("enquiry/new/", EnquiryCreateView.as_view(), name="enquiry_create"),
    path("enquiry/<uuid:pk>/edit/", EnquiryUpdateView.as_view(), name="enquiry_update"),
    path(
        "enquiry/<uuid:pk>/detail/", EnquiryDetailView.as_view(), name="enquiry_detail"
    ),
]
