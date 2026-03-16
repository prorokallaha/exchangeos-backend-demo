from __future__ import annotations

from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, Query

from app.api.deps.access import require_org_permission
from app.db.gateway import DBGateway
from app.db.session import get_gateway
from app.schemas.stats import OrganizationStatsOut
from app.services.stats_service import get_organization_stats

router = APIRouter(
    prefix="/organizations/{organization_id}/stats",
    tags=["organization-stats"],
)


@router.get("", response_model=OrganizationStatsOut)
async def get_org_stats(
    organization_id: UUID,
    period: str = Query(default="all"),
    date_from: datetime | None = Query(default=None),
    date_to: datetime | None = Query(default=None),
    _: object = Depends(require_org_permission("stats.org.read")),
    gw: DBGateway = Depends(get_gateway),
) -> OrganizationStatsOut:
    stats = await get_organization_stats(
        gw=gw,
        organization_id=organization_id,
        period=period,
        date_from=date_from,
        date_to=date_to,
    )
    return OrganizationStatsOut(**stats)