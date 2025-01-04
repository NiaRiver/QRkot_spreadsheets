from copy import deepcopy
from datetime import datetime as dt
from datetime import timedelta as delta

from aiogoogle import Aiogoogle

from app.core.config import settings

FORMAT = "%Y/%m/%d %H:%M:%S"
ROW_COUNT = 100
COLUMN_COUNT = 11
SPREADSHEET_BODY = dict(
    properties=dict(
        title="Отчёт на {date}",
        locale="ru_RU"
    ),
    sheets=[dict(
        properties=dict(
            sheetType="GRID",
            sheetId=0,
            title="Лист1",
            gridProperties=dict(
                rowCount=ROW_COUNT,
                columnCount=COLUMN_COUNT
            )
        )
    )]
)
TABLE_HEADER = [
    ["Отчёт от", "{date}"],
    ["Топ проктов по скорости закрытия."],
    ["Название проекта", "Время сбора", "Описание"]
]


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    now_dt = dt.now().strftime(FORMAT)
    service = await wrapper_services.discover("sheets", "v4")
    spreadsheet_body = deepcopy(SPREADSHEET_BODY)
    spreadsheet_body["properties"]["title"] = spreadsheet_body[
        "properties"
    ]["title"].format(date=now_dt)
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    return response["spreadsheetId"], response["spreadsheetUrl"]


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
    spreadsheet_id: str,
    projects: list,
    wrapper_services: Aiogoogle
) -> list[dict[str, str]]:
    now_dt = dt.now().strftime(FORMAT)
    service = await wrapper_services.discover(
        "sheets", "v4"
    )
    sheet_data = await wrapper_services.as_service_account(
        service.spreadsheets.get(spreadsheetId=spreadsheet_id)
    )
    table_values = deepcopy(TABLE_HEADER)
    table_values[0][1] = table_values[0][1].format(date=now_dt)
    table_values.extend([[
        str(project["name"]),
        str(delta(days=project["open_duration"])),
        str(project["description"])
    ] for project in projects])
    sheet_dims = sheet_data["sheets"][0]["properties"]["gridProperties"]
    update_dims = dict(
        rowCount=len(table_values),
        columnCount=max(len(row) for row in table_values)
    )
    for dim, value in update_dims.items():
        if value > sheet_dims[dim]:
            dim_name = "строк" if dim == "rowCount" else "колонок"
            raise ValueError("Данные отчета не помещаются на листе. "
                             f"{dim_name.capitalize()} отчета больше "
                             f"{dim_name} листа. "
                             f"{value} > {sheet_dims[dim]}")
    update_body = dict(
        majorDimension="ROWS",
        values=table_values
    )
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range="R1C1:R{rowCount}C{columnCount}".format(**update_dims),
            valueInputOption="USER_ENTERED",
            json=update_body
        )
    )
