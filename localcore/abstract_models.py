# -*- coding: utf-8 -*-
from django.db import models
from django.utils.text import slugify

from phonenumber_field.modelfields import PhoneNumberField


class AbstractTimeStampedModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True,
                                        blank=True,
                                        null=True)
    modified_date = models.DateTimeField(auto_now=True,
                                        blank=True,
                                        null=True)

    class Meta:
        abstract = True


class AbstractNameFieldsModel(models.Model):
    code = models.CharField('Code',
                            max_length=50,
                            blank=True)
    name = models.CharField('Name',
                            max_length=50,
                            blank=True,
                            null=True)
    slug = models.SlugField('Slug',
                            max_length=50,
                            blank=50,
                            null=True)
    description = models.TextField('Description',
                            max_length=250,
                            blank=True,
                            null=True)

    def _get_slug(self):
        return slugify(self.name)

    def __repr__(self):
        return "slug: %s" % (self.slug)

    def __str__(self):
        return "%s -- %s -- %s" % (self.code, self.name, self.slug)

    class Meta:
        abstract = True


class AbstractPhoneNumberFields(models.Model):
    phone_number_1 = PhoneNumberField(blank=True, null=True)
    phone_number_2 = PhoneNumberField(blank=True, null=True)

    class Meta:
        abstract = True
