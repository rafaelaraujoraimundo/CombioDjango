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