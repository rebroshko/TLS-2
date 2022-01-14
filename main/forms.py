from django import forms
from django.core.exceptions import ValidationError
from .models import Contact, Record, Calendar


class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = ['name', 'phone', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'id': 'name',
                                           'class': 'my__class'}),
            'phone': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.TextInput(attrs={'class': 'form-input'}),
            'message': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }


    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if len(phone) > 12 or len(phone) < 11:
            raise ValidationError('Номер введен некорректно')
        return phone


class RecordForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['choice_Rec'].empty_label = 'Событие не выбрано'

    class Meta:
        model = Record
        ch = Calendar.published.all()
        choice_Rec = forms.ModelChoiceField(queryset=Calendar.objects.all(), to_field_name='Выберите событие')
        fields = ['choice_Rec', 'name', 'phone', 'message']
        widgets = {
            'choice_Rec': forms.Select(choices=ch, attrs={'class': 'choice'}),
            'name': forms.TextInput(attrs={'class': 'inp'}),
            'phone': forms.TextInput(attrs={'class': 'inp'}),
            'message': forms.Textarea(attrs={'cols': 5, 'rows': 2}),
        }