# sales_enquiry/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
import uuid  # For unique_id and now for the primary_key
from django.utils import timezone  # Import timezone for custom ID generation if needed


def generate_unique_enquiry_id():
    # You can combine uuid with a timestamp if you want,
    # but for guaranteed uniqueness, uuid.uuid4().hex is sufficient.
    return f"ENQ-{uuid.uuid4().hex[:10].upper()}"


# Custom User Model (DSEs and Admins)
class UserRole(models.TextChoices):
    DSE = "DSE", _("DSE")
    ADMIN = "ADMIN", _("Admin")


class CustomUser(AbstractUser):
    # Add your custom fields here
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(
        max_length=5,
        choices=UserRole.choices,
        default=UserRole.DSE,
        verbose_name=_("Role"),
    )

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.username

    @property
    def is_dse(self):
        return self.role == UserRole.DSE

    @property
    def is_admin(self):
        return self.role == UserRole.ADMIN


# Enquiry Model
class EnquirySource(models.TextChoices):
    WALK_IN = "WALKIN", _("Walk-in")
    TELE = "TELE", _("Tele")
    WEBSITE = "WEB", _("Website")
    FLIPKART = "FLIPKART", _("Flipkart")
    AMAZON = "AMAZON", _("Amazon")
    CSD = "CSD", _("CSD")
    CPC = "CPC", _("CPC")
    ADS = "ADS", _("Ads")
    EVENTS = "EVENTS", _("Events")
    REFERRAL = "REF", _("Referral")
    OTHER = "OTHER", _("Other")


class BuyingType(models.TextChoices):
    CASH = "CASH", _("Cash")
    FINANCE = "FINANCE", _("Finance")
    # If you had Exchange, it would go here too
    # EXCHANGE = "EXCHANGE", _("Exchange")


class FollowUpStatus(models.TextChoices):
    INTERESTED = "INTERESTED", _("Interested")
    HOT_LEAD = "HOT_LEAD", _("Hot Lead")
    TEST_DRIVE_SCHEDULED = "TD_SCHED", _("Test Drive Scheduled")
    QUOTATION_SENT = "QUOTE_SENT", _("Quotation Sent")
    CALL_ON_DELIVERY = "COD", _("Call On Delivery")
    FIFTY_FIFTY = "50_50", _("50-50")
    NEGOTIATION_PHASE = "NEGOTIATE", _("Negotiation Phase")
    FOLLOW_UP_SCHEDULED = "FU_SCHED", _("Follow-up Call/Visit Scheduled")
    DOCUMENTATION_PENDING = "DOC_PENDING", _("Documentation Pending")


class EnquiryStatus(models.TextChoices):
    OPEN = "OPEN", _("Open")
    PENDING_SOLD_APPROVAL = "PEND_SOLD", _("Pending Sold Approval")
    SOLD = "SOLD", _("Sold")
    PENDING_CLOSE_APPROVAL = "PEND_CLOSE", _("Pending Close Approval")
    CLOSED = "CLOSED", _("Closed")


# --- NEW: Choices for 'Interested In' Models ---
class InterestedInModel(models.TextChoices):
    SPLENDOR_PLUS = "SPLENDOR_PLUS", "Splendor Plus"
    SUPER_SPLENDOR = "SUPER_SPLENDOR", "Super Splendor"
    XTREME_125R = "XTREME_125R", "Xtreme 125R"
    DESTINI_125 = "DESTINI_125", "Destini 125"
    PLEASURE_PLUS = "PLEASURE_PLUS", "Pleasure Plus"
    XOOM_125 = "XOOM_125", "Xoom 125"
    XTREME_160R = "XTREME_160R", "Xtreme 160R"
    HF_DELUXE = "HF_DELUXE", "HF Deluxe"
    XPULSE_200 = "XPULSE_200", "Xpulse 200"
    SUPER_SPLENDOR_XTEC = "SUPER_SPLENDOR_XTEC", "Super Splendor Xtec"
    XTREME_160R_4V = "XTREME_160R_4V", "Xtreme 160R 4V"
    MAVRICK_440 = "MAVRICK_440", "Mavrick 440"
    DESTINI_PRIME = "DESTINI_PRIME", "Destini Prime"
    XOOM_160 = "XOOM_160", "Xoom 160"
    PLEASURE = "PLEASURE", "Pleasure"
    SPLENDOR_PLUS_XTEC = "SPLENDOR_PLUS_XTEC", "Splendor Plus Xtec"
    PASSION_PLUS = "PASSION_PLUS", "Passion Plus"
    XPULSE_210 = "XPULSE_210", "Xpulse 210"
    XOOM = "XOOM", "Xoom"
    XOOM_110 = "XOOM_110", "Xoom 110"
    GLAMOUR = "GLAMOUR", "Glamour"
    GLAMOUR_XTEC = "GLAMOUR_XTEC", "Glamour Xtec"


# --- NEW: Choices for Finance Banks ---
class FinanceBank(models.TextChoices):
    HERO_FINCORP = "HERO_FINCORP", "Hero Fincorp Ltd"
    IDFC_BANK = "IDFC_BANK", "IDFC Bank"
    HDB_BANK = "HDB_BANK", "HDB Bank"
    CWC_LTD = "CWC_LTD", "CWC Ltd"
    SMFG_BANK = "SMFG_BANK", "SMFG Bank"
    AU_SMALL_FIN_BANK = "AU_SMALL_FIN_BANK", "Au Small Fin. Bank"
    HINDUJA_LEYLAND_BANK = "HINDUJA_LEYLAND_BANK", "Hinduja Leyland Bank"
    TATA_CAPITAL = "TATA_CAPITAL", "Tata Capital Ltd"
    RBL_BANK = "RBL_BANK", "RBL Bank"
    MUTHOOT_BANK = "MUTHOOT_BANK", "Muthoot Bank"
    LT_FIN_LTD = "LT_FIN_LTD", "L & T Fin. Ltd"
    HDFC_BANK = "HDFC_BANK", "HDFC Bank"
    CHOLA_MANDALAM_BANK = "CHOLA_MANDALAM_BANK", "Chola Mandalam Bank"


class Enquiry(models.Model):
    # ADD THIS LINE: Define a UUIDField as the primary key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Your existing unique_id field can remain for display purposes if you want
    # a shorter, human-readable ID that's different from the full UUID primary key.
    unique_id = models.CharField(
        max_length=30,
        unique=True,
        default=generate_unique_enquiry_id,
        editable=False,
    )

    customer_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, help_text="Customer's phone number")
    enquiry_source = models.CharField(
        max_length=10, choices=EnquirySource.choices, default=EnquirySource.WALK_IN
    )

    # --- NEW FIELD ADDED HERE ---
    interested_in_model = models.CharField(
        max_length=50,
        choices=InterestedInModel.choices,
        blank=True,
        null=True,  # Allow this to be optional initially
        verbose_name=_(
            "Interested In Model"
        ),  # Use gettext_lazy for translation if needed
    )

    buying_type = models.CharField(
        max_length=10, choices=BuyingType.choices, default=BuyingType.CASH
    )

    # --- NEW FIELD ADDED HERE (conditional visibility will be handled in form/template) ---
    finance_bank = models.CharField(
        max_length=50,  # Increased max_length to accommodate longer bank names/keys if needed
        choices=FinanceBank.choices,
        blank=True,
        null=True,  # Allow this to be optional
        verbose_name=_("Finance Bank"),
    )
    # Based on your existing model, 'assigned_financier_name' now holds the 'Bank if buying type is Finance' help text
    # So, we'll keep it as is, or you can rename it to 'finance_remarks' or similar if it's not a financier's name
    assigned_financier_name = models.CharField(
        max_length=100, blank=True, null=True, help_text="Financier's contact person"
    )

    deal_offer_image = models.ImageField(
        upload_to="deal_offers/", blank=True, null=True
    )  # Requires Pillow

    remarks = models.TextField(blank=True, null=True)
    follow_up_status = models.CharField(
        max_length=20, choices=FollowUpStatus.choices, default=FollowUpStatus.INTERESTED
    )

    # Foreign Key to the CustomUser (DSE) who submitted the enquiry
    dse = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="submitted_enquiries"
    )

    status = models.CharField(
        max_length=10, choices=EnquiryStatus.choices, default=EnquiryStatus.OPEN
    )

    first_submit_at = models.DateTimeField(
        auto_now_add=True
    )  # Automatically sets on creation
    last_updated_at = models.DateTimeField(
        auto_now=True
    )  # Automatically updates on each save

    sold_at = models.DateTimeField(blank=True, null=True)
    closed_at = models.DateTimeField(blank=True, null=True)
    sale_value = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    close_reason = models.TextField(blank=True, null=True)

    # To track who last edited the enquiry (DSE or Admin)
    last_edited_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,  # If the editor user is deleted, set this to NULL
        related_name="edited_enquiries",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name_plural = "Enquiries"  # Proper plural name in Admin
        ordering = ["-first_submit_at"]  # Added this for consistent ordering

    def __str__(self):
        return f"Enquiry {self.unique_id} - {self.customer_name}"
