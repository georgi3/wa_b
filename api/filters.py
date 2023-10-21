from datetime import datetime
from django.contrib.admin import SimpleListFilter
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class EventDateFilter(SimpleListFilter):
    title = _('event date')
    parameter_name = 'event_date'  # URL query parameter that will be used when the filter is applied.

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples in which the first element is the coded value
        for the option and the second element is the human-readable name for the option.
        """
        return (
            ('past', _('Past')),
            ('upcoming', _('Upcoming')),
        )

    def queryset(self, request, queryset):
        """
        Modify the queryset based on user's selection.
        """
        if self.value() == 'past':
            return queryset.filter(datetime__lt=datetime.today())
        if self.value() == 'upcoming':
            return queryset.filter(datetime__gte=datetime.today())


class EventStatusFilter(SimpleListFilter):
    title = 'Event Status'  # Human-readable title to appear in the admin
    parameter_name = 'status'  # URL query parameter

    def lookups(self, request, model_admin):
        # Define the filter options
        return (
            ('incomplete', 'Incomplete Event'),
            ('complete', 'Complete Event'),
        )

    def queryset(self, request, queryset):
        # Filter based on the provided parameters
        now = timezone.now()

        if self.value() == 'incomplete':
            return queryset.filter(summary__isnull=True, datetime__lte=now)

        if self.value() == 'complete':
            return queryset.filter(summary__isnull=False, datetime__lte=now)

        return queryset


class CompleteFundraiserFilter(SimpleListFilter):
    title = 'Fundraiser Completion'
    parameter_name = 'complete_fundraiser'

    def lookups(self, request, model_admin):
        return (
            ('complete', 'Complete'),
            ('incomplete', 'Incomplete'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'complete':
            return queryset.filter(
                datetime__lte=timezone.now(),
                imgHero__isnull=False,
                par1__isnull=False,
            ).exclude(
                imgHero__exact='',
                par1__exact='',
            )
        if self.value() == 'incomplete':
            return queryset.filter(
                datetime__lte=timezone.now(),
            ).filter(
                Q(imgHero__isnull=True) | Q(imgHero__exact=''),
                Q(par1__isnull=True) | Q(par1__exact=''),
            )

