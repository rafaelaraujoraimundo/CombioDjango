from django import forms
from .models import MondayToken

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