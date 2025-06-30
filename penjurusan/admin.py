from django.contrib import admin
from .models import User, Tes, JawabanMinat, SoalMinat, Minat, Jurusan, KlasifikasiRIASEC, Penjurusan

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'jenis_kelamin', 'tanggal_lahir', 'asal_sekolah', 'no_hp', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'asal_sekolah')
    list_filter = ('jenis_kelamin', 'is_staff', 'is_active')

class SoalMinatAdmin(admin.ModelAdmin):
    list_display = ('id', 'soal', 'minat')
    search_fields = ('soal',)
    list_filter = ('minat',)

class MinatAdmin(admin.ModelAdmin):
    list_display = ('id', 'nama', 'deskripsi')
    search_fields = ('nama',)

class JurusanAdmin(admin.ModelAdmin):
    list_display = ('id', 'nama_jurusan', 'deskripsi', 'prospek_kerja')
    search_fields = ('nama_jurusan',)

class KlasifikasiRIASECAdmin(admin.ModelAdmin):
    list_display = ('id_jurusan', 'realistic', 'investigative', 'artistic', 'social', 'enterprising', 'conventional')

class PenjurusanAdmin(admin.ModelAdmin):
    list_display = ('user', 'tes',)


admin.site.register(User, UserAdmin)
admin.site.register(Tes)
admin.site.register(JawabanMinat)
admin.site.register(SoalMinat, SoalMinatAdmin)
admin.site.register(Minat, MinatAdmin)
admin.site.register(Jurusan, JurusanAdmin)
admin.site.register(KlasifikasiRIASEC, KlasifikasiRIASECAdmin)
admin.site.register(Penjurusan, PenjurusanAdmin)