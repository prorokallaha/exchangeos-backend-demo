from __future__ import annotations

import enum


class UserStatus(str, enum.Enum):
    ACTIVE = "active"
    BLOCKED = "blocked"


class OrganizationStatus(str, enum.Enum):
    ACTIVE = "active"
    BLOCKED = "blocked"


class MemberStatus(str, enum.Enum):
    ACTIVE = "active"
    INVITED = "invited"
    BLOCKED = "blocked"


class RoleType(str, enum.Enum):
    OWNER = "owner"
    MANAGER = "manager"
    OPERATOR = "operator"
    VIEWER = "viewer"


class PermissionEffect(str, enum.Enum):
    ALLOW = "allow"
    DENY = "deny"


class SettingValueType(str, enum.Enum):
    INT = "int"
    DECIMAL = "decimal"
    BOOL = "bool"
    STR = "str"
    JSON = "json"


class SettingScope(str, enum.Enum):
    ORGANIZATION = "organization"
    USER = "user"


class AccountType(str, enum.Enum):
    CASH = "cash"
    BANK = "bank"
    CRYPTO = "crypto"
    PROVIDER = "provider"
    INTERNAL = "internal"


class RequisiteKind(str, enum.Enum):
    CARD = "card"
    BANK_ACCOUNT = "bank_account"
    CRYPTO_WALLET = "crypto_wallet"
    SBP = "sbp"


class OrderType(str, enum.Enum):
    BUY = "buy"
    SELL = "sell"
    EXCHANGE = "exchange"


class OrderStatus(str, enum.Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    DISPUTED = "disputed"


class LedgerTxType(str, enum.Enum):
    ORDER = "order"
    DEPOSIT = "deposit"
    WITHDRAW = "withdraw"
    ADJUSTMENT = "adjustment"


class LedgerTxStatus(str, enum.Enum):
    DRAFT = "draft"
    POSTED = "posted"
    CANCELLED = "cancelled"


class EntryDirection(str, enum.Enum):
    DEBIT = "debit"
    CREDIT = "credit"


class AuditAction(str, enum.Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    LOGIN = "login"
    APPROVE = "approve"
    REJECT = "reject"