from django import forms

from .models import Node


class NodeCreateForm(forms.ModelForm):
    """Form for staff to create a new hierarchy node from the front-end modal."""

    class Meta:
        model = Node
        fields = ["name", "node_type", "parent", "leader", "order"]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "f.eks. 1. Kommando, Alpha-patrulje…",
            }),
            "node_type": forms.Select(attrs={"class": "form-select"}),
            "parent": forms.Select(attrs={"class": "form-select"}),
            "leader": forms.Select(attrs={"class": "form-select"}),
            "order": forms.NumberInput(attrs={
                "class": "form-control",
                "min": 0,
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["parent"].empty_label = "— Ingen (rodenhed)"
        self.fields["parent"].required = False
        self.fields["leader"].empty_label = "— Ingen befalingsmand"
        self.fields["leader"].required = False
        self.fields["order"].initial = 0
