# django_enquiry_saas/urls.py (your project's main urls.py)
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView  # Import RedirectView

admin.site.site_header = "Enquiry Management System"  # Change this text
admin.site.site_title = "Enquiry Admin Portal"  # For the browser tab title
admin.site.index_title = "Welcome to Enquiry Admin"  # Text on the admin index page

urlpatterns = [
    path("jet/", include("jet.urls")),
    path("superadminenq25/", admin.site.urls),
    path("dse/", include("sales_enquiry.urls")),
    # Add a path for the root URL
    # Redirect to the login page when accessing the root
    path("", RedirectView.as_view(url="/dse/login/", permanent=False)),
    # OR if you want a custom home view:
    # path('', views.home_view, name='home'),
]

# Needed for serving media files during development (important for image uploads)
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
