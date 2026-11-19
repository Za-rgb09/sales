
from django import forms
from .models import Prospek, FollowUp, Reminder


class ProspekForm(forms.ModelForm):
    class Meta:
        model = Prospek
        fields = [
            'nama',
            'perusahaan',
            'nomor_hp',
            'email',
            'sumber',
            'unit_diminati',
            'status',
            'catatan',
            'tanggal_deal',
            'tanggal_penyerahan',
        ]

        widgets = {
            'nama': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nama customer'
            }),
            'perusahaan': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'nomor_hp': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control'
            }),
            'sumber': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'unit_diminati': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contoh: Yamaha NMAX'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'catatan': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
            'tanggal_deal': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'tanggal_penyerahan': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }


class FollowUpForm(forms.ModelForm):
    class Meta:
        model = FollowUp
        fields = ['metode', 'hasil', 'catatan']

        widgets = {
            'metode': forms.Select(attrs={
                'class': 'form-select'
            }),
            'hasil': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Bagaimana hasil komunikasi dengan customer?'
            }),
            'catatan': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Catatan tambahan'
            }),
        }


class ReminderForm(forms.ModelForm):
    tanggal = forms.DateTimeField(
        input_formats=['%Y-%m-%dT%H:%M'],
        widget=forms.DateTimeInput(
            attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            },
            format='%Y-%m-%dT%H:%M'
        )
    )

    class Meta:
        model = Reminder
        fields = ['judul', 'tanggal', 'catatan']

        widgets = {
            'judul': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contoh: Hubungi customer kembali'
            }),
            'catatan': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2
            }),
        }
