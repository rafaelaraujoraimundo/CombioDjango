from django.views import View
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.utils.http import urlencode
from .models import MondayToken
from .forms import MondayTokenForm
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator

from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import PinggyTokenForm, PinggyRedirectForm
from .models import PinggyRedirect, PinggyToken
from .services.pinggy import start_tunnel, stop_tunnel, check_online

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('global_permissions.combio_integracoes', login_url='erro_page'), name='dispatch')
class MondayTokenListView(ListView):
    model = MondayToken
    template_name = "integracoes/mondaytoken_list.html"
    context_object_name = "tokens"
    extra_context = {
        "title": "Lista de Link PowerBI X Monday",
        "activegroup": "integracoes",
    }

class MondayTokenCreateView(CreateView):
    model = MondayToken
    form_class = MondayTokenForm
    template_name = "integracoes/mondaytoken_form.html"
    success_url = None  # vamos renderizar a mesma página com os links
    extra_context = {
        "title": "Novo Link PowerBI X Monday",
        "activegroup": "integracoes",
    }

    def form_valid(self, form):
        # salva e mantém na mesma página mostrando os links
        self.object = form.save()

        base = 'http://179.191.91.6:810'  # remove barra final
    
        api_path = "/api/v1/integracoes/items"

        # Links GET prontos para clique
        qs_false = urlencode({"token": self.object.token, "includeSubitem": "false"})
        qs_true  = urlencode({"token": self.object.token, "includeSubitem": "true"})
        link_itens = f"{base}{api_path}?{qs_false}"
        link_subitens = f"{base}{api_path}?{qs_true}"

        context = self.get_context_data(form=form, object=self.object)
        context.update({
            "saved": True,
            "generated_token": self.object.token,
            "link_itens": link_itens,
            "link_subitens": link_subitens,
  
        })
        return self.render_to_response(context)


class MondayTokenUpdateView(UpdateView):
    model = MondayToken
    form_class = MondayTokenForm
    template_name = "integracoes/mondaytoken_form.html"
    pk_url_kwarg = "token"

    def form_valid(self, form):
        self.object = form.save()

        base = self.request.build_absolute_uri("/")[:-1]
        api_path = "/api/v1/integraes/items"

        qs_false = urlencode({"token": self.object.token, "includeSubitem": "false"})
        qs_true  = urlencode({"token": self.object.token, "includeSubitem": "true"})
        link_itens = f"{base}{api_path}?{qs_false}"
        link_subitens = f"{base}{api_path}?{qs_true}"

        context = self.get_context_data(form=form, object=self.object)
        context.update({
            "saved": True,
            "generated_token": self.object.token,
            "link_itens": link_itens,
            "link_subitens": link_subitens,
        })
        return self.render_to_response(context)
@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('global_permissions.combio_integracoes', login_url='erro_page'), name='dispatch')
class MondayTokenDeleteView(View):
    def post(self, request, token: str):
        obj = get_object_or_404(MondayToken, pk=token)
        obj.delete()
        messages.success(request, "Token excluído com sucesso.")
        return redirect("integracoes:tokens_list")
    



@login_required
@permission_required('global_permissions.combio_integracoes', raise_exception=True)
def dashboard(request: HttpRequest) -> HttpResponse:
    tokens = PinggyToken.objects.all().prefetch_related("redirects")
    # Soft health-check (não bloqueante)
    for token in tokens:
        for r in token.redirects.all():
            if r.url_publica:
                ok = check_online(r.url_publica)
                r.online = ok
                r.ultimo_check = timezone.now()
                r.save(update_fields=["online", "ultimo_check"])
    return render(request, 'integracoes/pinggy/dashboard.html', {"tokens": tokens})


@login_required
@permission_required('global_permissions.combio_integracoes', raise_exception=True)
def token_novo(request: HttpRequest) -> HttpResponse:
    form = PinggyTokenForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Token cadastrado.")
        return redirect('integracoes:pinggy_dashboard')
    return render(request, 'integracoes/pinggy/token_form.html', {"form": form})


@login_required
@permission_required('global_permissions.combio_integracoes', raise_exception=True)
def redirect_novo(request: HttpRequest) -> HttpResponse:
    form = PinggyRedirectForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Redirecionamento criado.")
        return redirect('integracoes:pinggy_dashboard')
    return render(request, 'integracoes/pinggy/redirect_form.html', {"form": form})


@login_required
@permission_required('global_permissions.combio_integracoes', raise_exception=True)
def iniciar_tunel(request: HttpRequest, redirect_id: int) -> HttpResponse:
    r = get_object_or_404(PinggyRedirect, pk=redirect_id, habilitado=True)
    res = start_tunnel(r.tipo, r.token.token, r.host_local, r.porta_local, r.sni_local)

    r.pid = res.pid
    r.url_publica = res.public_url
    r.porta_publica = res.public_port
    r.online = bool(res.public_url)
    r.ultimo_check = timezone.now()
    r.save()

    if r.url_publica:
        messages.success(request, f"Túnel iniciado: {r.url_publica}")
    else:
        messages.warning(request, "Túnel iniciado, aguardando URL pública…")

    return redirect('integracoes:pinggy_dashboard')


@login_required
@permission_required('global_permissions.combio_integracoes', raise_exception=True)
def parar_tunel(request: HttpRequest, redirect_id: int) -> HttpResponse:
    r = get_object_or_404(PinggyRedirect, pk=redirect_id)
    ok = False
    if r.pid:
        ok = stop_tunnel(r.pid)

    r.online = False
    r.pid = None
    r.save(update_fields=["online", "pid"])

    messages.info(request, "Túnel finalizado." if ok else "Processo não estava ativo.")
    return redirect('integracoes:pinggy_dashboard')
