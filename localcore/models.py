from django.db import models
from django.utils.text import slugify

from .abstract_models import AbstractTimeStampedModel, AbstractNameFieldsModel,\
                            AbstractPhoneNumberFields


class Country(AbstractTimeStampedModel):
    english_name = models.CharField('English Name',
                                    max_length=100,
                                    blank=True,
                                    null=True)
    french_name = models.CharField('French Name',
                                    max_length=100,
                                    blank=True,
                                    null=True)
    code = models.CharField('Code',
                            max_length=20,
                            blank=True,
                            null=True)
    slug = models.SlugField('Slug',
                            max_length=50,
                            blank=50,
                            null=True)
    region = models.CharField('Region of a Continent',
                            max_length=100,
                            blank=True,
                            null=True)
    continent = models.CharField('Continent',
                            max_length=100,
                            blank=True,
                            null=True)

    def __repr__(self):
        return "Country Name: %s" % self.english_name

    def __str__(self):
        return self.code + " - " + self.english_name

    def _get_slug(self):
        return slugify(self.english_name)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_slug()
        super(Country, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"


class Province(AbstractTimeStampedModel, AbstractNameFieldsModel):
    country = models.ForeignKey(Country,
                            on_delete=models.CASCADE,
                            related_name="country_provinces",
                            db_index=True,
                            verbose_name="Province",
                            blank=True)

    def __repr__(self):
        return "Province: %s - %s" % (self.id, self.name)

    def __str__(self):
        return "Province: %s - %s" % (self.id, self.name)

    def _get_slug(self):
        return slugify(self.name)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_slug()
        super(Province, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Province"


class City(AbstractTimeStampedModel, AbstractNameFieldsModel):

    class CountryType(models.TextChoices):
        CONGO_KINSHASA = "0", "Congo(Kinshasa)"
        OTHER = "1", "ABROAD"

    country = models.ForeignKey(Country,
                            on_delete=models.CASCADE,
                            related_name="country_cities",
                            db_index=True,
                            blank=True,
                            null=True,
                            verbose_name="Country")

    #Abroad cities have province=null
    province = models.ForeignKey(Province,
                            on_delete=models.CASCADE,
                            related_name="province_cities",
                            db_index=True,
                            blank=True,
                            null=True,
                            verbose_name="Province")
    city_type = models.CharField(max_length=1,
                            choices=CountryType.choices)

    def __repr__(self):
        return "City: %s - %s" % (self.id, self.name)

    def __str__(self):
        return "City: %s - %s" % (self.id, self.name)

    def _get_slug(self):
        return slugify(self.id + " " + self.name)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_slug()
        super(City, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "City"


class Commune(AbstractTimeStampedModel, AbstractNameFieldsModel):
    city = models.ForeignKey(City,
                            on_delete=models.CASCADE,
                            related_name="city_commune",
                            db_index=True,
                            verbose_name="Commune",
                            blank=True,
                            null=True)

    def __repr__(self):
        return "Commune: %s - %s" % (self.id, self.name)

    def __str__(self):
        return "Commune: %s - %s" % (self.id, self.name)

    def _get_slug(self):
        return slugify(self.name)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_slug()
        super(Commune, self).save(*args, **kwargs)


class Address(models.Model):

    class CountryType(models.TextChoices):
        CONGO_KINSHASA = "0", "Congo(Kinshasa)"
        OTHER = "1", "ABROAD"

    street = models.CharField("Street",
                            max_length=50,
                            blank=True,
                            null=True)
    city = models.ForeignKey(City,
                            on_delete=models.CASCADE,
                            related_name="city_addresses",
                            db_index=True,
                            verbose_name="City",
                            blank=True,
                            null=True)
    city_origin = models.CharField("City",
                            max_length=50,
                            blank=True,
                            null=True)
    commune = models.ForeignKey(Commune,
                            on_delete=models.CASCADE,
                            related_name="commune_addresses",
                            db_index=True,
                            verbose_name="Commune",
                            blank=True,
                            null=True)
    province = models.ForeignKey(Province,
                            on_delete=models.CASCADE,
                            related_name="province_addresses",
                            db_index=True,
                            verbose_name="Province",
                            blank=True,
                            null=True)
    country = models.ForeignKey(Country,
                            on_delete=models.CASCADE,
                            related_name="country_addresses",
                            db_index=True,
                            verbose_name="Country",
                            blank=True,
                            null=True)
    country_type = models.CharField(max_length=1,
                            choices=CountryType.choices)

    def __repr__(self):
        return "address_id: %s, country: %s, street: %s" % \
                (self.id, self.country, self.street)

    def __str__(self):
        return "address_id: %s, country: %s, street: %s" % \
                (self.id, self.country, self.street)

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"

