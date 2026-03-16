from fastapi import APIRouter

from app.api.v1.organization_members import router as organization_members_router
from app.api.v1.organization_settings import router as organization_settings_router
from app.api.v1.organizations import router as organizations_router
from app.api.v1.platform_organizations import router as platform_organizations_router
from app.api.v1.organization_requisites import router as organization_requisites_router
from app.api.v1.organization_orders import router as organization_orders_router
from app.api.v1.organization_ledger import router as organization_ledger_router
from app.api.v1.organization_stats import router as organization_stats_router
from app.api.v1.users import router as users_router
from app.api.v1.auth import router as auth_router

router = APIRouter()
router.include_router(users_router)
router.include_router(auth_router)
router.include_router(platform_organizations_router)
router.include_router(organizations_router)
router.include_router(organization_members_router)
router.include_router(organization_settings_router)
router.include_router(organization_requisites_router)
router.include_router(organization_orders_router)
router.include_router(organization_ledger_router)
router.include_router(organization_stats_router)