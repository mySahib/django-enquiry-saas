# sales_enquiry/forms.py
from django import forms
from .models import Enquiry, CustomUser, EnquiryStatus
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Layout,
    Submit,
    Row,
    Column,
)  # Removed Div/HTML as they won't be used for layout directly here


class EnquiryForm(forms.ModelForm):
    class Meta:
        model = Enquiry
        fields = [
            "customer_name",
            "phone_number",
            "enquiry_source",
            "interested_in_model",
            "buying_type",
            "finance_bank",  # Keep in Meta.fields
            "assigned_financier_name",  # Keep in Meta.fields
            "deal_offer_image",
            "remarks",
            "follow_up_status",
        ]
        widgets = {
            "remarks": forms.Textarea(attrs={"rows": 3}),
            "close_reason": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()

        # Define the base layout elements (Crispy Forms will render these)
        layout_elements = [
            Row(
                Column("customer_name", css_class="form-group col-md-6 mb-0"),
                Column("phone_number", css_class="form-group col-md-6 mb-0"),
                css_class="form-row",
            ),
            Row(
                Column("enquiry_source", css_class="form-group col-md-6 mb-0"),
                Column("interested_in_model", css_class="form-group col-md-6 mb-0"),
                css_class="form-row",
            ),
            Row(
                Column("buying_type", css_class="form-group col-md-6 mb-0"),
                css_class="form-row",
            ),
            # REMOVED: 'finance_bank', 'assigned_financier_name' from Crispy layout
            "deal_offer_image",  # This field will be rendered by Crispy
            "remarks",
            Row(
                Column("follow_up_status", css_class="form-group col-md-6 mb-0"),
                css_class="form-row",
            ),
        ]

        if user and user.is_admin:
            self.fields["status"] = forms.ChoiceField(
                choices=EnquiryStatus.choices,
                label="Status",
                required=True,
                initial=(
                    self.instance.status if self.instance.pk else EnquiryStatus.OPEN
                ),
            )

            # Ensure these fields are also recognized by Django's form processing
            if "status" not in self.Meta.fields:
                self.Meta.fields.append("status")
            if "sale_value" not in self.Meta.fields:
                self.Meta.fields.append("sale_value")
            if "close_reason" not in self.Meta.fields:
                self.Meta.fields.append("close_reason")

            # REMOVED: 'status', 'sale_value', 'close_reason' from Crispy layout for manual rendering
            layout_elements.insert(
                len(layout_elements)
                - 1,  # Example: insert status field before deal_offer_image
                Row(
                    Column("status", css_class="form-group col-md-6 mb-0"),
                    css_class="form-row",
                ),
            )
        # else: # For DSE users, no additional fields are added, status remains default in model

        # Apply the constructed layout
        self.helper.layout = Layout(
            *layout_elements,
            Submit("submit", "Submit Enquiry", css_class="btn btn-primary mt-3")
        )

    def clean(self):
        # Your clean method remains the same and handles validation for all fields
        cleaned_data = super().clean()
        buying_type = cleaned_data.get("buying_type")
        finance_bank = cleaned_data.get("finance_bank")
        assigned_financier_name = cleaned_data.get("assigned_financier_name")

        # Validation for finance fields
        if buying_type == "FINANCE":
            if not finance_bank:
                self.add_error(
                    "finance_bank", "Finance Bank is required for Finance buying type."
                )
            if not assigned_financier_name:
                self.add_error(
                    "assigned_financier_name",
                    "Financier Name is required for Finance buying type.",
                )
        else:
            # Clear finance-related fields if buying type is not Finance
            cleaned_data["finance_bank"] = None
            cleaned_data["assigned_financier_name"] = ""

        # Validation for status-dependent fields (only applies if fields were rendered, i.e., for Admin)
        status = cleaned_data.get("status")
        sale_value = cleaned_data.get("sale_value")
        close_reason = cleaned_data.get("close_reason")

        if status:  # Check if 'status' field was actually part of the form submission
            if status == EnquiryStatus.SOLD:
                if not sale_value:
                    self.add_error(
                        "sale_value", "Sale Value is required for Sold status."
                    )
            else:
                cleaned_data["sale_value"] = None

            if status == EnquiryStatus.CLOSED:
                if not close_reason:
                    self.add_error(
                        "close_reason", "Close Reason is required for Closed status."
                    )
            else:
                cleaned_data["close_reason"] = ""

        return cleaned_data
