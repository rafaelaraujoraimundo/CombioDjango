from django import forms
from .models import MondayToken,  PinggyToken, PinggyRedirect

class MondayTokenForm(forms.ModelForm):
    class Meta:
        model = MondayToken
        fields = ["monday_key", "monday_board"]
        widgets = {
            "monday_key": forms.PasswordInput(
                render_value=False,
                attrs={
                    "autocomplete": "new-password",
                    "autocapitalize": "off",
                    "autocorrect": "off",
                    "spellcheck": "false",
                    "data-lpignore": "true",
                    "data-1p-ignore": "true",
                },
            ),
        }
    

class PinggyTokenForm(forms.ModelForm):
    class Meta:
        model = PinggyToken
        fields = ["nome", "token", "subdominio", "ativo", "auto_start", "observacoes"]
        widgets = {"observacoes": forms.Textarea(attrs={"rows": 2})}


class PinggyRedirectForm(forms.ModelForm):
    class Meta:
        model = PinggyRedirect
        fields = ["token", "nome", "tipo", "host_local", "porta_local", "sni_local", "habilitado"]