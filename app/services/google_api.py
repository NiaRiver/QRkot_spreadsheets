from datetime import datetime as dt
from datetime import timedelta as delta

from aiogoogle import Aiogoogle

from app.core.config import settings

FORMAT = "%Y/%m/%d %H:%M:%S"


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    now_dt = dt.now().strftime(FORMAT)
    service = await wrapper_services.discover("sheets", "v4")
    spreadsheet_body = {
        "properties": {
            "title": f"Отчёт на {now_dt}",
            "locale": "ru_RU"
        },
        "sheets": [
            {
                "properties": {
                    "sheetType": "GRID",
                    "sheetId": 0,
                    "title": "Лист1",
                    "gridProperties": {
                        "rowCount": 100,
                        "columnCount": 11
                    }
                }
            }
        ]
    }
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheetid = response["spreadsheetId"]
    return spreadsheetid


async def set_user_permissions(
    spreadsheetid: str,
    wrapper_services: Aiogoogle
) -> None:
    permissions_body = {
        "type": "user",
        "role": "writer",
        "emailAddress": settings.email
    }
    service = await wrapper_services.discover("drive", "v3")
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid,
            json=permissions_body,
            fields="id"
        )
    )


async def spreadsheets_update_value(
    spreadsheetid: str,
    reservations: list,
    wrapper_services: Aiogoogle
) -> list[dict[str, str]]:
    now_dt = dt.now().strftime(FORMAT)
    service = await wrapper_services.discover(
        "sheets", "v4"
    )
    table_values = [
        ["Отчёт от", now_dt],
        ["Топ проктов по скорости закрытия."],
        ["Название проекта", "Время сбора", "Описание"]
    ]
    for res in reservations:
        new_row = [
            str(res["name"]),
            str(delta(days=res["open_duration"])),
            str(res["description"])
        ]
        table_values.append(new_row)

    update_body = {
        "majorDimension": "ROWS",
        "values": table_values
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range="A1:E30",
            valueInputOption="USER_ENTERED",
            json=update_body
        )
    )
    keys = ["name", "open_duration", "description"]
    table_values = [dict(zip(keys, item)) for item in table_values]
    return table_values[3:]