
# Create your models here.
from django.db import models
from django.template.defaultfilters import slugify


class AbstractDateTimeModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        "customuser.User",
        related_name="%(class)s_created_by",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    updated_by = models.ForeignKey(
        "customuser.User",
        related_name="%(class)s_updated_by",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True

    def soft_delete(self: 'AbstractDateTimeModel') -> None:
        self.is_deleted = True
        self.save()


class DropdownMaster(AbstractDateTimeModel):
    """Model for Master Data."""

    name = models.CharField(max_length=255, null=False, blank=False)
    slug = models.CharField(max_length=255, null=False, blank=False)
    ordering = ["name"]

    def save(self: 'DropdownMaster', *args: tuple, **kwargs: dict) -> None:
        self.slug = slugify(self.name)
        super(DropdownMaster, self).save(*args, **kwargs)

    def __str__(self: 'DropdownMaster') -> None:
        """Instance Representation."""
        return f"{self.slug}"


class DropdownValues(AbstractDateTimeModel):
    """Model for saving data according to master."""

    name = models.CharField(max_length=250)
    slug = models.CharField(max_length=200, null=True, blank=True)
    display_order = models.IntegerField(null=True, blank=True)
    dropdownmaster = models.ForeignKey(
        DropdownMaster,
        related_name="dropdownvalues",
        on_delete=models.PROTECT,
        related_query_name="dropdownvalue",
    )
    ordering = ["name"]

    def save(self: 'DropdownValues', *args: tuple, **kwargs: dict) -> None:
        if not self.slug:
            self.slug = slugify(self.name)
        super(DropdownValues, self).save(*args, **kwargs)

    def __str__(self: 'DropdownValues') -> str:
        """Instance Representation."""
        return f"{self.name}"


class FileUpload(AbstractDateTimeModel):
    """Saves FIle in model."""
    file = models.FileField(upload_to="uploads/file/", null=False, blank=False)
    is_active = models.BooleanField(default=True)

    def delete_file(self: 'FileUpload') -> None:
        """Delete file."""
        self.delete()


