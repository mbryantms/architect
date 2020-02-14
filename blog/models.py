from django.db import models
from django_postgres_unlimited_varchar import UnlimitedCharField
from django.utils import timezone


class Tag(models.Model):
    tag = models.SlugField(unique=True)

    def __str__(self):
        return self.tag


class BaseModel(models.Model):
    created = models.DateTimeField(default=timezone.now)
    tags = models.ManyToManyField(Tag, blank=True)
    slug = models.SlugField(max_length=64)

    # TODO: Add longitude & latitude to base model

    class Meta:
        abstract = True
        ordering = ("-created",)


class Series(models.Model):
    title = UnlimitedCharField()
    slug = models.SlugField()
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "series"

    def __str__(self):
        return self.title


class Entry(BaseModel):
    title = models.CharField(max_length=255, blank=True)
    body = models.TextField()

    tweet_html = models.TextField(
        blank=True,
        null=True,
        help_text="""
        Paste in the embed tweet HTML, minus the script tag, 
        to display a tweet in the sidebar next to this entry.
        """.strip(),
    )

    extra_head_html = models.TextField(
        blank=True,
        null=True,
        help_text="""
        Extra HTML to be included in the &lt;head&gt; for this entry.
        """.strip(),
    )

    series = models.ForeignKey(
        Series, related_name="entries", blank=True, null=True, on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Entries"


class Quotation(BaseModel):
    quotation = models.TextField()
    source = models.CharField(max_length=255)
    source_url = UnlimitedCharField(blank=True, null=True)

    def __str__(self):
        return self.quotation


class Blogmark(BaseModel):
    link_url = models.URLField(max_length=1000)
    link_title = models.CharField(max_length=255)
    via_url = models.URLField(blank=True, null=True)
    via_title = models.CharField(max_length=255, blank=True, null=True)
    commentary = models.TextField()

    def __str__(self):
        return self.link_title


class Photo(BaseModel):
    photo = models.ImageField(upload_to="photos/%Y/%M")
    title = UnlimitedCharField(blank=True)

    def __str__(self):
        return self.title
