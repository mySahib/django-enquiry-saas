# sales_enquiry/admin.py
from django.contrib import admin
from django.db.models import Sum, Count, F
from django.urls import reverse
from django.utils.html import format_html

# from django.contrib.admin import SimpleListFilter # REMOVED: Not using SimpleListFilter for date range
from django.utils import timezone  # Keep this for debugging/shell if needed
import datetime  # Keep this for debugging/shell if needed

from rangefilter.filters import DateRangeFilter  # RE-ENABLED: We want calendar pickers!

from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Enquiry, CustomUser, EnquiryStatus, UserRole


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "email",
        "role",
        "is_dse",
        "is_admin",
        "is_staff",
        "is_active",
    )
    list_filter = ("role", "is_staff", "is_active")
    search_fields = ("username", "email")
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Personal info",
            {"fields": ("first_name", "last_name", "email", "phone_number")},
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                    "role",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )


class EnquiryResource(resources.ModelResource):
    class Meta:
        model = Enquiry
        fields = (
            "unique_id",
            "customer_name",
            "phone_number",
            "enquiry_source",
            "interested_in_model",
            "buying_type",
            "finance_bank",
            "assigned_financier_name",
            "deal_offer_image",
            "remarks",
            "follow_up_status",
            "dse__username",
            "status",
            "first_submit_at",
            "last_updated_at",
            "sold_at",
            "closed_at",
            "sale_value",
            "close_reason",
            "last_edited_by__username",
        )
        export_order = (
            "unique_id",
            "customer_name",
            "phone_number",
            "enquiry_source",
            "interested_in_model",
            "buying_type",
            "finance_bank",
            "assigned_financier_name",
            "deal_offer_image",
            "remarks",
            "follow_up_status",
            "dse__username",
            "status",
            "first_submit_at",
            "last_updated_at",
            "sold_at",
            "closed_at",
            "sale_value",
            "close_reason",
            "last_edited_by__username",
        )


@admin.register(Enquiry)
class EnquiryAdmin(ImportExportModelAdmin):
    resource_class = EnquiryResource
    list_display = (
        "unique_id",
        "customer_name",
        "phone_number",
        "dse",
        "enquiry_source",
        "interested_in_model",
        "buying_type",
        "finance_bank",
        "assigned_financier_name",
        "status",
        "sale_value",
        "follow_up_status",
        "first_submit_at",
        "last_updated_at",
        "display_edit_link",
    )

    list_filter = (
        "dse",
        "status",
        "buying_type",
        "finance_bank",
        "enquiry_source",
        "interested_in_model",
        "follow_up_status",
        # Use DateRangeFilter for all date fields to get calendar pickers
        ("first_submit_at", DateRangeFilter),
        ("last_updated_at", DateRangeFilter),
        ("sold_at", DateRangeFilter),
        ("closed_at", DateRangeFilter),
    )

    search_fields = (
        "unique_id",
        "customer_name",
        "phone_number",
        "remarks",
        "dse__username",
        "finance_bank",
        "assigned_financier_name",
        "interested_in_model",
    )

    readonly_fields = (
        "unique_id",
        "dse",
        "first_submit_at",
        "last_updated_at",
        "last_edited_by",
        "sold_at",
        "closed_at",
    )

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "customer_name",
                    "phone_number",
                    "enquiry_source",
                    "interested_in_model",
                    "remarks",
                )
            },
        ),
        (
            "Deal & Status Information",
            {
                "fields": (
                    "buying_type",
                    "finance_bank",
                    "assigned_financier_name",
                    "deal_offer_image",
                    "follow_up_status",
                    "status",
                    "close_reason",
                    "sale_value",
                )
            },
        ),
        (
            "System Information",
            {
                "fields": (
                    "unique_id",
                    "dse",
                    "first_submit_at",
                    "last_updated_at",
                    "last_edited_by",
                    "sold_at",
                    "closed_at",
                ),
                "classes": ("collapse",),
            },
        ),
    )

    ordering = ("-first_submit_at",)

    change_list_template = "admin/sales_enquiry/enquiry/change_list.html"

    def display_edit_link(self, obj):
        url = reverse(
            "admin:%s_%s_change" % (obj._meta.app_label, obj._meta.model_name),
            args=[obj.pk],
        )
        return format_html('<a class="btn btn-info btn-sm" href="{}">Edit</a>', url)

    display_edit_link.short_description = "Actions"

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)

        cl = response.context_data["cl"]
        queryset = cl.queryset

        total_open = queryset.filter(status=EnquiryStatus.OPEN).count()
        total_sold = queryset.filter(status=EnquiryStatus.SOLD).count()
        total_closed = queryset.filter(status=EnquiryStatus.CLOSED).count()
        total_enquiries = queryset.count()

        total_sale_value = (
            queryset.filter(status=EnquiryStatus.SOLD).aggregate(Sum("sale_value"))[
                "sale_value__sum"
            ]
            or 0
        )

        dse_metrics = {}
        dse_ids = queryset.values_list("dse", flat=True).distinct()
        for dse_id in dse_ids:
            if dse_id:
                dse_user = CustomUser.objects.get(pk=dse_id)
                dse_qs = queryset.filter(dse=dse_user)
                dse_total = dse_qs.count()
                dse_sold = dse_qs.filter(status=EnquiryStatus.SOLD).count()

                conversion_rate = (dse_sold / dse_total * 100) if dse_total > 0 else 0
                dse_metrics[dse_user.username] = {
                    "total": dse_total,
                    "sold": dse_sold,
                    "conversion_rate": f"{conversion_rate:.2f}%",
                }

        overall_sold = queryset.filter(status=EnquiryStatus.SOLD).count()
        overall_total = queryset.count()
        overall_conversion_rate = (
            (overall_sold / overall_total * 100) if overall_total > 0 else 0
        )

        extra_context = extra_context or {}
        extra_context["summary_data"] = {
            "total_open": total_open,
            "total_sold": total_sold,
            "total_closed": total_closed,
            "total_enquiries": total_enquiries,
            "overall_conversion_rate": f"{overall_conversion_rate:.2f}%",
            "dse_metrics": dse_metrics,
        }
        response.context_data.update(extra_context)
        return response
