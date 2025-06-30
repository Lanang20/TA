from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    jenis_kelamin = models.CharField(
        max_length=20, 
        choices=[('Laki-laki', 'Laki-laki'), ('Perempuan', 'Perempuan')]
    )
    tanggal_lahir = models.DateField()
    asal_sekolah = models.CharField(max_length=255)
    no_hp = models.CharField(max_length=15)

    REQUIRED_FIELDS = ['tanggal_lahir']

    def save(self, *args, **kwargs):
        # Enkripsi password hanya jika password berubah
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

class Minat(models.Model):
    nama = models.CharField(max_length=255)  # e.g., Realistic, Investigative
    deskripsi = models.TextField()

    def __str__(self):
        return self.nama

class SoalMinat(models.Model):
    soal = models.TextField()
    minat = models.ForeignKey(Minat, on_delete=models.CASCADE)

    def __str__(self):
        return f"Soal {self.id}"

class Tes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tes_set')
    tanggal_tes = models.DateTimeField()

    def __str__(self):
        return f"{self.user.username} - {self.tanggal_tes.date()}"

class JawabanMinat(models.Model):
    tes = models.ForeignKey(Tes, on_delete=models.CASCADE)
    id_soal = models.ForeignKey(SoalMinat, on_delete=models.CASCADE)
    jawaban = models.CharField(max_length=10)  # "Ya" atau "Tidak"

    def __str__(self):
        return f"Tes {self.tes.id} - Soal {self.id_soal.id} - Jawaban: {self.jawaban}"

class Jurusan(models.Model):
    nama_jurusan = models.CharField(max_length=255)
    deskripsi = models.TextField()
    prospek_kerja = models.TextField()

    def __str__(self):
        return self.nama_jurusan

class KlasifikasiRIASEC(models.Model):
    realistic = models.IntegerField()
    investigative = models.IntegerField()
    artistic = models.IntegerField()
    social = models.IntegerField()
    enterprising = models.IntegerField()
    conventional = models.IntegerField()
    id_jurusan = models.ForeignKey(Jurusan, on_delete=models.CASCADE, related_name='klasifikasi_riasec')

    def __str__(self):
        return f"Kriteria untuk {self.id_jurusan.nama_jurusan}"

class Penjurusan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='penjurusan_set')
    tes = models.ForeignKey(Tes, on_delete=models.CASCADE)
    jurusan = models.ForeignKey(Jurusan, on_delete=models.CASCADE)

    def tanggal_tes(self):
        return self.tes.tanggal_tes
