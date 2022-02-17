"""Database models."""
from djongo import models


class Entry(models.Model):
    id = models.ObjectIdField(db_column='_id', primary_key=True)
    text = models.CharField(
        max_length=255,
        verbose_name='Entry text')
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created',
        help_text='Date when entry was created')

    class Meta:
        """Table information."""

        managed = False
        verbose_name = 'Entry'
        verbose_name_plural = 'Entries'

    def __str__(self):
        return f'<{self.id}>: {self.text[:10]}...'
