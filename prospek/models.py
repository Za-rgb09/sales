
from django.db import models
from django.utils import timezone


class Prospek(models.Model):
    STATUS_CHOICES = [
        ('Baru', 'Prospek Baru'),
        ('Dihubungi', 'Sudah Dihubungi'),
        ('Follow Up', 'Follow Up'),
        ('Potensial', 'Potensial'),
        ('Negosiasi', 'Negosiasi'),
        ('Deal', 'Deal'),
        ('Unit Diproses', 'Unit Diproses'),
        ('Diserahkan', 'Unit Diserahkan'),
        ('Tidak Berhasil', 'Tidak Berhasil'),
    ]

    nama = models.CharField(max_length=150)
    perusahaan = models.CharField(max_length=150, blank=True)
    nomor_hp = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    sumber = models.CharField(max_length=100, blank=True)

    unit_diminati = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Unit yang diminati'
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='Baru'
    )

    catatan = models.TextField(blank=True)

    tanggal_deal = models.DateField(
        null=True,
        blank=True
    )

    tanggal_penyerahan = models.DateField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nama

    class Meta:
        ordering = ['-created_at']


class FollowUp(models.Model):
    METODE_CHOICES = [
        ('WhatsApp', 'WhatsApp'),
        ('Telepon', 'Telepon'),
        ('Kunjungan', 'Kunjungan'),
        ('Email', 'Email'),
        ('Lainnya', 'Lainnya'),
    ]

    prospek = models.ForeignKey(
        Prospek,
        on_delete=models.CASCADE,
        related_name='riwayat_followup'
    )

    tanggal = models.DateTimeField(default=timezone.now)

    metode = models.CharField(
        max_length=30,
        choices=METODE_CHOICES,
        default='WhatsApp'
    )

    hasil = models.TextField()

    catatan = models.TextField(blank=True)

    def __str__(self):
        return f'{self.prospek.nama} - {self.tanggal:%d-%m-%Y}'

    class Meta:
        ordering = ['-tanggal']


class Reminder(models.Model):
    prospek = models.ForeignKey(
        Prospek,
        on_delete=models.CASCADE,
        related_name='reminders'
    )

    judul = models.CharField(max_length=150)

    tanggal = models.DateTimeField()

    catatan = models.TextField(blank=True)

    selesai = models.BooleanField(default=False)

    dibuat_pada = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['tanggal']

    def __str__(self):
        return f'{self.judul} - {self.prospek.nama}'

    @property
    def terlambat(self):
        return not self.selesai and self.tanggal < timezone.now()
