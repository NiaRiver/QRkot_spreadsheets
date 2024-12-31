from datetime import datetime as dt

from app.models.base import CharityDonationBase


def invest(
    target: CharityDonationBase,
    sources: list[CharityDonationBase]
) -> list[CharityDonationBase]:
    updates = []
    invest_date = dt.now()
    for source in sources:
        if not target.fully_invested:
            investing_amount = min(
                source.full_amount - source.invested_amount,
                target.full_amount - target.invested_amount
            )
            for proj_or_donat in [target, source]:
                proj_or_donat.invested_amount += investing_amount
                if proj_or_donat.invested_amount == proj_or_donat.full_amount:
                    proj_or_donat.fully_invested = True
                    proj_or_donat.close_date = invest_date
            updates.append(source)
    return updates
