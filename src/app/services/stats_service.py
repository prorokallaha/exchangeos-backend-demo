from __future__ import annotations

import uuid
from datetime import datetime, time, timedelta, timezone
from decimal import Decimal

from app.db.gateway import DBGateway
from app.db.models.enums import OrderStatus


def _resolve_period_bounds(
    *,
    period: str,
    date_from: datetime | None,
    date_to: datetime | None,
) -> tuple[datetime | None, datetime | None]:
    now = datetime.now(timezone.utc)

    if period == "all":
        return None, None

    if period == "today":
        start = datetime.combine(now.date(), time.min, tzinfo=timezone.utc)
        return start, now

    if period == "week":
        start = now - timedelta(days=7)
        return start, now

    if period == "month":
        start = now - timedelta(days=30)
        return start, now

    if period == "custom":
        if date_from is None or date_to is None:
            raise ValueError("date_from and date_to are required for custom period")
        if date_from > date_to:
            raise ValueError("date_from must be less than or equal to date_to")
        return date_from, date_to

    raise ValueError("Unsupported period")


async def get_organization_stats(
    gw: DBGateway,
    *,
    organization_id: uuid.UUID,
    period: str = "all",
    date_from: datetime | None = None,
    date_to: datetime | None = None,
) -> dict:
    resolved_from, resolved_to = _resolve_period_bounds(
        period=period,
        date_from=date_from,
        date_to=date_to,
    )

    orders = await gw.orders().list_by_org(organization_id)

    if resolved_from is not None:
        orders = [o for o in orders if o.created_at >= resolved_from]

    if resolved_to is not None:
        orders = [o for o in orders if o.created_at <= resolved_to]

    member_map: dict[uuid.UUID, object] = {}
    user_map: dict[uuid.UUID, object] = {}

    assigned_member_ids = {
        o.assigned_to_member_id for o in orders if o.assigned_to_member_id is not None
    }

    for member_id in assigned_member_ids:
        member = await gw.members().get_by_id(member_id)
        if member:
            member_map[member_id] = member

    user_ids = {
        member.user_id
        for member in member_map.values()
        if getattr(member, "user_id", None) is not None
    }

    for user_id in user_ids:
        user = await gw.users().get_by_id(user_id)
        if user:
            user_map[user_id] = user

    total_orders = len(orders)
    completed_orders = [o for o in orders if o.status == OrderStatus.COMPLETED]
    active_orders = [
        o for o in orders if o.status in {OrderStatus.NEW, OrderStatus.IN_PROGRESS}
    ]
    cancelled_orders = [o for o in orders if o.status == OrderStatus.CANCELLED]

    total_volume_in = sum((o.amount_in for o in completed_orders), Decimal("0"))
    total_volume_out = sum((o.amount_out for o in completed_orders), Decimal("0"))

    by_order_type_map: dict = {}
    by_currency_in_map: dict[str, dict] = {}
    by_currency_out_map: dict[str, dict] = {}
    by_operator_map: dict[uuid.UUID, dict] = {}

    for order in orders:
        by_order_type_map[order.type] = by_order_type_map.get(order.type, 0) + 1

        if order.status == OrderStatus.COMPLETED:
            if order.currency_in not in by_currency_in_map:
                by_currency_in_map[order.currency_in] = {
                    "currency": order.currency_in,
                    "count": 0,
                    "volume": Decimal("0"),
                }
            by_currency_in_map[order.currency_in]["count"] += 1
            by_currency_in_map[order.currency_in]["volume"] += order.amount_in

            if order.currency_out not in by_currency_out_map:
                by_currency_out_map[order.currency_out] = {
                    "currency": order.currency_out,
                    "count": 0,
                    "volume": Decimal("0"),
                }
            by_currency_out_map[order.currency_out]["count"] += 1
            by_currency_out_map[order.currency_out]["volume"] += order.amount_out

        if order.assigned_to_member_id is not None:
            assigned_member = member_map.get(order.assigned_to_member_id)
            assigned_user = None
            if assigned_member and getattr(assigned_member, "user_id", None):
                assigned_user = user_map.get(assigned_member.user_id)

            if order.assigned_to_member_id not in by_operator_map:
                by_operator_map[order.assigned_to_member_id] = {
                    "member_id": order.assigned_to_member_id,
                    "user_id": getattr(assigned_member, "user_id", None),
                    "login": getattr(assigned_user, "login", None),
                    "display_name": getattr(assigned_user, "display_name", None),
                    "orders_count": 0,
                    "completed_orders": 0,
                    "volume_in": Decimal("0"),
                    "volume_out": Decimal("0"),
                }

            by_operator_map[order.assigned_to_member_id]["orders_count"] += 1

            if order.status == OrderStatus.COMPLETED:
                by_operator_map[order.assigned_to_member_id]["completed_orders"] += 1
                by_operator_map[order.assigned_to_member_id]["volume_in"] += order.amount_in
                by_operator_map[order.assigned_to_member_id]["volume_out"] += order.amount_out

    by_operator = list(by_operator_map.values())
    by_operator.sort(
        key=lambda item: (
            item["completed_orders"],
            item["orders_count"],
            item["volume_in"],
        ),
        reverse=True,
    )

    return {
        "period": {
            "period": period,
            "date_from": resolved_from,
            "date_to": resolved_to,
        },
        "summary": {
            "total_orders": total_orders,
            "completed_orders": len(completed_orders),
            "active_orders": len(active_orders),
            "cancelled_orders": len(cancelled_orders),
            "total_volume_in": total_volume_in,
            "total_volume_out": total_volume_out,
        },
        "by_order_type": [
            {
                "type": order_type,
                "count": count,
            }
            for order_type, count in by_order_type_map.items()
        ],
        "by_currency_in": list(by_currency_in_map.values()),
        "by_currency_out": list(by_currency_out_map.values()),
        "by_operator": by_operator,
    }