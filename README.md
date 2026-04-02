<div align="center">

# 🟢 git-activity-generator

**CLI tool untuk mengisi GitHub contribution graph secara otomatis**  
dengan commit yang terlihat natural — dilengkapi UI interaktif di terminal.

[![Python](https://img.shields.io/badge/Python-3.7+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Stars](https://img.shields.io/github/stars/kahfiiii/git-activity-generator?style=flat-square&color=yellow)](https://github.com/kahfiiii/git-activity-generator/stargazers)

</div>

---

## 🖼️ Preview

### Menu Utama
![Menu](assets/menu.png)

### Pemilihan Tanggal & Kalender
![Calendar](assets/calendar.png)

### Hasil di GitHub Contribution Graph
![Graph](assets/graph.png)

---

## ✨ Fitur

| Fitur | Keterangan |
|---|---|
| 🖥️ UI Interaktif | Menu navigasi lengkap di terminal |
| 🗓️ Date Picker | Pilih tahun, bulan, tanggal + preview kalender berwarna |
| 📊 Preset Commit | Ringan / Normal / Aktif / Gila / Custom |
| 🌿 Multi-branch | Support `main`, `master`, atau nama branch sendiri |
| 📡 Auto Push | Push otomatis ke remote setelah generate |
| 📋 Konfirmasi | Ringkasan lengkap sebelum mulai eksekusi |
| 🔗 Link GitHub | Buka repo langsung dari menu |
| 📦 No Install | Pure Python — tidak butuh library tambahan |

---

## 📋 Requirements

Sebelum mulai, pastikan kamu sudah punya:

- ✅ **Python 3.7+** — [download di python.org](https://python.org/downloads)
- ✅ **Git** — [download di git-scm.com](https://git-scm.com/downloads)
- ✅ **Akun GitHub** yang sudah terhubung ke git lokal

Cek apakah sudah terinstall:

```bash
python --version
# Python 3.x.x

git --version
# git version 2.x.x
```

---

## 🛠️ Instalasi

### Langkah 1 — Buat repo baru di GitHub

1. Buka [github.com/new](https://github.com/new)
2. Isi nama repo (contoh: `my-projects`)
3. Pilih **Public** atau **Private**
4. Klik **Create repository** — jangan tambahkan README dulu

### Langkah 2 — Clone repo ke komputer kamu

```bash
git clone https://github.com/USERNAME/NAMA-REPO.git
cd NAMA-REPO
```

> Ganti `USERNAME` dengan username GitHub kamu dan `NAMA-REPO` dengan nama repo yang baru dibuat.

### Langkah 3 — Download script ini

**Opsi A — Clone repo ini lalu copy scriptnya:**

```bash
# Clone repo git-activity-generator
git clone https://github.com/kahfiiii/git-activity-generator.git

# Copy script ke repo kamu
cp git-activity-generator/src/git_activity.py NAMA-REPO/
cd NAMA-REPO
```

**Opsi B — Download langsung (tanpa clone):**

```bash
cd NAMA-REPO

# Linux / macOS
curl -O https://raw.githubusercontent.com/kahfiiii/git-activity-generator/main/src/git_activity.py

# Windows (PowerShell)
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/kahfiiii/git-activity-generator/main/src/git_activity.py" -OutFile "git_activity.py"
```

### Langkah 4 — Verifikasi

Struktur folder kamu seharusnya seperti ini:

```
NAMA-REPO/
└── git_activity.py   ✅
```

Tidak perlu install library apapun — script ini hanya menggunakan Python standard library.

---

## 🚀 Cara Menggunakan

### Jalankan script

```bash
python git_activity.py
```

Setelah dijalankan, akan muncul **menu interaktif** seperti ini:

```
╔══════════════════════════════════════════════════════════════╗
║  git-activity-generator                                      ║
║  Isi GitHub contribution graph dengan mudah 🟩               ║
║  Version : 2.0.0  │  Python 3.7+                            ║
╚══════════════════════════════════════════════════════════════╝

  MENU UTAMA
  ──────────────────────────────────────────────────────────────
  1.  🚀  Mulai Generate          buat commits sekarang
  2.  🗓️   Pilih Rentang Tanggal   atur start & end date
  3.  ⚙️   Pengaturan Lanjutan      branch, commit/hari
  4.  ℹ️   Cara Penggunaan
  5.  🔗  Buka GitHub Repo
  6.  ❌  Keluar
```

---

### Langkah-langkah penggunaan

#### 1️⃣ Pilih Rentang Tanggal (Menu 2)

Sebelum generate, atur dulu tanggal mulai dan selesai:

```
Pilih nomor › 2

── TANGGAL MULAI ──
Masukkan tahun [2025] › 2025
Nomor bulan (1–12) [1] › 1     ← Januari
Tanggal (1–31) [1] › 1

── TANGGAL SELESAI ──
Masukkan tahun [2025] › 2025
Nomor bulan (1–12) [3] › 12    ← Desember
Tanggal (1–31) [28] › 31
```

Setelah dipilih, kalender akan tampil dengan highlight tanggal yang kamu pilih:

```
  ── Januari 2025 ──
  Sen  Sel  Rab  Kam  Jum  Sab  Min
           01   02   03   04   05
  06   07   08   09   10   11   12
  13   14   15   16   17   18   19
  20   21   22   23   24   25   26
  27   28   29   30   31

  ## dipilih    ## hari ini
```

---

#### 2️⃣ Atur Pengaturan Lanjutan (Menu 3)

Konfigurasi branch dan jumlah commit per hari:

```
Pilih nomor › 3

── Branch Target ──
  1.  master  (default GitHub lama)
  2.  main    (default GitHub baru)
  3.  Ketik nama branch sendiri

── Jumlah Commit per Hari ──
  1.  🟡  Ringan   1–2 commit/hari  — terlihat biasa
  2.  🟢  Normal   1–4 commit/hari  — natural ✓
  3.  🔵  Aktif    3–7 commit/hari  — cukup sibuk
  4.  🔴  Gila     5–15 commit/hari — super aktif
  5.  ⚡  Custom   atur sendiri

── Opsi Push ke Remote ──
  1.  ✅  Ya  — push otomatis setelah selesai
  2.  💾  Tidak  — simpan lokal dulu
```

> 💡 **Rekomendasi:** Pilih preset **Normal** agar contribution graph terlihat paling natural.

---

#### 3️⃣ Mulai Generate (Menu 1)

```
Pilih nomor › 1

Path repo [./] › ./
```

Akan muncul ringkasan konfigurasi:

```
📋 RINGKASAN — SIAP GENERATE?
──────────────────────────────────────
🗂️   Repo path         ./
🌿  Branch             main
📅  Tanggal mulai      01 Januari 2025
📅  Tanggal selesai    31 Desember 2025
📆  Jumlah hari        365 hari
📝  Commit/hari        1–4
📊  Estimasi total     ~912 commits
📡  Push ke remote     Ya

Lanjutkan?
  1.  ✅  Ya, mulai generate sekarang!
  2.  ✏️   Edit pengaturan lanjutan
  3.  🗓️   Ganti rentang tanggal
  4.  ❌  Batal
```

Pilih `1` untuk mulai. Progress bar akan muncul:

```
  [████████████████████░░░░░░░░░░░░░░░░░░] 52%  2025-07-03  3 commits
```

Setelah selesai, script otomatis push ke GitHub dan menampilkan ringkasan:

```
╔══════════════════════════════════════════════════════════════╗
║  ✅  SELESAI!                                                ║
║                                                              ║
║  Total commit  :  912                                        ║
║  Rentang       :  365 hari                                   ║
║  Branch        :  main                                       ║
╚══════════════════════════════════════════════════════════════╝
```

Buka GitHub kamu — contribution graph akan terisi dalam beberapa menit! 🟩

---

## 🗺️ Alur Lengkap

```
python git_activity.py
        │
        ▼
   Menu Utama
   ├── 2. Pilih Rentang Tanggal  ──→  Pilih tahun → bulan → tanggal
   ├── 3. Pengaturan Lanjutan    ──→  Branch + commit/hari + push
   └── 1. Mulai Generate         ──→  Konfirmasi → Generate → Push
```

---

## ❓ Troubleshooting

**Push gagal / error remote**
```bash
# Cek apakah remote sudah terset
git remote -v

# Jika belum, tambahkan manual
git remote add origin https://github.com/USERNAME/NAMA-REPO.git
```

**`python` tidak dikenali di Windows**
```bash
# Coba ganti dengan
python3 git_activity.py
# atau
py git_activity.py
```

**Contribution graph tidak update**
> Tunggu 5–10 menit setelah push. GitHub kadang butuh waktu untuk refresh graph.
> Pastikan commit menggunakan **email yang sama** dengan akun GitHub kamu:
> ```bash
> git config user.email
> ```

**Branch salah (main vs master)**
> Cek default branch repo kamu di GitHub → Settings → Default branch.

---

## ⚙️ Preset Commit per Hari

| Preset | Range | Tampilan Graph |
|---|---|---|
| 🟡 Ringan | 1–2 / hari | Warna terang, sesekali aktif |
| 🟢 Normal | 1–4 / hari | **Paling natural** ✓ |
| 🔵 Aktif | 3–7 / hari | Warna sedang, cukup rajin |
| 🔴 Gila | 5–15 / hari | Warna gelap, super aktif |
| ⚡ Custom | bebas | Atur sendiri |

---

## 📜 License

MIT — bebas digunakan dan dimodifikasi.

---

<div align="center">
  Made with ☕ by <a href="https://github.com/kahfiiii">kahfiiii</a>
</div>
