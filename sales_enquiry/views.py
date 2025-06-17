# sales_enquiry/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q, Count
import datetime  # Import for date filtering

# Import all necessary models and enums
from .models import Enquiry, CustomUser, UserRole, EnquiryStatus
from .forms import EnquiryForm

# --- Authentication Views (using Django's built-in) ---
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import (
    AuthenticationForm,
)


class CustomLoginView(LoginView):
    template_name = "registration/login.html"
    authentication_form = AuthenticationForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        messages.success(self.request, "You have been successfully logged in!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password.")
        return super().form_invalid(form)


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("login")

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, "You have been logged out.")
        return super().dispatch(request, *args, **kwargs)


# --- DSE Dashboard (ListView) ---
class DSEDashboardView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Enquiry
    template_name = "sales_enquiry/dse_dashboard.html"
    context_object_name = "enquiries"
    paginate_by = 10

    def test_func(self):
        return self.request.user.is_authenticated and (
            self.request.user.is_dse or self.request.user.is_admin
        )

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        # Base queryset: filter by DSE if not admin
        if user.is_dse:
            queryset = queryset.filter(dse=user)

        # --- Card Click Filtering ---
        # Get filter parameters from URL
        status_filter = self.request.GET.get("status_filter")
        show_all = self.request.GET.get("show_all")

        if status_filter:
            # Filter by specific status (e.g., 'SOLD', 'CLOSED')
            if status_filter in [EnquiryStatus.SOLD, EnquiryStatus.CLOSED]:
                queryset = queryset.filter(status=status_filter)
            elif status_filter == "OPEN":  # If you ever wanted to click to see 'OPEN'
                queryset = queryset.filter(status=EnquiryStatus.OPEN)

        elif show_all:
            # If 'show_all' is present, no further status filtering is applied,
            # meaning it shows all enquiries relevant to the user (DSE's or all for Admin)
            pass  # Queryset is already correctly set based on user type

        # --- Search Query ---
        search_query = self.request.GET.get("q")
        if search_query:
            queryset = queryset.filter(
                Q(customer_name__icontains=search_query)
                | Q(phone_number__icontains=search_query)
                | Q(unique_id__icontains=search_query)
                | Q(remarks__icontains=search_query)
            )

        # Order by latest submission first
        return queryset.order_by("-first_submit_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # --- Context for search and conditional rendering ---
        context["search_query"] = self.request.GET.get("q", "")
        context["status_filter"] = self.request.GET.get("status_filter")
        context["show_all"] = self.request.GET.get("show_all")

        # Determine if 'Edit' button should be shown
        # It should NOT be shown if a card was clicked (i.e., status_filter or show_all is present)
        context["show_edit_button"] = not (
            context["status_filter"] or context["show_all"]
        )

        # --- Calculate metrics for the cards (CURRENT MONTH ONLY) ---
        today = datetime.date.today()
        current_month_start = today.replace(day=1)
        # current_month_end = today.replace(day=calendar.monthrange(today.year, today.month)[1]) # Not strictly needed if using __month and __year

        if user.is_dse:
            # Filter by DSE and current month
            base_enquiries_for_cards_qs = Enquiry.objects.filter(
                dse=user,
                first_submit_at__year=today.year,
                first_submit_at__month=today.month,
            )
        else:  # Admin user sees counts for all DSEs in the current month
            base_enquiries_for_cards_qs = Enquiry.objects.filter(
                first_submit_at__year=today.year, first_submit_at__month=today.month
            )

        context["total_enquiries"] = base_enquiries_for_cards_qs.count()
        context["total_sold"] = base_enquiries_for_cards_qs.filter(
            status=EnquiryStatus.SOLD
        ).count()
        context["total_lost_closed"] = base_enquiries_for_cards_qs.filter(
            status=EnquiryStatus.CLOSED
        ).count()

        return context


# --- Enquiry Create View ---
class EnquiryCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Enquiry
    form_class = EnquiryForm
    template_name = "sales_enquiry/enquiry_form.html"
    success_url = reverse_lazy("dse_dashboard")

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_dse

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.dse = self.request.user
        form.instance.last_edited_by = self.request.user
        messages.success(self.request, "Enquiry submitted successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors in the form.")
        return super().form_invalid(form)


# --- Enquiry Update View ---
class EnquiryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Enquiry
    form_class = EnquiryForm
    template_name = "sales_enquiry/enquiry_form.html"
    context_object_name = "enquiry"
    success_url = reverse_lazy("dse_dashboard")

    def test_func(self):
        enquiry = self.get_object()
        return self.request.user.is_authenticated and (
            self.request.user.is_admin
            or (self.request.user.is_dse and enquiry.dse == self.request.user)
        )

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.last_edited_by = self.request.user
        messages.success(self.request, "Enquiry updated successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors in the form.")
        return super().form_invalid(form)


# --- Enquiry Detail View ---
class EnquiryDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Enquiry
    template_name = "sales_enquiry/enquiry_detail.html"
    context_object_name = "enquiry"

    def test_func(self):
        enquiry = self.get_object()
        return self.request.user.is_authenticated and (
            self.request.user.is_admin
            or (self.request.user.is_dse and enquiry.dse == self.request.user)
        )
