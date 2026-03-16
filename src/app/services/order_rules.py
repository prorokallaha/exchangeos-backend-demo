from __future__ import annotations

from app.db.models.enums import MemberStatus, OrderStatus, RoleType
from decimal import Decimal


ALLOWED_ORDER_STATUS_TRANSITIONS: dict[OrderStatus, set[OrderStatus]] = {
    OrderStatus.NEW: {
        OrderStatus.IN_PROGRESS,
        OrderStatus.CANCELLED,
    },
    OrderStatus.IN_PROGRESS: {
        OrderStatus.COMPLETED,
        OrderStatus.CANCELLED,
    },
    OrderStatus.COMPLETED: set(),
    OrderStatus.CANCELLED: set(),
}


def validate_order_status_transition(current: OrderStatus, new: OrderStatus) -> None:
    allowed = ALLOWED_ORDER_STATUS_TRANSITIONS.get(current, set())
    if new not in allowed:
        raise ValueError(
            f"Invalid order status transition: {current.value} -> {new.value}"
        )


def validate_assignee(member) -> None:
    if member.role_type != RoleType.OPERATOR:
        raise ValueError("Assigned member must have OPERATOR role")

    if member.status != MemberStatus.ACTIVE:
        raise ValueError("Assigned member must be active")


def validate_order_creation_payload(
    *,
    amount_in: Decimal,
    currency_in: str,
    amount_out: Decimal,
    currency_out: str,
    rate: Decimal,
) -> None:
    if amount_in <= 0:
        raise ValueError("amount_in must be greater than 0")

    if amount_out <= 0:
        raise ValueError("amount_out must be greater than 0")

    if rate <= 0:
        raise ValueError("rate must be greater than 0")

    currency_in_normalized = currency_in.strip().upper()
    currency_out_normalized = currency_out.strip().upper()

    if not currency_in_normalized:
        raise ValueError("currency_in must not be empty")

    if not currency_out_normalized:
        raise ValueError("currency_out must not be empty")

    if currency_in_normalized == currency_out_normalized:
        raise ValueError("currency_in and currency_out must be different")