from django.contrib import admin
from .models import Entry, Quotation, Blogmark, Series, Photo, Tag
from django import forms


class BaseAdmin(admin.ModelAdmin):
    date_hierarchy = "created"
    list_display = ("__str__", "slug", "created")


class MyEntryForm(forms.ModelForm):
    def clean_body(self):
        body = self.cleaned_data["body"]
        try:
            ElementTree.fromstring("<entry>%s</entry>" % body)
        except Exception as e:
            raise forms.ValidationError(str(e))
        return body


@admin.register(Entry)
class EntryAdmin(BaseAdmin):
    search_fields = ("tags__tag", "title", "body")
    form = MyEntryForm
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Quotation)
class QuotationAdmin(BaseAdmin):
    search_fields = ("tags__tag", "quotation")
    prepopulated_fields = {"slug": ("source",)}


@admin.register(Blogmark)
class BlogmarkAdmin(BaseAdmin):
    search_fields = ("tags__tag", "commentary")
    prepopulated_fields = {"slug": ("link_title",)}


@admin.register(Photo)
class PhotoAdmin(BaseAdmin):
    search_fields = ("tags__tag", "title")


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ("tag",)

    def get_search_results(self, request, queryset, search_term):
        search_term = search_term.strip()
        if search_term:
            return (
                queryset.filter(tag__icontains=search_term)
                .annotate(tag_length=Length("tag"))
                .order_by("tag_length"),
                False,
            )
        else:
            return queryset.none(), False


@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
