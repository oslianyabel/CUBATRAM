from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class Category(models.Model):
    """Modelo para categorías de excursiones (ej: Adventure Tours, Popular Destinations)"""

    title = models.CharField(max_length=100, blank=True)
    slug = models.SlugField(max_length=100, unique=True)
    subtitle = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to="categories/", blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["display_order", "title"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)


class Destination(models.Model):
    """Modelo para los destinos turísticos (ej: Havana, Varadero Beach)"""

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="destinations/")
    is_active = models.BooleanField(default=True)
    is_popular = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class TourImage(models.Model):
    """Imágenes adicionales para los tours"""

    image = models.ImageField(upload_to="tour_images/")
    caption = models.CharField(max_length=200, blank=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order"]

    def __str__(self):
        return f"Tour Image #{self.id}"  # type: ignore


class Tour(models.Model):
    """Modelo principal para las excursiones"""

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    short_description = models.CharField(max_length=300)
    description = models.TextField()
    categories = models.ManyToManyField(Category, related_name="tours")
    destinations = models.ManyToManyField(Destination, related_name="tours")
    images = models.ManyToManyField(TourImage, related_name="tours")
    adult_price = models.DecimalField(
        max_digits=8, decimal_places=2, validators=[MinValueValidator(0)]
    )
    child_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
    )
    duration = models.CharField(
        max_length=50, help_text="Duración del tour (ej: 4 horas, 1 día)"
    )
    main_image = models.ImageField(upload_to="tours/")
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-is_featured", "title"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class HeroSection(models.Model):
    """Modelo para la sección hero de la página principal"""

    name = models.CharField(max_length=50)
    background_image = models.ImageField(upload_to="hero/")
    title1 = models.CharField(max_length=200)
    title2 = models.CharField(max_length=200)
    title3 = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order"]
        verbose_name = "Hero Section"
        verbose_name_plural = "Hero Sections"

    def __str__(self):
        return f"Hero Section #{self.display_order} {self.name}"


class InfoSection(models.Model):
    """Modelo para la sección de información de la página principal"""

    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200)
    content = models.TextField()
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Info Section"
        verbose_name_plural = "Info Sections"

    def __str__(self):
        return self.title


class InfoPoint(models.Model):
    """Puntos de información dentro de la info section"""

    info_section = models.ForeignKey(
        InfoSection, on_delete=models.CASCADE, related_name="points"
    )
    icon = models.CharField(
        max_length=50, help_text="Nombre del icono SVG (ej: heart.svg)"
    )
    content = models.TextField()
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order"]

    def __str__(self):
        return f"Info Point #{self.display_order}"


class SpecialOffer(models.Model):
    """Modelo para ofertas especiales que aparecen en el footer"""

    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="special_offers/")
    description = models.TextField(blank=True)
    discount_percentage = models.PositiveIntegerField(blank=True, null=True)
    valid_from = models.DateField()
    valid_to = models.DateField()
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-valid_from"]

    def __str__(self):
        return self.title

    def is_currently_active(self):
        today = timezone.now().date()
        return self.valid_from <= today <= self.valid_to


class Booking(models.Model):
    """Modelo para las reservas de tours"""

    tour = models.ForeignKey(Tour, on_delete=models.PROTECT, related_name="bookings")
    email = models.EmailField()
    date = models.DateField()
    time = models.TimeField()
    adults = models.PositiveIntegerField(default=1)
    children = models.PositiveIntegerField(default=0)
    special_requests = models.TextField(blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Reserva #{self.id} - {self.tour.title}"  # type: ignore

    def calculate_total_price(self):
        total = self.adults * self.tour.adult_price
        if self.tour.child_price and self.children > 0:
            total += self.children * self.tour.child_price
        return total

    def save(self, *args, **kwargs):
        if not self.total_price:
            self.total_price = self.calculate_total_price()
        super().save(*args, **kwargs)


class ContactInfo(models.Model):
    """Información de contacto para el footer"""

    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Contact Information"

    def __str__(self):
        return "Contact Information"


class SocialMediaLink(models.Model):
    """Redes sociales para el footer"""

    name = models.CharField(max_length=50)
    url = models.URLField()
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order"]

    def __str__(self):
        return self.name
