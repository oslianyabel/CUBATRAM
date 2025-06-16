from django.contrib import admin
from django.utils.html import format_html
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import (
    Booking,
    Category,
    ContactInfo,
    Destination,
    HeroSection,
    InfoPoint,
    InfoSection,
    SocialMediaLink,
    SpecialOffer,
    Tour,
    TourImage,
)

admin.site.site_header = "CUBATRAM administration"
admin.site.site_title = "CUBATRAM administration portal"
admin.site.index_title = "Welcome to the CUBATRAM administration portal"


class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category


class DestinationResource(resources.ModelResource):
    class Meta:
        model = Destination


class TourResource(resources.ModelResource):
    class Meta:
        model = Tour
        exclude = ("images",)  # Excluir el campo many-to-many


class BookingResource(resources.ModelResource):
    class Meta:
        model = Booking


class SpecialOfferResource(resources.ModelResource):
    class Meta:
        model = SpecialOffer


class SocialMediaLinkResource(resources.ModelResource):
    class Meta:
        model = SocialMediaLink


@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "title1",
        "title2",
        "title3",
        "is_active",
        "display_order",
        "preview_image",
    )
    list_editable = ("title1", "title2", "title3", "is_active")
    list_filter = ("is_active",)
    ordering = ("display_order",)

    def preview_image(self, obj):
        if obj.background_image:
            return format_html(
                '<img src="{}" style="max-height: 100px;" />', obj.background_image.url
            )
        return "-"

    preview_image.short_description = "Preview"  # type: ignore


@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin, admin.ModelAdmin):  # type: ignore
    resource_class = CategoryResource
    list_display = ("title", "slug", "is_featured", "display_order")
    list_editable = ("is_featured", "display_order")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Destination)
class DestinationAdmin(ImportExportModelAdmin, admin.ModelAdmin):  # type: ignore
    resource_class = DestinationResource
    list_display = ("name", "slug", "is_active", "is_popular", "display_order")
    list_editable = ("is_active", "is_popular", "display_order")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(TourImage)
class TourImageAdmin(admin.ModelAdmin):
    list_display = ("__str__", "display_order")
    list_editable = ("display_order",)


class TourImageInline(admin.TabularInline):
    model = Tour.images.through
    extra = 1


@admin.register(Tour)
class TourAdmin(ImportExportModelAdmin, admin.ModelAdmin):  # type: ignore
    resource_class = TourResource
    list_display = (
        "title",
        "price_display",
        "main_image_preview",
        "is_featured",
        "is_active",
    )
    list_filter = ("categories", "destinations", "is_featured", "is_active")
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [TourImageInline]
    exclude = ("images",)

    filter_horizontal = ("categories", "destinations")
    readonly_fields = ("created_at", "updated_at")
    date_hierarchy = "created_at"

    def price_display(self, obj):
        if obj.child_price:
            return f"Adulto: ${obj.adult_price} | Niño: ${obj.child_price}"
        return f"${obj.adult_price}"

    price_display.short_description = "Precios"  # type: ignore

    def main_image_preview(self, obj):
        if obj.main_image:
            return format_html(
                '<img src="{}" style="max-height: 200px;" />', obj.main_image.url
            )
        return "-"

    main_image_preview.short_description = "Vista previa"  # type: ignore


class InfoPointInline(admin.TabularInline):
    model = InfoPoint
    extra = 1


@admin.register(InfoSection)
class InfoSectionAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active")
    inlines = [InfoPointInline]


@admin.register(SpecialOffer)
class SpecialOfferAdmin(ImportExportModelAdmin, admin.ModelAdmin):  # type: ignore
    resource_class = SpecialOfferResource
    list_display = (
        "title",
        "discount_percentage",
        "valid_from",
        "valid_to",
        "is_active",
    )
    list_filter = ("is_active",)
    date_hierarchy = "valid_from"


@admin.register(Booking)
class BookingAdmin(ImportExportModelAdmin, admin.ModelAdmin):  # type: ignore
    resource_class = BookingResource
    list_display = (
        "id",
        "tour",
        "email",
        "date",
        "time",
        "total_price",
        "is_confirmed",
    )
    list_filter = ("is_confirmed", "tour", "date")
    search_fields = ("email", "tour__title")
    date_hierarchy = "date"


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not ContactInfo.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(SocialMediaLink)
class SocialMediaLinkAdmin(ImportExportModelAdmin, admin.ModelAdmin):  # type: ignore
    resource_class = SocialMediaLinkResource
    list_display = ("name", "url", "display_order")
    list_editable = ("display_order",)
