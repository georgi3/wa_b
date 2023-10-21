import gspread
import pandas as pd
from django.http import HttpResponse
from oauth2client.service_account import ServiceAccountCredentials

from api.models import VolunteerAssignment


def hide_published_events(modeladmin, request, queryset):
    queryset.update(hide_event=True)


def publish_hidden_events(modeladmin, request, queryset):
    queryset.update(hide_event=False)


def prepare_volunteers_export(queryset):
    df = pd.DataFrame.from_records(queryset.values())
    df["joined_date"] = df["joined_date"].dt.strftime('%A, %B %d')
    df.drop(columns=['id', 'user_id_id'], inplace=True)
    print(df.columns)
    return df


def export_selected_volunteers_to_sheets(modeladmin, request, queryset):
    df = prepare_volunteers_export(queryset)

    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('website-data-401203-899945cfc301.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open(title='Volunteer Database Website').sheet1
    for index, row in df.iterrows():
        sheet.append_row(row.tolist())


def export_selected_volunteers_to_excel(modeladmin, request, queryset):
    df = prepare_volunteers_export(queryset)

    # Create an HTTP response with an Excel file
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=volunteers.xlsx'
    # Write the dataframe to the response using pandas Excel writer
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Volunteers', index=False)
    return response


def prepare_event_volunteers_export(queryset):
    data = []

    for event in queryset:
        assignments = VolunteerAssignment.objects.filter(volunteering_event=event)
        for assignment in assignments:
            volunteer = assignment.volunteer
            if not volunteer:
                continue
            data.append({
                'Event Name': event.title,
                'Name': volunteer.name,
                'Email': volunteer.email,
                'Phone#': volunteer.phone,
                'Volunteer Title': assignment.assigned_position,
                'Address': f"{volunteer.address if volunteer.address else ''}, "
                           f"{volunteer.zip_code if volunteer.zip_code else ''}",
                'Event Date': event.datetime,
                # 'Event Location': event.location,
                # 'Organization': volunteer.organization,
                "WA Member": "",
                "Confirmation": assignment.approve_participation

            })

    df = pd.DataFrame(data)
    df['Event Date'] = df['Event Date'].dt.tz_convert('America/Toronto').dt.tz_localize(None)
    df.insert(0, "Month", df['Event Date'].dt.strftime('%B'))
    df.insert(6, "Date", df['Event Date'].dt.strftime('%A, %B %d'))
    df.drop(columns=["Event Date"], inplace=True)
    return df


def export_event_volunteers_to_sheets(modeladmin, request, queryset):
    df = prepare_event_volunteers_export(queryset)
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('website-data-401203-899945cfc301.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open(title='Website Events').sheet1
    for index, row in df.iterrows():
        sheet.append_row(row.tolist())


def export_event_volunteers_to_excel(modeladmin, request, queryset):
    # Create an HTTP response with an Excel file
    df = prepare_event_volunteers_export(queryset)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=volunteering_events_volunteers.xlsx'

    # Write the dataframe to the response using pandas Excel writer
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Volunteering Events Volunteers', index=False)

    return response


export_event_volunteers_to_excel.short_description = "Export Events and Volunteers to Excel"
export_event_volunteers_to_sheets.short_description = "Export Events and Volunteers to Sheets"
export_selected_volunteers_to_excel.short_description = "Export selected volunteers to Excel"
export_selected_volunteers_to_sheets.short_description = "Export selected volunteers to Sheets"
hide_published_events.short_description = "Hide published items"
publish_hidden_events.short_description = "Publish hidden items"
