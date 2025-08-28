# suporte/api_suporte.py
from typing import List, Optional
from django.contrib.auth import authenticate
from django.db.models import Q
from ninja import Router, Schema
from ninja.security import HttpBasicAuth
from ninja_jwt.authentication import JWTAuth  # opcional (se já usa JWT)
from .models import UsuarioM365

router = Router(tags=["Suporte / M365"])

# --- Autenticação ---
class BasicAuth(HttpBasicAuth):
    def authenticate(self, request, username, password):
        user = authenticate(request, username=username, password=password)
        if user and user.is_active:
            request.user = user
            return username
        return None

basic_auth = BasicAuth()
jwt_auth = JWTAuth()  # opcional

def _require_perm(request, perm_codename: str):
    if not request.user.has_perm(perm_codename):
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden("Você não tem permissão para acessar este recurso.")

# --- Schemas ---
class UsuarioM365Schema(Schema):
    email: str
    display_name: Optional[str] = None
    given_name: Optional[str] = None
    surname: Optional[str] = None
    job_title: Optional[str] = None
    department: Optional[str] = None
    office_location: Optional[str] = None
    mobile_phone: Optional[str] = None
    business_phones: Optional[str] = None
    user_type: Optional[str] = None
    account_enabled: bool
    created_at: Optional[str] = None
    language: Optional[str] = None
    manager_name: Optional[str] = None
    manager_email: Optional[str] = None
    manager_title: Optional[str] = None
    tenant_id: int
    updated_at: str

class SearchResponse(Schema):
    count: int
    results: List[UsuarioM365Schema]

# --- Endpoints ---
@router.get("/m365/search", response=SearchResponse, auth=[basic_auth, jwt_auth])
def search_usuarios_m365(request, q: str, limit: int = 50, offset: int = 0):
    """
    Busca livre em vários campos (icontains).
    Requer permissão: suporte.view_usuariom365
    """
    perm_check = _require_perm(request, "global_permissions.combio_api")
    if perm_check:
        return perm_check

    filtro = (
        Q(email__icontains=q) |
        Q(display_name__icontains=q) |
        Q(given_name__icontains=q) |
        Q(surname__icontains=q) |
        Q(job_title__icontains=q) |
        Q(department__icontains=q) |
        Q(office_location__icontains=q) |
        Q(mobile_phone__icontains=q) |
        Q(business_phones__icontains=q) |
        Q(user_type__icontains=q) |
        Q(language__icontains=q) |
        Q(manager_name__icontains=q) |
        Q(manager_email__icontains=q) |
        Q(manager_title__icontains=q)
        # | Q(tenant__name__icontains=q)  # habilite se houver campo 'name' em MS365Tenant
    )

    qs = UsuarioM365.objects.filter(filtro).order_by("display_name")
    total = qs.count()
    slice_qs = qs[offset: offset + min(max(limit, 1), 200)]

    results = [
        UsuarioM365Schema(
            email=o.email,
            display_name=o.display_name,
            given_name=o.given_name,
            surname=o.surname,
            job_title=o.job_title,
            department=o.department,
            office_location=o.office_location,
            mobile_phone=o.mobile_phone,
            business_phones=o.business_phones,
            user_type=o.user_type,
            account_enabled=o.account_enabled,
            created_at=o.created_at.isoformat() if o.created_at else None,
            language=o.language,
            manager_name=o.manager_name,
            manager_email=o.manager_email,
            manager_title=o.manager_title,
            tenant_id=o.tenant_id,
            updated_at=o.updated_at.isoformat() if o.updated_at else None,
        )
        for o in slice_qs
    ]
    return {"count": total, "results": results}

@router.get("/m365/by-email", response=Optional[UsuarioM365Schema], auth=[basic_auth, jwt_auth])
def get_usuario_by_email(request, email: str):
    """
    Busca direta pela PK (email).
    Requer permissão: suporte.view_usuariom365
    """
    perm_check = _require_perm(request, "global_permissions.combio_api")
    if perm_check:
        return perm_check

    try:
        o = UsuarioM365.objects.get(pk=email)
        return UsuarioM365Schema(
            email=o.email,
            display_name=o.display_name,
            given_name=o.given_name,
            surname=o.surname,
            job_title=o.job_title,
            department=o.department,
            office_location=o.office_location,
            mobile_phone=o.mobile_phone,
            business_phones=o.business_phones,
            user_type=o.user_type,
            account_enabled=o.account_enabled,
            created_at=o.created_at.isoformat() if o.created_at else None,
            language=o.language,
            manager_name=o.manager_name,
            manager_email=o.manager_email,
            manager_title=o.manager_title,
            tenant_id=o.tenant_id,
            updated_at=o.updated_at.isoformat() if o.updated_at else None,
        )
    except UsuarioM365.DoesNotExist:
        return None
