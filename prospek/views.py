
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q, Count
from django.http import HttpResponse

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

from .models import Prospek, FollowUp, Reminder
from .forms import ProspekForm, FollowUpForm, ReminderForm


def index(request):
    data = Prospek.objects.all()

    keyword = request.GET.get('q', '')
    status = request.GET.get('status', '')

    if keyword:
        data = data.filter(
            Q(nama__icontains=keyword) |
            Q(nomor_hp__icontains=keyword) |
            Q(unit_diminati__icontains=keyword)
        )

    if status:
        data = data.filter(status=status)

    context = {
        'data': data,
        'keyword': keyword,
        'status_filter': status,
        'status_choices': Prospek.STATUS_CHOICES,
    }

    return render(request, 'prospek/index.html', context)


def tambah(request):
    form = ProspekForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Prospek berhasil ditambahkan.')
        return redirect('prospek:index')

    return render(request, 'prospek/form.html', {
        'form': form,
        'judul': 'Tambah Prospek'
    })


def edit(request, id):
    prospek = get_object_or_404(Prospek, id=id)
    form = ProspekForm(request.POST or None, instance=prospek)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Data prospek berhasil diperbarui.')
        return redirect('prospek:detail', id=prospek.id)

    return render(request, 'prospek/form.html', {
        'form': form,
        'judul': 'Edit Prospek'
    })


def hapus(request, id):
    prospek = get_object_or_404(Prospek, id=id)

    if request.method == 'POST':
        prospek.delete()
        messages.success(request, 'Prospek berhasil dihapus.')
        return redirect('prospek:index')

    return render(request, 'prospek/hapus.html', {
        'prospek': prospek
    })


def detail(request, id):
    prospek = get_object_or_404(Prospek, id=id)

    riwayat = prospek.riwayat_followup.all()
    reminders = prospek.reminders.all()

    followup_form = FollowUpForm()
    reminder_form = ReminderForm()

    if request.method == 'POST':
        jenis = request.POST.get('jenis')

        if jenis == 'followup':
            followup_form = FollowUpForm(request.POST)

            if followup_form.is_valid():
                aktivitas = followup_form.save(commit=False)
                aktivitas.prospek = prospek
                aktivitas.save()

                if prospek.status == 'Baru':
                    prospek.status = 'Dihubungi'
                    prospek.save()

                messages.success(request, 'Riwayat follow-up berhasil disimpan.')
                return redirect('prospek:detail', id=id)

        elif jenis == 'reminder':
            reminder_form = ReminderForm(request.POST)

            if reminder_form.is_valid():
                reminder = reminder_form.save(commit=False)
                reminder.prospek = prospek
                reminder.save()

                messages.success(request, 'Reminder berhasil dibuat.')
                return redirect('prospek:detail', id=id)

    return render(request, 'prospek/detail.html', {
        'prospek': prospek,
        'riwayat': riwayat,
        'reminders': reminders,
        'followup_form': followup_form,
        'reminder_form': reminder_form,
    })


def daftar_reminder(request):
    sekarang = timezone.now()

    reminders = Reminder.objects.select_related(
        'prospek'
    ).filter(
        selesai=False
    )

    hari_ini = reminders.filter(
        tanggal__date=timezone.localdate()
    )

    terlambat = reminders.filter(
        tanggal__lt=sekarang
    )

    return render(request, 'prospek/reminder.html', {
        'reminders': reminders,
        'hari_ini': hari_ini,
        'terlambat': terlambat,
    })


def selesaikan_reminder(request, id):
    reminder = get_object_or_404(Reminder, id=id)

    if request.method == 'POST':
        reminder.selesai = True
        reminder.save()
        messages.success(request, 'Reminder berhasil diselesaikan.')

    return redirect('prospek:reminder')


def export_excel(request):
    data = Prospek.objects.all()

    wb = Workbook()
    ws = wb.active
    ws.title = 'Data Prospek'

    headers = [
        'No',
        'Nama Customer',
        'Perusahaan',
        'Nomor HP',
        'Email',
        'Sumber',
        'Unit Diminati',
        'Status',
        'Tanggal Deal',
        'Tanggal Penyerahan',
        'Tanggal Dibuat',
    ]

    ws.append(headers)

    for nomor, p in enumerate(data, start=1):
        ws.append([
            nomor,
            p.nama,
            p.perusahaan,
            p.nomor_hp,
            p.email,
            p.sumber,
            p.unit_diminati,
            p.get_status_display(),
            p.tanggal_deal.strftime('%d-%m-%Y') if p.tanggal_deal else '',
            p.tanggal_penyerahan.strftime('%d-%m-%Y') if p.tanggal_penyerahan else '',
            timezone.localtime(p.created_at).strftime('%d-%m-%Y %H:%M'),
        ])

    header_fill = PatternFill(
        fill_type='solid',
        fgColor='1E293B'
    )

    for cell in ws[1]:
        cell.font = Font(color='FFFFFF', bold=True)
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal='center')

    for column in ws.columns:
        max_length = max(
            len(str(cell.value or ''))
            for cell in column
        )
        column_letter = get_column_letter(column[0].column)
        ws.column_dimensions[column_letter].width = min(max_length + 4, 35)

    ws.freeze_panes = 'A2'
    ws.auto_filter.ref = ws.dimensions

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

    response['Content-Disposition'] = (
        'attachment; filename="laporan_data_prospek.xlsx"'
    )

    wb.save(response)

    return response
