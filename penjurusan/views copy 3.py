from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from .models import User, Jurusan, SoalMinat, JawabanMinat, Minat, Tes, Penjurusan, KlasifikasiRIASEC
from django.contrib import messages
from django.urls import reverse
from django.core.mail import send_mail
from django.utils import timezone
from django.template.loader import get_template, render_to_string
import json
from xhtml2pdf import pisa
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
import pdfkit
from django.conf import settings


# Create your views here.
def user_authenticated(user):
    return user.is_authenticated

def index(request):
    return render(request, 'index.html')

def login_view(request):
    msg = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            msg = "Username atau Password salah"
    return render(request, 'index.html', {'msg': msg})

@login_required
def dashboard(request):
    # Mengambil data statistik
    total_pengguna = User.objects.count()
    total_tes = Tes.objects.count()
    total_jurusan = Jurusan.objects.count()
    total_soal = SoalMinat.objects.count()

    # Mengambil 5 pengguna terbaru
    pengguna_terbaru = User.objects.order_by('-date_joined')[:9]

    user = User.objects.get(username=request.user.username)

    # Menghitung jawaban per minat
    realistic_count = JawabanMinat.objects.filter(
    tes__user=user,
    jawaban='Ya',
    id_soal__minat__nama='Realistic'
    ).count()

    investigative_count = JawabanMinat.objects.filter(
        tes__user=user,
        jawaban='Ya',
        id_soal__minat__nama='Investigative'
    ).count()

    artistic_count = JawabanMinat.objects.filter(
        tes__user=user,
        jawaban='Ya',
        id_soal__minat__nama='Artistic'
    ).count()

    social_count = JawabanMinat.objects.filter(
        tes__user=user,
        jawaban='Ya',
        id_soal__minat__nama='Social'
    ).count()

    enterprising_count = JawabanMinat.objects.filter(
        tes__user=user,
        jawaban='Ya',
        id_soal__minat__nama='Enterprising'
    ).count()

    conventional_count = JawabanMinat.objects.filter(
        tes__user=user,
        jawaban='Ya',
        id_soal__minat__nama='Conventional'
    ).count()

    context = {
        'total_pengguna': total_pengguna,
        'total_tes': total_tes,
        'total_jurusan': total_jurusan,
        'total_soal': total_soal,
        'pengguna_terbaru': pengguna_terbaru,
        'user': user,
        'realistic_count': realistic_count,
        'investigative_count': investigative_count,
        'artistic_count': artistic_count,
        'social_count': social_count,
        'enterprising_count': enterprising_count,
        'conventional_count': conventional_count,
    }

    return render(request, 'dashboard.html', context)

def daftar(request):
    if request.method == 'POST':
        # Ambil data dari formulir pendaftaran
        username = request.POST['username']
        password = request.POST['password']
        nama = request.POST['nama']
        jenis_kelamin = request.POST['jenis_kelamin']
        tanggal_lahir = request.POST['tanggal_lahir']
        asal_sekolah = request.POST['asal_sekolah']
        no_hp = request.POST['no_hp']
        email = request.POST['email']

        # Cek apakah username sudah digunakan
        if User.objects.filter(username=username).exists():
            # Tampilkan SweetAlert jika username sudah digunakan
            response_data = {
                'width': 600,
                'title': 'Username Tidak Tersedia',
                'text': 'Username sudah digunakan. Silahkan pilih username lain.',
                'icon': 'error',
                'confirmButtonColor': "#157347",
            }
            return HttpResponse(json.dumps(response_data), content_type='application/json')

        # Buat objek pengguna baru
        user = User.objects.create_user(username=username, password=password, 
                                        first_name=nama, jenis_kelamin=jenis_kelamin, 
                                        tanggal_lahir=tanggal_lahir, asal_sekolah=asal_sekolah, 
                                        no_hp=no_hp, email=email)

        # Tampilkan SweetAlert jika pendaftaran berhasil
        response_data = {
            'width': 600,
            'title': 'Pendaftaran Berhasil',
            'text': 'Silahkan login untuk melanjutkan.',
            'icon': 'success',
            'confirmButtonColor': "#157347",
        }
        return HttpResponse(json.dumps(response_data), content_type='application/json')

    return render(request, 'daftar.html')

@login_required
def profile_view(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.jenis_kelamin = request.POST.get('jenis_kelamin')
        user.tanggal_lahir = request.POST.get('tanggal_lahir')
        user.asal_sekolah = request.POST.get('asal_sekolah')
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.no_hp = request.POST.get('no_hp')
        
        # Mengelola password
        password = request.POST.get('password')
        if password:
            user.set_password(password)
            # Perbarui sesi autentikasi setelah mengubah password
            update_session_auth_hash(request, user)
        user.save()
        
        messages.success(request, 'Profil berhasil diperbarui.')
        return HttpResponseRedirect(reverse('profile_view'))

def send_contact_email(request):
    if request.method == 'POST':
        # Ambil data dari formulir kontak
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Kirim email
        send_mail(
            'Pesan dari CermatJaya',
            f'Name: {name}\nEmail: {email}\n\nMessage: {message}',
            email,  # Email pengirim
            ['cermatjayaa@gmail.com'],  # Email penerima
            fail_silently=False,
        )

        return HttpResponseRedirect(reverse('thankyou_view'))

@login_required    
def jurusan_view(request):
    return render(request,'jurusan.html', {
        'jurusan': Jurusan.objects.all().order_by('nama_jurusan'),
    })

@login_required
def tes(request):
    return render(request, 'tes.html')

@login_required
def mulai_tes(request):
    if request.method == 'POST':
        tes_id = request.session.get('tes_id')
        if not tes_id:
            return redirect('tes')

        tes = Tes.objects.get(pk=tes_id)
        question_ids = request.POST.getlist('question_ids')

        for qid in question_ids:
            answer = request.POST.get(f'answer_{qid}')
            if answer:
                soal = SoalMinat.objects.get(pk=qid)
                JawabanMinat.objects.create(
                    tes=tes,
                    id_soal=soal,
                    jawaban=answer
                )

        # Ambil soal yang belum dijawab
        next_questions = SoalMinat.objects.exclude(
            id__in=JawabanMinat.objects.filter(tes=tes).values_list('id_soal', flat=True)
        )[:3]

        if next_questions:
            answered_count = JawabanMinat.objects.filter(tes=tes).count()
            context = {
                'current_questions': next_questions,
                'total_soal': SoalMinat.objects.count(),
                'start_number': answered_count + 1,
            }
            return render(request, 'mulai_tes.html', context)
        else:
            return redirect('selesai_tes')

    else:
        # Pertama kali mulai tes
        user = request.user
        tes = Tes.objects.create(user=user, tanggal_tes=timezone.now())
        request.session['tes_id'] = tes.id

        first_questions = SoalMinat.objects.all()[:3]
        context = {
            'current_questions': first_questions,
            'total_soal': SoalMinat.objects.count(),
            'start_number': 1,
        }
        return render(request, 'mulai_tes.html', context)

@login_required
def hasil_tes(request):
    if request.method == 'GET':
        user = request.user

        # Ambil tes terakhir user
        tes = Tes.objects.filter(user=user).order_by('-tanggal_tes').first()
        if not tes:
            return render(request, 'hasil_tes.html', {
                'error': 'Anda belum melakukan tes RIASEC.',
            })

        # Hitung jumlah jawaban "Ya" untuk setiap minat
        skor_minat = {}
        for minat in Minat.objects.all():
            skor = JawabanMinat.objects.filter(
                tes=tes,
                id_soal__minat=minat,
                jawaban='Ya'
            ).count()
            skor_minat[minat.nama.lower()] = skor  # gunakan nama lowercase untuk kesesuaian key

        # Pastikan semua kategori RIASEC terisi, walaupun 0
        all_keys = ['realistic', 'investigative', 'artistic', 'social', 'enterprising', 'conventional']
        for k in all_keys:
            skor_minat.setdefault(k, 0)

        print(skor_minat)  # Print untuk debugging

        # Buat vektor RIASEC
        riasec_vector = np.array([
            skor_minat['realistic'],
            skor_minat['investigative'],
            skor_minat['artistic'],
            skor_minat['social'],
            skor_minat['enterprising'],
            skor_minat['conventional'],
        ])

        # Ambil data klasifikasi dari database
        klasifikasi_data = KlasifikasiRIASEC.objects.all()
        if not klasifikasi_data.exists():
            return render(request, 'hasil_tes.html', {
                'error': 'Data klasifikasi RIASEC belum tersedia.',
            })

        X = []
        y = []
        for data in klasifikasi_data:
            X.append([
                data.realistic,
                data.investigative,
                data.artistic,
                data.social,
                data.enterprising,
                data.conventional
            ])
            y.append(data.id_jurusan.nama_jurusan)

        # Jalankan KNN
        knn = KNeighborsClassifier(n_neighbors=3)  # ambil 3 terdekat
        knn.fit(X, y)

        # Prediksi 3 jurusan terdekat
        _, indices = knn.kneighbors([riasec_vector])
        jurusan_terdekat = [y[i] for i in indices[0]]  # list nama jurusan

        # Ambil objek jurusan berdasarkan nama
        jurusan1 = Jurusan.objects.filter(nama_jurusan=jurusan_terdekat[0]).first()
        jurusan2 = Jurusan.objects.filter(nama_jurusan=jurusan_terdekat[1]).first()
        jurusan3 = Jurusan.objects.filter(nama_jurusan=jurusan_terdekat[2]).first()

        # Validasi minimal jurusan utama tersedia
        if not jurusan1:
            return render(request, 'hasil_tes.html', {
                'error': 'Jurusan hasil prediksi tidak ditemukan.',
            })

        # Simpan hasil penjurusan
        Penjurusan.objects.create(
            user=user,
            tes=tes,
            jurusan_1=jurusan1,
            jurusan_2=jurusan2,
            jurusan_3=jurusan3
        )

        # Cari minat dengan skor tertinggi
        max_score = max(skor_minat.values())
        # Ambil semua minat dengan skor maksimum dan objek Minat-nya
        minat_tertinggi = []
        for minat in Minat.objects.all():
            nama = minat.nama.lower()
            if skor_minat.get(nama, 0) == max_score:
                minat_tertinggi.append(minat)

        return render(request, 'hasil_tes.html', {
            'tes': tes,
            'riasec_scores': skor_minat,
            'jurusan_1': jurusan1,
            'jurusan_2': jurusan2,
            'jurusan_3': jurusan3,
            'minat_tertinggi': minat_tertinggi,
        })

@login_required
def generatePDF(request):
    user = request.user
    penjurusan = Penjurusan.objects.filter(user=user).order_by('-tes__tanggal_tes').first()

    if not penjurusan:
        return HttpResponse("Tidak ada data penjurusan untuk dicetak.")

    tes = penjurusan.tes
    jawaban_ya = JawabanMinat.objects.filter(tes=tes, jawaban='Ya')

    minat_labels = ['Realistic', 'Investigative', 'Artistic', 'Social', 'Enterprising', 'Conventional']
    riasec_scores = {label.lower(): 0 for label in minat_labels}

    for jawaban in jawaban_ya:
        nama_minat = jawaban.id_soal.minat.nama.lower()
        if nama_minat in riasec_scores:
            riasec_scores[nama_minat] += 1

    # Cari minat tertinggi (bisa lebih dari satu)
    max_score = max(riasec_scores.values())
    minat_tertinggi = []
    for minat in Minat.objects.all():
        if riasec_scores.get(minat.nama.lower(), 0) == max_score:
            minat_tertinggi.append(minat)

    context = {
        'user': user,
        'penjurusan': penjurusan,
        'riasec_scores': riasec_scores,
        'jurusan_1': penjurusan.jurusan_1,
        'jurusan_2': penjurusan.jurusan_2,
        'jurusan_3': penjurusan.jurusan_3,
        'minat_tertinggi': minat_tertinggi,
    }

    html = render_to_string('cetak_pdf.html', context)

    pdfkit_config = pdfkit.configuration(wkhtmltopdf=settings.PDFKIT_CONFIG['wkhtmltopdf'])
    pdf = pdfkit.from_string(html, False, configuration=pdfkit_config)

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="hasil_tes_{user.username}.pdf"'
    return response

@login_required
def selesai_tes(request):
    return render(request, 'selesai_tes.html')

@login_required
def tentang_tes(request):
    return render(request, 'tentang_tes.html')

@login_required
def logout_view(request):
    return render(request, 'logout.html')

def thankyou_view(request):
    return render(request, 'thankyou.html')

def logout_session(request):
    logout(request)
    return redirect('index')