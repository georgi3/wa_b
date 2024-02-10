from datetime import datetime
from api.models import VolunteerAssignment


def get_application_count_by_position(event):
    application_count = dict()
    positions = ['Driver', "Cook", "Server", "Dishwasher", "Photographer"]
    for pos in positions:
        application_count[f"{pos.lower()}_count"] = len(VolunteerAssignment.objects.filter(volunteering_event=event,
                                                                                           assigned_position=pos))
    return application_count


def get_volunteering_spots(event):
    """
    Utility function for displaying volunteering events.
    Used by views: get_volunteering_events(), get_volunteering_event()
    :returns number of free positions for each position
    """
    existing_drivers_count = VolunteerAssignment.objects.filter(
        volunteering_event=event,
        assigned_position="Driver",
        approve_participation=True
    ).count()

    existing_cooks_count = VolunteerAssignment.objects.filter(
        volunteering_event=event,
        assigned_position="Cook",
        approve_participation=True
    ).count()

    existing_servers_count = VolunteerAssignment.objects.filter(
        volunteering_event=event,
        assigned_position="Server",
        approve_participation=True
    ).count()

    existing_dishwashers_count = VolunteerAssignment.objects.filter(
        volunteering_event=event,
        assigned_position="Dishwasher",
        approve_participation=True
    ).count()

    existing_photographers_count = VolunteerAssignment.objects.filter(
        volunteering_event=event,
        assigned_position="Photographer",
        approve_participation=True
    ).count()

    return {
        "drivers_left": event.driver_num - existing_drivers_count,
        "cooks_left": event.cook_num - existing_cooks_count,
        "servers_left": event.servers_num - existing_servers_count,
        "dishwashers_left": event.dishwashers_num - existing_dishwashers_count,
        "photographers_left": event.photographers_num - existing_photographers_count,
    }


def is_position_full(event, position, position_limit):
    """
    Utility function for volunteer_application() view
    :param event:
    :param position:
    :param position_limit:
    :return:
    """
    count = VolunteerAssignment.objects.filter(
        volunteering_event=event,
        assigned_position=position,
        approve_participation=True
    ).count()
    return count >= position_limit


def apply_volunteer(event, position, volunteer):
    """
    Utility function for volunteer_application() view
    :param event:
    :param position:
    :param volunteer:
    :return:
    """
    VolunteerAssignment.objects.create(
        volunteering_event=event,
        assigned_position=position,
        volunteer=volunteer,
        approve_participation=False,
        confirm_participation=False,
        volunteering_hours=2,
    )


def add_position_to_profile(position, volunteer):
    """Adds Position to volunteers profile if applied"""
    if position == "Driver":
        volunteer.is_driver = True
    elif position == "Cook":
        volunteer.is_cook = True
    elif position == "Server":
        volunteer.is_server = True
    elif position == "Dishwasher":
        volunteer.is_dishwasher = True
    elif position == "Photographer":
        volunteer.is_photographer = True
    volunteer.save()


def update_last_application_date(volunteer):
    volunteer.last_applied = datetime.now().date()
    volunteer.save()


def create_update_fields_dict(*values):
    phone, organization, car_type, address, zip_code = values
    update_fields = {}
    if phone:
        update_fields['phone'] = phone
    if organization:
        update_fields['organization'] = organization
    if car_type:
        update_fields['car_type'] = car_type
    if address:
        update_fields['address'] = address
    if zip_code:
        update_fields['zip_code'] = zip_code
    return update_fields
