from django.db.models import Q
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models import VolunteeringEvents, FundraiserEvents
from api.serializers.event_serializers import VolunteeringEventsSerializer, FundraiserEventsSerializer, \
    VolunteeringEventSerializer
from api.utilities.views_utilities import get_volunteering_spots, get_application_count_by_position


@api_view(["GET"])
def get_all_events(request):
    current_dt = timezone.now()
    fr_events = FundraiserEvents.objects.all().exclude(datetime__lt=current_dt, par1="", imgHero__isnull=False)
    fr_serializer = FundraiserEventsSerializer(fr_events, many=True)
    vol_events = VolunteeringEvents.objects.all().exclude(datetime__lt=current_dt, summary="", hide_event=True)
    vol_serializer = VolunteeringEventsSerializer(vol_events, many=True)
    return Response([*vol_serializer.data, *fr_serializer.data])


@api_view(["GET"])
def get_volunteering_event(request, PK):
    volunteering_event = VolunteeringEvents.objects.get(id=PK, hide_event=False)
    volunteering_spots = get_volunteering_spots(volunteering_event)
    application_count = get_application_count_by_position(volunteering_event)
    serializer = VolunteeringEventSerializer(volunteering_event, many=False)
    return Response({**serializer.data, **volunteering_spots, **application_count})


@api_view(["GET"])
def get_volunteering_events(request):
    events = VolunteeringEvents.objects.filter(hide_event=False)
    events_with_spots = []

    for event in events:
        volunteering_spots = get_volunteering_spots(event)
        application_count = get_application_count_by_position(event)
        event_serializer = VolunteeringEventsSerializer(event, many=False)
        events_with_spots.append({**event_serializer.data, **volunteering_spots, **application_count})
    return Response(events_with_spots)


@api_view(['GET'])
def filter_volunteering_events(request):
    """
    Endpoint for user profile page, retrieves events associated with the user.
    Note: the list with events is already confirmed, no need to reconfirm  it.
    """
    event_ids_str = request.GET.get('event_ids', '')
    event_ids = list(map(int, event_ids_str.split(','))) if event_ids_str else []

    events = VolunteeringEvents.objects.filter(
        id__in=event_ids,
        datetime__lt=timezone.now()
    ).exclude(Q(summary__isnull=True) | Q(summary__exact=''))
    serialized_events = VolunteeringEventsSerializer(events, many=True)
    return Response(serialized_events.data)


@api_view(["GET"])
def get_fundraiser_event(request, PK):
    event = FundraiserEvents.objects.get(id=PK, hide_event=False)
    serializer = FundraiserEventsSerializer(event, many=False)
    return Response(serializer.data)


@api_view(["GET"])
def get_fundraiser_events(request):
    events = FundraiserEvents.objects.filter(hide_event=False).order_by('datetime')
    serializer = FundraiserEventsSerializer(events, many=True)
    return Response(serializer.data)

