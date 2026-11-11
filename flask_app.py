
import os

from flask import (
    Flask,
    abort,
    jsonify,
    redirect,
    render_template,
    request,
    url_for
)

app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY",
    "kunci-rahasia-praktikum"
)

# ==================================
# 1. DATA MAHASISWA
# ==================================

KOLOM = ["nim", "nama", "prodi", "ipk", "kehadiran"]

MAHASISWA = [
    dict(zip(KOLOM, baris)) for baris in [
        ("A11.2023.00001", "dewi lestari", "SI", 3.62, 0.95),
        ("A11.2023.00002", "budi santoso", "SI", 2.41, 0.62),
        ("A12.2023.00003", "rina maharani", "TI", 3.05, 0.80),
        ("A12.2023.00004", "agus prasetyo", "TI", 2.78, 0.70),
        ("A13.2023.00005", "siti nurhaliza", "MI", 3.88, 0.98),
    ]
]


# ==================================
# 2. FUNGSI PENCARIAN MAHASISWA
# ==================================

def cari(nim):
    return next(
        (m for m in MAHASISWA if m["nim"] == nim),
        None
    )


# ==================================
# 3. FILTER JINJA
# ==================================

@app.template_filter("predikat")
def predikat(ipk):
    if ipk >= 3.51:
        return "Dengan Pujian"
    if ipk >= 3.01:
        return "Sangat Memuaskan"
    if ipk >= 2.76:
        return "Memuaskan"
    return "Perlu Pendampingan"


@app.template_filter("persen")
def persen(nilai):
    return f"{nilai * 100:.0f}%"


# ==================================
# 4. HALAMAN DASHBOARD
# ==================================

@app.route("/")
def beranda():
    berisiko = [
        m for m in MAHASISWA
        if m["ipk"] < 2.76 or m["kehadiran"] < 0.65
    ]

    return render_template(
        "index.html",
        total=len(MAHASISWA),
        berisiko=berisiko
    )


# ==================================
# 5. DAFTAR MAHASISWA
# ==================================

@app.route("/mahasiswa")
def daftar_mahasiswa():
    prodi = request.args.get("prodi", "").upper()

    data = [
        m for m in MAHASISWA
        if not prodi or m["prodi"] == prodi
    ]

    return render_template(
        "mahasiswa.html",
        data=data,
        prodi=prodi
    )


# ==================================
# 6. DETAIL MAHASISWA
# ==================================

@app.route("/mahasiswa/<nim>")
def detail_mahasiswa(nim):
    mhs = cari(nim)

    if mhs is None:
        abort(404)

    return render_template(
        "detail.html",
        mhs=mhs
    )


# ==================================
# 7. PENCARIAN MAHASISWA
# ==================================

@app.route("/cari", methods=["GET", "POST"])
def cari_nim():
    if request.method == "POST":
        nim = request.form.get("nim", "").strip()

        return redirect(
            url_for("detail_mahasiswa", nim=nim)
        )

    return render_template("cari.html")


# ==================================
# 8. API DATA MAHASISWA
# ==================================

@app.route("/api/mahasiswa/<nim>")
def api_mahasiswa(nim):
    mhs = cari(nim)

    if mhs:
        return jsonify(mhs), 200

    return jsonify(error="NIM tidak ditemukan"), 404


# ==================================
# 9. HALAMAN ERROR 404
# ==================================

@app.errorhandler(404)
def tidak_ditemukan(e):
    return render_template("404.html"), 404
