from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _, get_language
from django.urls import reverse
from django.core.cache import cache

from modelcluster.fields import ParentalKey

from wagtail.core import blocks
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField, StreamField
from wagtail.images.blocks import ImageChooserBlock

from treebeard.mp_tree import MP_Node

from localcore.abstract_models import AbstractPhoneNumberFields,\
                                    AbstractTimeStampedModel, \
                                    AbstractNameFieldsModel
from localcore.models import Address, Country

import json
import sys
import traceback


#Generate choices from country id and english name
#The querie should be in queries_utils
NATIONALITY_CHOICES = (("", ""), ("", ""))


def project_videos_path(instance, filename=""):
    return "assets/projects/videos/{0}/".format(instance.slug)


def project_images_path(instance, filename=""):
    return "assets/projects/videos/{0}/".format(instance.slug)


def get_site_root_page():
    try:
        home_page = Page.objects.get(slug="home")
        print("IN GET HOME PAGE")
        print(home_page)
    except Exception:
        home_page = None

    if not home_page:
        try:
            print("IN CREATE HOME PAGE")
            home_page = Page.add_root(
                title="home",
                slug="home",
                url_path="/"
            )
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)
    return home_page


class ProjectSponsor(AbstractTimeStampedModel, AbstractPhoneNumberFields):

    class SponsorType(models.TextChoices):
        BUSINESS = "0", "Business"
        INDIVIDUAL = "1", "Individual"

    class SponsorLocalization(models.TextChoices):
        CONGO_KINSHASA = "0", "Congo(Kinshasa)"
        OTHER = "1", "ABROAD"

    auth_user = models.OneToOneField(User,
                                    on_delete=models.CASCADE,
                                    related_name="project_sponsor_user")
    middle_name = models.CharField("Middlename",
                                    max_length=50,
                                    blank=True,
                                    null=True)
    address = models.ForeignKey(Address,
                                on_delete=models.CASCADE,
                                related_name="project_sponsor_address",
                                db_index=True,
                                verbose_name="Address",
                                blank=True,
                                null=True)
    sponsor_type = models.CharField("Sponsor Type",
                            max_length=1,
                            choices=SponsorType.choices)
    company_name = models.CharField("Company Name",
                                     max_length=50,
                                     blank=True,
                                     null=True)
    company_description = RichTextField("Company Presentation",
                                    blank=True,
                                    null=True)
    country_origin = models.ForeignKey(Country,
                                    on_delete=models.CASCADE,
                                    related_name="sponsor_country_origin",
                                    db_index=True,
                                    verbose_name="Country Origin",
                                    blank=True,
                                    null=True)
    city_origin = models.CharField("City Origin",
                                    max_length=50,
                                    blank=True,
                                    null=True)
    company_logo = models.ImageField("Upload Company Logo",
                                    upload_to="assets/img/sponsors",
                                    max_length=256)
    localization = models.CharField("Localization(R.D.Congo/Abroad)",
                                    max_length=1,
                                    choices=SponsorLocalization.choices)

    @property
    def sponsor_full_name(self):
        try:
            first_name = self.auth_user.first_name
        except Exception:
            first_name = ""
        try:
            last_name = self.auth_user.last_name
        except Exception:
            last_name = ""
        return "{} {} {}".format(first_name, self.middle_name, last_name)

    @property
    def sponsor_logo_filename(self):
        return self.company_logo.path

    def __repr__(self):
        try:
            username = self.auth_user.username
        except Exception:
            username = ""
        return "ID: %s -- Username: % s -- Company: %s" % (
                        self.id, username, self.company_name)

    def __str__(self):
        try:
            username = self.auth_user.username
        except Exception:
            username = ""
        return "ID: %s -- Username: % s -- Company: %s" % (
                        self.id, username, self.company_name)

    class Meta:
        verbose_name = "Sponsor"
        verbose_name_plural = "Sponsors"


class SponsorBlock(blocks.StructBlock):
    page_header = blocks.CharBlock(classname="full title")
    sponsor_name = blocks.CharBlock()
    description = blocks.RichTextBlock()
    sidebar = blocks.RichTextBlock()
    page_footer = blocks.CharBlock()

    def set_sponsor_block(self, block_data={}):
        self.page_header = block_data.get("page_header", "")
        self.sponsor_name = block_data.get("sponsor_name", "")
        self.description = block_data.get("description", "")
        self.sidebar = block_data.get("sidebar", "")
        self.page_footer = block_data.get("page_footer", "")

        return


class SponsorPage(AbstractTimeStampedModel):
    sponsor_page_id = models.BigAutoField(primary_key=True)
    page = models.OneToOneField(Page,
                                on_delete=models.CASCADE,
                                related_name="sponsorpage_page",
                                null=True)
    project_sponsor = models.ForeignKey(ProjectSponsor,
                            on_delete=models.SET_NULL,
                            related_name="page_project_sponsors",
                            db_index=True,
                            blank=True,
                            null=True)
    body = StreamField([
            ('heading', blocks.CharBlock(classname="full title")),
            ('image', ImageChooserBlock()),
            ('description', blocks.RichTextBlock()),
        ], null=True, blank=True)
    use_home_template = models.BooleanField(default=False)
    use_own_template = models.BooleanField(default=False)
    is_home_page = models.BooleanField(default=False)

    parent_page_types = []
    subpage_types = ['SponsorPage']

    def set_page_slug(self):
        try:
            company_name = self.project_sponsor.company_name
        except Exception:
            company_name = ""
        try:
            sponsor_name = self.project_sponsor.full_name
        except Exception:
            sponsor_name = ""
        if company_name:
            self.slug = slugify(company_name)
            return True
        if sponsor_name:
            self.slug = slugify(sponsor_name)
            return True
        return False

    def set_page_title(self):
        try:
            company_name = self.project_sponsor.company_name
        except Exception:
            company_name = ""
        try:
            sponsor_name = self.project_sponsor.full_name
        except Exception:
            sponsor_name = ""
        if company_name:
            self.title = company_name
            return True
        if sponsor_name:
            self.title = sponsor_name
            return True
        return False

    def get_template(self, request):
        if self.use_home_template:
            return "localaccount/sponsors_home.html"
        return "domeproject/sponsors_page.html"

    def get_context(self, request):
        context = super().get_context(request)
        return context

    class Meta:
        verbose_name = "Sponsor Page"
        verbose_name_plural = "Sponsors Pages"

"""
class SponsorHomePage(Page):

    template = "localaccount/sponsors_home.html"

    #parent_page_types = []
    #subpage_types = ['SponsorPage']

    def get_context(self, request):
        context = super().get_context(request)
        #try:
        #    sponsors_pages = SponsorPage.objects.child_of(self).live()
        #except Exception:
        #    sponsors_pages = None
        #    exc_type, exc_value, exc_traceback = sys.exc_info()
        #    traceback.print_exception(exc_type, exc_value, exc_traceback)

        #context['sponsors_pages'] = sponsors_pages
        return context
"""

def get_sponsors_home_page():
    try:
        sponsors_home = SponsorPage.objects.get(is_home_page=True)
    except Exception:
        sponsors_home = None

    print("IN GET SPONSOR HOME")
    print(sponsors_home)

    if not sponsors_home:
        site_root = get_site_root_page()
        if site_root:
            print("GOTTEN SITE ROOT")
            print(site_root)
            try:
                page = site_root.add_child(
                        title="Sponsors' Space",
                        slug=slugify("Sponsors' Space")
                    )
                print("TRYING TO ADD CHILD")
                print(page)
            except Exception:
                page = None
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback.print_exception(exc_type, exc_value, exc_traceback)

        try:
            sponsors_home = SponsorPage()
            sponsors_home.page = page
            sponsors_home.use_home_template = True
            sponsors_home.is_home_page = True
            sponsors_home.save()
        except Exception:
            sponsors_home = None
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)
    return sponsors_home


class ProjectInitiator(AbstractTimeStampedModel, AbstractPhoneNumberFields):
    class InitiatorType(models.TextChoices):
        REALISATOR = "0", "Realisator"
        PRODUCER = "1", "Producer"

    auth_user = models.OneToOneField(User,
                                    on_delete=models.CASCADE,
                                    related_name="project_initiator_user")
    middle_name = models.CharField("Middlename",
                                    max_length=50,
                                    blank=True,
                                    null=True)
    address = models.ForeignKey(Address,
                                on_delete=models.CASCADE,
                                related_name="project_initiator_address",
                                db_index=True,
                                verbose_name="Address",
                                blank=True,
                                null=True)
    initiator_type = models.CharField("Initiator Type",
                            max_length=1,
                            choices=InitiatorType.choices)
    languages_spoken = models.CharField("Languages Spoken",
                                    max_length=100,
                                    blank=True,
                                    null=True)
    nationality = models.CharField("Nationality",
                                    max_length=100,
                                    choices=NATIONALITY_CHOICES,
                                    blank=True,
                                    null=True)
    birth_date = models.DateField("Date of Birth",
                                    blank=True,
                                    null=True)
    years_experience = models.IntegerField("Years of Experience",
                                    blank=True,
                                    null=True)
    curriculum_vitea = RichTextField("Curriculum Vitae")
    awards = models.CharField("Awards won",
                                max_length=256,
                                blank=True,
                                null=True)
    photo = models.ImageField("Initiator Photo",
                                upload_to=project_images_path,
                                max_length=255,
                                blank=True,
                                null=True)

    def __repr__(self):
        try:
            user_id = self.auth_user.id
        except Exception:
            user_id = ""
        return "ID: %s -- User ID: % s " % (self.id, user_id)

    def __str__(self):
        try:
            user_id = self.auth_user.id
        except Exception:
            user_id = ""
        return "ID: %s -- User ID: % s " % (self.id, user_id)

    class Meta:
        verbose_name = "Initiator"
        verbose_name_plural = "Initiators"


class Category(MP_Node):
    name = models.CharField('Name',
                            max_length=255,
                            db_index=True,
                            blank=True,
                            null=True)
    code = models.CharField('Code',
                            max_length=50,
                            blank=True,
                            null=True)
    description = models.TextField('Description',
                            blank=True,
                            null=True)
    image = models.ImageField('Image',
                            upload_to='assets/projects/categories',
                            blank=True,
                            null=True,
                            max_length=255)
    slug = models.SlugField('Slug',
                            max_length=255,
                            blank=True,
                            null=True)

    _slug_separator = '/'
    _full_name_separator = ' > '

    def __str__(self):
        return 'Category: {}'.format(self.name)

    @property
    def full_name(self):
        names = [category.name for category in self.get_ancestor_and_self()]
        return self._full_name_separator.join(names)

    @property
    def full_slug(self):
        slugs = [category.slug for category in self.get_ancestor_and_self()]
        return self._slug_separator.join(slugs)

    def generate_slug(self):
        return slugify(self.name)

    def ensure_slug_uniqueness(self):
        unique_slug = self.slug
        siblings = self.get_siblings().exclude(pk=self.pk)
        next_num = 2
        while siblings.filter(slug=unique_slug).exists():
            unique_slug = '{slug}_{end}'.format(slug=self.slug, end=next_num)
            next_num += 1

        if unique_slug != self.slug:
            self.slug = unique_slug
            self.save()

    def save(self, *args, **kwargs):
        if self.slug:
            super(Category, self).save(*args, **kwargs)
        else:
            self.slug = self.SponsorPagegenerate_slug()
            super(Category, self).save(*args, **kwargs)
            self.ensure_slug_uniqueness()

    def get_ancestor_and_self(self):
        return list(self.get_ancestors()) + [self]

    def get_absolute_url(self):
        current_locale = get_language()
        cache_key = 'CATEGORY_URL_%s_%s' % (current_locale, self.pk)
        url = cache.get(cache_key)
        if not url:
            url = reverse(
                    'project_category',
                    kwargs={'category_slug': self.full_slug, 'pk': self.pk})
            cache.set(cache_key, url)
        return url

    def has_children(self):
        return self.get_num_children() > 0

    def get_num_children(self):
        return self.get_children().count()

    class Meta:
            ordering = ['path']
            verbose_name = 'Category'
            verbose_name_plural = 'Categories'


class ProjectFormat(AbstractTimeStampedModel, AbstractNameFieldsModel):
    pass


class ProjectGenre(AbstractTimeStampedModel, AbstractNameFieldsModel):
    pass


class Project(AbstractTimeStampedModel):
    title = models.CharField("Title",
                            max_length=255,
                            blank=True,
                            null=True)
    slug = models.SlugField("Slug",
                            max_length=255,
                            blank=True,
                            null=True)
    initiator = models.ForeignKey(
                            ProjectInitiator,
                            related_name="initiator_projects",
                            on_delete=models.CASCADE,
                            blank=True,
                            null=True,
                            verbose_name="Project Initiator")
    co_initiators = models.ManyToManyField(ProjectInitiator)
    presentation = models.TextField("Presentation",
                            blank=True,
                            null=True)
    budget_estimate = models.DecimalField("Budget Estimate",
                            max_digits=12,
                            decimal_places=2)
    start_date_estimate = models.DateField("Estimated Start Date",
                            auto_now=False,
                            auto_now_add=False)
    end_date_estimate = models.DateField("Estimated End Date",
                            auto_now=False,
                            auto_now_add=False)
    categories = models.ManyToManyField(Category,
                            through="ProjectCategory",
                            verbose_name="Categories")
    genres = models.ManyToManyField(ProjectGenre,
                            through="ProjectThroughGenre",
                            verbose_name="Genres of Project")
    project_format = models.ForeignKey(ProjectFormat,
                            on_delete=models.CASCADE,
                            related_name="format_of_projects",
                            db_index=True,
                            blank=True,
                            null=True,
                            verbose_name="Format of Projects")
    scenario = models.TextField("Scenario",
                            blank=True,
                            null=True)
    synopsis = models.TextField("Synopsis",
                            blank=True,
                            null=True)
    summary = models.TextField("Summary",
                            blank=True,
                            null=True)
    statement_intent = models.TextField("Statement of Intent",
                            blank=True,
                            null=True)
    pitch_video = models.FileField(
                            upload_to=project_videos_path,
                            max_length=255,
                            blank=True,
                            null=True)
    trailer_video = models.FileField(
                            upload_to=project_videos_path,
                            max_length=255,
                            blank=True,
                            null=True)
    poster = models.ImageField(
                            upload_to=project_images_path,
                            max_length=255,
                            blank=True,
                            null=True)
    location = models.CharField("Project Location",
                            max_length=255,
                            blank=True,
                            null=True)
    web_address = models.URLField("Web Address",
                            max_length=255,
                            blank=True,
                            null=True)

    def _get_slug(self):
        try:
            initiator_id = self.initiator.auth_user.id
        except Exception:
            initiator_id = ""
        if initiator_id:
            slug = "{0} {1}".format(self.title, initiator_id)
            return slugify(slug)
        else:
            return ""

    def __repr__(self):
        return "ID: {0} - Title: {1}".format(self.id, self.title)

    def __str__(self):
        return "ID: {0} - Title: {1}".format(self.id, self.title)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_slug()
        super(Project, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"


class ProjectCategory(models.Model):
    project = models.ForeignKey(
                Project,
                on_delete=models.CASCADE,
                null=True,
                blank=True,
                verbose_name="Project")
    category = models.ForeignKey(
                Category,
                on_delete=models.CASCADE,
                null=True,
                blank=True,
                verbose_name="Category")

    class Meta:
        ordering = ['project', 'category']
        unique_together = ('project', 'category')
        verbose_name = ('Project Category')

    def __repr__(self):
        return "Project ID: {0}, Category ID: {1}".format(self.project.id,
                                                            self.category.id)

    def __str__(self):
        return "Project ID: {0}, Category ID: {1}".format(self.project.id,
                                                            self.category.id)


class ProjectThroughGenre(models.Model):
    project = models.ForeignKey(
                Project,
                on_delete=models.CASCADE,
                verbose_name="Project")
    genre = models.ForeignKey(
                ProjectGenre,
                on_delete=models.CASCADE,
                verbose_name="Project Genre")

    def __repr__(self):
        return "Project ID: {0}, Genre ID: {1}".format(self.project.id,
                                                            self.genre.id)

    def __str__(self):
        return "Project ID: {0}, Genre ID: {1}".format(self.project.id,
                                                            self.genre.id)

    class Meta:
        ordering = ["project", "genre"]
        unique_together = ('project', "genre")
        verbose_name = ("Project Genre")


class IndependentCineaste(AbstractTimeStampedModel, AbstractPhoneNumberFields):
    auth_user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name="cineaste_user")
    middlename = models.CharField("Middle Name",
                                max_length=255,
                                blank=True,
                                null=True)
    address = models.ForeignKey(Address,
                                on_delete=models.CASCADE,
                                related_name="cineaste_address",
                                db_index=True,
                                verbose_name="Address",
                                blank=True,
                                null=True)
    awards = models.CharField("Awards",
                                max_length=255,
                                blank=True,
                                null=True)
    curriculum_vitae = models.TextField("Curriculum Vitae",
                                blank=True,
                                null=True)
    birth_date = models.DateField("Date of Birth",
                                auto_now=False,
                                auto_now_add=False)
    nationality = models.CharField("Nationality",
                                max_length=100,
                                choices=NATIONALITY_CHOICES,
                                blank=True,
                                null=True)

    def __str__(self):
        return "Cineaste ID: {0} User ID: {1}".format(self.id,
                                                        self.auth_user.id)

    def __repr__(self):
        return "Cineaste ID: {0} User ID: {1}".format(self.id,
                                                        self.auth_user.id)


@receiver(post_save, sender=ProjectSponsor, dispatch_uid="save_sponsor_page")
def save_project_sponsor_page(sender, instance, **kwargs):
    sponsor_page = None
    sponsors_home = get_sponsors_home_page()
    if sponsors_home:
        try:
            sponsor_page = SponsorPage()
            sponsor_page.project_sponsor = instance
            sponsor_page.body = json.dumps([
                {"type": "heading", "value": sponsor_page.set_page_title()},
                {"type": "image", "value": instance.sponsor_logo_filename},
                {"type": "description", "value": instance.company_description}
            ])
            #sponsor_page = sponsors_home.add_child(instance=sponsor_page)
            sponsor_page.set_page_title()
            sponsor_page.set_page_slug()
            sponsor_page.page = sponsors_home.page.add_child(
                    title=sponsor_page.title,
                    slug=sponsor_page.slug,
                    url_path="localaccount/{}/".format(sponsor_page.slug)
                )
            sponsor_page.save()
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)

    return sponsor_page
