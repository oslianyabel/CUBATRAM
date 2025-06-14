from django.shortcuts import render
from django.views.generic import ListView

from .models import (
    Category,
    ContactInfo,
    Destination,
    HeroSection,
    InfoSection,
    SocialMediaLink,
    SpecialOffer,
    Tour,
)


class TourListView(ListView):
    model = Tour
    template_name = "tours/tour_list.html"
    context_object_name = "tours"
    paginate_by = 9

    def get_queryset(self):
        queryset = super().get_queryset().filter(is_active=True)

        # Filtro por categoría
        category_slug = self.request.GET.get("category")
        if category_slug:
            queryset = queryset.filter(categories__slug=category_slug)

        # Filtro por destino
        destination_slug = self.request.GET.get("destination")
        if destination_slug:
            queryset = queryset.filter(destinations__slug=destination_slug)

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.filter(is_featured=True)
        context["destinations"] = Destination.objects.filter(is_active=True)
        return context


def home(request):
    hero_section = HeroSection.objects.filter(is_active=True).first()

    categories = Category.objects.all()
    destinations = Destination.objects.all()

    featured_categories = Category.objects.filter(is_featured=True)

    popular_destinations = (
        Destination.objects.filter(is_active=True)
        .filter(is_popular=True)
        .order_by("?")[:6]
    )

    adventure_category = Category.objects.filter(slug="adventure").first()
    adventure_tours = Tour.objects.filter(is_active=True)
    if adventure_category:
        adventure_tours = adventure_tours.filter(categories=adventure_category)

    featured_tours = Tour.objects.filter(is_featured=True, is_active=True)[:4]

    info_section = InfoSection.objects.filter(is_active=True).first()

    special_offers = SpecialOffer.objects.filter(is_active=True)[:3]

    contact_info = ContactInfo.objects.first()

    social_media = SocialMediaLink.objects.all().order_by("display_order")

    context = {
        "categories": categories,
        "destinations": destinations,
        "hero_section": hero_section,
        "featured_categories": featured_categories,
        "popular_destinations": popular_destinations,
        "adventure_tours": adventure_tours,
        "featured_tours": featured_tours,
        "info_section": info_section,
        "special_offers": special_offers,
        "contact_info": contact_info,
        "social_media": social_media,
    }
    return render(request, "home/home.html", context)
