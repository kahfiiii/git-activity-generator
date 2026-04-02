#!/usr/bin/env python3
"""
╔══════════════════════════════════════════╗
║       git-activity-generator  v2.0       ║
║   Fill your GitHub contribution graph    ║
╚══════════════════════════════════════════╝
"""

import os, random, subprocess, sys, calendar, re
from datetime import datetime, timedelta

# ═══════════════════════════════════════════════════════════════
#  ANSI COLORS
# ═══════════════════════════════════════════════════════════════
R    = "\033[0m"
B    = "\033[1m"
DIM  = "\033[2m"
IT   = "\033[3m"
UL   = "\033[4m"
RED  = "\033[91m"
GRN  = "\033[92m"
YLW  = "\033[93m"
BLU  = "\033[94m"
MAG  = "\033[95m"
CYN  = "\033[96m"
WHT  = "\033[97m"
BG_GRN = "\033[42m"
BG_YLW = "\033[43m"
BG_BLU = "\033[44m"
BLK  = "\033[30m"

def _strip(s):
    return re.sub(r'\033\[[0-9;]*m', '', s)

def clr():
    os.system("cls" if os.name == "nt" else "clear")

def p(text=""):
    print(text)

# ═══════════════════════════════════════════════════════════════
#  UI PRIMITIVES
# ═══════════════════════════════════════════════════════════════
def box(lines, color=CYN, width=60):
    top = color + "╔" + "═" * width + "╗" + R
    bot = color + "╚" + "═" * width + "╝" + R
    bar = color + "║" + R
    p(top)
    for line in lines:
        plain_len = len(_strip(line))
        pad = width - plain_len - 2
        p(f"{bar}  {line}{' ' * max(pad,0)}{bar}")
    p(bot)

def divider(w=62, color=DIM):
    p(color + "  " + "─" * w + R)

def header_bar(text, color=CYN):
    plain = _strip(text)
    pad   = max(0, 58 - len(plain))
    p(f"\n  {color}{B}── {text} {'─' * pad}{R}")

def ask(prompt, default=None):
    hint = f" {DIM}[{default}]{R}" if default is not None else ""
    try:
        val = input(f"\n  {B}{prompt}{R}{hint} {CYN}›{R} ").strip()
    except (KeyboardInterrupt, EOFError):
        p(f"\n\n  {YLW}Keluar. Sampai jumpa! 👋{R}\n")
        sys.exit(0)
    return val if val else (str(default) if default is not None else "")

def ask_int(prompt, default, mn=1, mx=9999):
    while True:
        raw = ask(prompt, default)
        try:
            v = int(raw)
            if mn <= v <= mx:
                return v
            p(f"  {RED}⚠  Masukkan angka antara {mn}–{mx}.{R}")
        except ValueError:
            p(f"  {RED}⚠  Harus berupa angka.{R}")

def menu(prompt, options):
    p(f"\n  {B}{prompt}{R}")
    divider(62)
    for i, (label, _) in enumerate(options, 1):
        p(f"  {CYN}{B}{i}.{R}  {label}")
    divider(62)
    while True:
        raw = ask("Pilih nomor", 1)
        try:
            idx = int(raw) - 1
            if 0 <= idx < len(options):
                return options[idx][1]
            p(f"  {RED}⚠  Pilih 1–{len(options)}.{R}")
        except ValueError:
            p(f"  {RED}⚠  Masukkan angka.{R}")

def confirm(prompt):
    while True:
        raw = ask(f"{prompt} (y/n)", "y").lower()
        if raw in ("y", "ya", "yes", ""):
            return True
        if raw in ("n", "tidak", "no"):
            return False
        p(f"  {RED}⚠  Ketik y atau n.{R}")

# ═══════════════════════════════════════════════════════════════
#  CONSTANTS
# ═══════════════════════════════════════════════════════════════
GITHUB_REPO = "https://github.com/kahfiiii/git-activity-generator"
VERSION     = "1.0.0"
NOW         = datetime.now()

MONTHS_ID = [
    "Januari","Februari","Maret","April","Mei","Juni",
    "Juli","Agustus","September","Oktober","November","Desember",
]

PROJECT_NAMES = [
    "todo-cli","expense-tracker","note-manager","file-watcher",
    "link-checker","csv-parser","task-runner","data-cleaner",
    "log-analyzer","api-client","config-loader","db-migrator",
    "cache-manager","event-emitter","queue-processor","rate-limiter",
]

COMMIT_MESSAGES = [
    "init feature","update logic","fix minor bug","improve structure",
    "update README","refactor module","add error handling","clean up code",
    "optimize performance","add comments","remove unused imports","minor tweaks",
    "update dependencies","fix typo","add validation","improve docs",
    "add tests","fix edge case","update config","bump version",
]

# ═══════════════════════════════════════════════════════════════
#  GIT UTILITIES
# ═══════════════════════════════════════════════════════════════
def run_cmd(cmd, env=None, silent=True):
    return subprocess.run(
        cmd, shell=True, env=env,
        stdout=subprocess.DEVNULL if silent else None,
        stderr=subprocess.DEVNULL if silent else None,
    ).returncode

def random_time():
    return f"{random.randint(8,23):02}:{random.randint(0,59):02}:{random.randint(0,59):02}"

def write_fake_change(base_dir):
    os.makedirs(base_dir, exist_ok=True)
    proj = random.choice(PROJECT_NAMES)
    path = os.path.join(base_dir, proj)
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, "main.py"), "a") as f:
        f.write(f"# update {datetime.now()}\n")

# ═══════════════════════════════════════════════════════════════
#  CALENDAR RENDERER
# ═══════════════════════════════════════════════════════════════
def render_calendar(year, month, start_dt=None, end_dt=None):
    p(f"\n  {B}{CYN}  ── {MONTHS_ID[month-1]} {year} ──{R}")
    p(f"  {DIM}  Sen  Sel  Rab  Kam  Jum  Sab  Min{R}")
    for week in calendar.monthcalendar(year, month):
        row = "  "
        for day in week:
            if day == 0:
                row += "     "
                continue
            d = datetime(year, month, day)
            in_range = bool(start_dt and end_dt and start_dt <= d <= end_dt)
            is_today = d.date() == NOW.date()
            if in_range and is_today:
                cell = f"{BG_BLU}{WHT}{B}{day:2}{R}"
            elif in_range:
                cell = f"{BG_GRN}{BLK}{day:2}{R}"
            elif is_today:
                cell = f"{BG_YLW}{BLK}{day:2}{R}"
            else:
                cell = f"{DIM}{day:2}{R}"
            row += f"  {cell} "
        p(row)
    p()

def render_legend():
    p(f"  {BG_GRN}{BLK} ## {R} dipilih   "
      f"{BG_YLW}{BLK} ## {R} hari ini   "
      f"{BG_BLU}{WHT} ## {R} keduanya")

# ═══════════════════════════════════════════════════════════════
#  DATE PICKER
# ═══════════════════════════════════════════════════════════════
def pick_date(label, default):
    header_bar(f"📅  {label}", MAG)
    p()

    # Year
    p(f"  {B}Tahun:{R}")
    year = ask_int("Masukkan tahun", default.year, 2015, NOW.year + 3)

    # Month grid (4 columns)
    p(f"\n  {B}Bulan:{R}")
    for i, m in enumerate(MONTHS_ID, 1):
        hl = f"{BG_GRN}{BLK}" if i == default.month else ""
        print(f"  {CYN}{i:2}.{R} {hl}{m:<12}{R}", end="")
        if i % 4 == 0:
            print()
    if 12 % 4 != 0:
        print()

    month = ask_int("Nomor bulan (1–12)", default.month, 1, 12)

    _, last_day = calendar.monthrange(year, month)
    render_calendar(year, month)

    day = ask_int(f"Tanggal (1–{last_day})", min(default.day, last_day), 1, last_day)
    return datetime(year, month, day)

# ═══════════════════════════════════════════════════════════════
#  SCREENS
# ═══════════════════════════════════════════════════════════════

def screen_banner():
    clr()
    p()
    box([
        " " * 17 + f"{GRN}{B}git-activity-generator{R}",
        " " * 7 + f"{DIM}Isi GitHub contribution graph dengan mudah{R}",
        "",
        " " * 4 + f"{DIM}Version :{R}  {CYN}{B}{VERSION}{R}  {DIM}│  Python 3.7+{R}",
        " " * 4 + f"{DIM}GitHub  :{R}  {CYN}{UL}{GITHUB_REPO.replace('https://', '')}{R}",
    ], color=GRN, width=60)
    p()


def screen_main_menu():
    screen_banner()
    return menu("MENU UTAMA", [
        (f"🚀  {B}Mulai Generate{R}          {DIM}buat commits sekarang{R}",   "generate"),
        (f"🗓️   {B}Pilih Rentang Tanggal{R}   {DIM}atur start & end date{R}",  "date"),
        (f"⚙️   {B}Pengaturan Lanjutan{R}      {DIM}branch, commit/hari{R}",    "settings"),
        (f"ℹ️   {B}Cara Penggunaan{R}          {DIM}panduan langkah demi langkah{R}", "howto"),
        (f"🔗  {B}Buka GitHub Repo{R}         {DIM}{GITHUB_REPO}{R}",          "github"),
        (f"❌  {B}Keluar{R}",                                                    "exit"),
    ])


def screen_howto():
    clr()
    p()
    box([f"  {B}ℹ️   CARA PENGGUNAAN{R}"], color=BLU, width=60)
    p()
    steps = [
        ("1", "Buat repo kosong di GitHub (boleh private)"),
        ("2", f"Clone ke lokal:\n       {CYN}git clone https://github.com/user/repo.git{R}"),
        ("3", f"Masuk ke folder repo:\n       {CYN}cd repo{R}"),
        ("4", f"Taruh & jalankan script:\n       {CYN}python git_activity.py{R}"),
        ("5", "Pilih rentang tanggal di menu interaktif"),
        ("6", f"Script membuat folder {CYN}projects/{R} + commit otomatis"),
        ("7", "Commit langsung di-push ke branch pilihanmu"),
    ]
    for num, desc in steps:
        p(f"  {GRN}{B} {num}.{R}  {desc}")
    p()
    divider()
    p(f"  {YLW}{B}Tips:{R}")
    for t in [
        "Preset 'Normal' agar contribution graph terlihat natural",
        "Branch 'main' = GitHub baru, 'master' = GitHub lama",
        "Jika push gagal: cek  git remote -v  dan login git",
        "GitHub update graph dalam beberapa menit setelah push",
    ]:
        p(f"  {DIM}•  {t}{R}")
    p()
    ask("Tekan Enter untuk kembali ke menu", "")


def screen_github():
    import webbrowser
    clr()
    p()
    box([f"  {B}🔗  GITHUB REPO{R}"], color=CYN, width=60)
    p()
    p(f"  {DIM}URL :{R}  {CYN}{UL}{GITHUB_REPO}{R}")
    p()
    try:
        webbrowser.open(GITHUB_REPO)
        p(f"  {GRN}✓  Browser berhasil dibuka!{R}")
    except Exception:
        p(f"  {YLW}Tidak bisa membuka browser.{R}")
        p(f"  Salin URL di atas dan buka secara manual.")
    p()
    ask("Tekan Enter untuk kembali ke menu", "")


def screen_pick_dates(cfg):
    while True:
        clr()
        p()
        box([f"  {B}🗓️   PILIH RENTANG TANGGAL{R}"], color=MAG, width=60)

        start_dt = pick_date("TANGGAL MULAI", cfg.get("start", NOW.replace(day=1)))

        clr()
        p()
        box([f"  {B}🗓️   PILIH RENTANG TANGGAL{R}"], color=MAG, width=60)
        p(f"  {DIM}Mulai: {B}{GRN}{start_dt.strftime('%d %B %Y')}{R}")

        default_end = start_dt.replace(day=1) + timedelta(days=59)
        end_dt = pick_date("TANGGAL SELESAI", cfg.get("end", default_end))

        if end_dt < start_dt:
            p(f"\n  {RED}⚠  Tanggal selesai harus setelah tanggal mulai!{R}")
            ask("Tekan Enter untuk coba lagi", "")
            continue

        # Preview
        clr()
        p()
        box([f"  {B}🗓️   PREVIEW RENTANG TANGGAL{R}"], color=GRN, width=60)
        days = (end_dt - start_dt).days + 1
        p(f"\n  {GRN}✓  {B}{start_dt.strftime('%d %B %Y')}{R}  →  "
          f"{GRN}{B}{end_dt.strftime('%d %B %Y')}{R}"
          f"  {DIM}({days} hari){R}\n")

        shown = 0
        cur = datetime(start_dt.year, start_dt.month, 1)
        while cur <= end_dt and shown < 3:
            render_calendar(cur.year, cur.month, start_dt, end_dt)
            shown += 1
            cur = (cur.replace(day=28) + timedelta(days=4)).replace(day=1)
        total_months = (end_dt.year - start_dt.year) * 12 + end_dt.month - start_dt.month + 1
        if shown < total_months:
            p(f"  {DIM}... dan {total_months - shown} bulan lainnya{R}")
        render_legend()
        p()

        if confirm("Simpan rentang tanggal ini?"):
            cfg["start"] = start_dt
            cfg["end"]   = end_dt
            p(f"\n  {GRN}✓  Tanggal disimpan!{R}")
            ask("Tekan Enter untuk kembali ke menu", "")
            return cfg


def screen_settings(cfg):
    clr()
    p()
    box([f"  {B}⚙️   PENGATURAN LANJUTAN{R}"], color=YLW, width=60)

    # Branch
    header_bar("🌿  Branch Target", BLU)
    p(f"  {DIM}Branch aktif: {B}{CYN}{cfg.get('branch','master')}{R}\n")
    branch = menu("Pilih branch:", [
        (f"master  {DIM}(default GitHub lama){R}",  "master"),
        (f"main    {DIM}(default GitHub baru){R}",   "main"),
        (f"Ketik nama branch sendiri",               "__custom__"),
    ])
    if branch == "__custom__":
        branch = ask("Nama branch", cfg.get("branch", "master"))
    cfg["branch"] = branch

    # Commits per day
    header_bar("📊  Jumlah Commit per Hari", BLU)
    p(f"  {DIM}Lebih banyak commit = warna lebih gelap di graph.{R}\n")
    preset = menu("Pilih preset:", [
        (f"🟡  Ringan   {DIM}1–2 commit/hari  — terlihat biasa{R}",   "light"),
        (f"🟢  Normal   {DIM}1–4 commit/hari  — natural ✓{R}",        "normal"),
        (f"🔵  Aktif    {DIM}3–7 commit/hari  — cukup sibuk{R}",      "active"),
        (f"🔴  Gila     {DIM}5–15 commit/hari — super aktif{R}",      "insane"),
        (f"⚡  Custom   {DIM}atur sendiri{R}",                         "custom"),
    ])
    presets = {"light": (1,2), "normal": (1,4), "active": (3,7), "insane": (5,15)}
    if preset in presets:
        cfg["min_c"], cfg["max_c"] = presets[preset]
    else:
        cfg["min_c"] = ask_int("Min commit/hari", cfg.get("min_c", 1), 1, 30)
        cfg["max_c"] = ask_int("Max commit/hari", cfg.get("max_c", 3), cfg["min_c"], 30)

    # Push option
    header_bar("📡  Opsi Push ke Remote", BLU)
    push = menu("Setelah generate, langsung push?", [
        (f"✅  Ya  {DIM}— push otomatis setelah selesai{R}",        True),
        (f"💾  Tidak  {DIM}— simpan lokal, push manual nanti{R}",  False),
    ])
    cfg["no_push"] = not push

    p(f"\n  {GRN}✓  Pengaturan disimpan!{R}")
    ask("\nTekan Enter untuk kembali ke menu", "")
    return cfg


def screen_confirm(cfg):
    clr()
    days = (cfg["end"] - cfg["start"]).days + 1
    est  = int(days * (cfg["min_c"] + cfg["max_c"]) / 2)

    p()
    box([f"  {B}📋  RINGKASAN — SIAP GENERATE?{R}"], color=GRN, width=60)
    p()
    rows = [
        ("🗂️   Repo path",       cfg["repo_path"]),
        ("🌿  Branch",           cfg["branch"]),
        ("📅  Tanggal mulai",    cfg["start"].strftime(f"%d {MONTHS_ID[cfg['start'].month-1]} %Y")),
        ("📅  Tanggal selesai",  cfg["end"].strftime(f"%d {MONTHS_ID[cfg['end'].month-1]} %Y")),
        ("📆  Jumlah hari",      f"{days} hari"),
        ("📝  Commit/hari",      f"{cfg['min_c']}–{cfg['max_c']}"),
        ("📊  Estimasi total",   f"~{est} commits"),
        ("📡  Push ke remote",   f"{RED}Tidak{R}" if cfg["no_push"] else f"{GRN}Ya{R}"),
    ]
    for k, v in rows:
        p(f"  {DIM}{k:<24}{R}{B}{CYN}{v}{R}")

    # 2-month calendar preview
    p(f"\n  {B}Preview kalender:{R}")
    shown = 0
    cur = datetime(cfg["start"].year, cfg["start"].month, 1)
    while cur <= cfg["end"] and shown < 2:
        render_calendar(cur.year, cur.month, cfg["start"], cfg["end"])
        shown += 1
        cur = (cur.replace(day=28) + timedelta(days=4)).replace(day=1)
    render_legend()
    p()

    return menu("Lanjutkan?", [
        (f"✅  {B}Ya, mulai generate sekarang!{R}", "yes"),
        (f"✏️   Edit pengaturan lanjutan",            "edit"),
        (f"🗓️   Ganti rentang tanggal",               "date"),
        (f"❌  Batal ke menu utama",                  "cancel"),
    ])


def run_generate(cfg):
    clr()
    p()
    box([
        f"  {B}🚀  GENERATING COMMITS...{R}",
        f"  {DIM}Jangan tutup terminal ini.{R}",
    ], color=GRN, width=60)
    p()

    os.chdir(cfg["repo_path"])
    start   = cfg["start"]
    end     = cfg["end"]
    total_days    = (end - start).days + 1
    total_commits = 0
    current       = start
    day_num       = 0

    while current <= end:
        day_num += 1
        n = random.randint(cfg["min_c"], cfg["max_c"])
        date_str = current.strftime("%Y-%m-%d")

        filled = int(50 * day_num / total_days)
        bar = GRN + "█" * filled + R + DIM + "░" * (50 - filled) + R
        pct = int(100 * day_num / total_days)
        print(f"\r  [{bar}] {B}{pct:3}%{R}  {CYN}{date_str}{R}  {DIM}{n}c{R}   ",
              end="", flush=True)

        for _ in range(n):
            write_fake_change("projects")
            run_cmd("git add .", silent=True)
            dt  = f"{date_str}T{random_time()}"
            env = os.environ.copy()
            env["GIT_AUTHOR_DATE"] = env["GIT_COMMITTER_DATE"] = dt
            run_cmd(f'git commit -m "{random.choice(COMMIT_MESSAGES)}"', env=env, silent=True)
            total_commits += 1

        current += timedelta(days=1)

    print()

    if not cfg["no_push"]:
        p(f"\n  {B}Push ke origin/{cfg['branch']} …{R}")
        code = run_cmd(f"git push origin {cfg['branch']}", silent=False)
        if code == 0:
            p(f"  {GRN}✓  Push berhasil!{R}")
        else:
            p(f"  {RED}✗  Push gagal — coba manual: git push origin {cfg['branch']}{R}")
    else:
        p(f"\n  {YLW}↷  Push dilewati.{R}  Push manual: {CYN}git push origin {cfg['branch']}{R}")

    p()
    box([
        f"  {GRN}{B}✅  SELESAI!{R}",
        "",
        f"  {DIM}Total commit  :{R}  {B}{CYN}{total_commits}{R}",
        f"  {DIM}Rentang       :{R}  {B}{CYN}{total_days} hari{R}",
        f"  {DIM}Branch        :{R}  {B}{CYN}{cfg['branch']}{R}",
        "",
        f"  {DIM}Cek contribution graph kamu di GitHub!{R}",
        f"  {CYN}{UL}{GITHUB_REPO}{R}",
    ], color=GRN, width=60)
    p()

# ═══════════════════════════════════════════════════════════════
#  MAIN LOOP
# ═══════════════════════════════════════════════════════════════
def main():
    cfg = {
        "repo_path": "./",
        "branch":    "master",
        "start":     NOW.replace(day=1),
        "end":       (NOW.replace(day=1) + timedelta(days=59)),
        "min_c":     1,
        "max_c":     4,
        "no_push":   False,
    }

    while True:
        choice = screen_main_menu()

        if choice == "generate":
            clr(); p()
            box([f"  {B}🚀  MULAI GENERATE{R}"], color=GRN, width=60)
            header_bar("🗂️  Path Repo Git", CYN)
            p(f"  {DIM}Folder repo git kamu (misal: ./  atau  /home/user/repo){R}")
            repo_path = ask("Path repo", cfg["repo_path"])
            if not os.path.isdir(repo_path):
                p(f"\n  {RED}✗  Folder tidak ditemukan: {repo_path}{R}")
                ask("Tekan Enter untuk kembali", "")
                continue
            
            if not os.path.isdir(os.path.join(repo_path, ".git")):
                p(f"\n  {RED}✗  {repo_path} bukan repository git.{R}")
                p(f"     Jalankan {CYN}git init{R} terlebih dahulu di folder tersebut.")
                ask("\n  Tekan Enter untuk kembali", "")
                continue
                
            res = subprocess.run("git remote -v", shell=True, cwd=repo_path, capture_output=True, text=True)
            if "origin" not in res.stdout:
                p(f"\n  {RED}✗  Link Git (remote 'origin') belum diatur!{R}")
                p(f"     Tambahkan dengan: {CYN}git remote add origin <url-repo-github>{R}")
                ask("\n  Tekan Enter untuk kembali", "")
                continue

            cfg["repo_path"] = repo_path

            while True:
                action = screen_confirm(cfg)
                if action == "yes":
                    run_generate(cfg)
                    ask("\n  Tekan Enter untuk kembali ke menu", "")
                    break
                elif action == "edit":
                    cfg = screen_settings(cfg)
                elif action == "date":
                    cfg = screen_pick_dates(cfg)
                else:
                    break

        elif choice == "date":
            cfg = screen_pick_dates(cfg)

        elif choice == "settings":
            cfg = screen_settings(cfg)

        elif choice == "howto":
            screen_howto()

        elif choice == "github":
            screen_github()

        elif choice == "exit":
            clr()
            p(f"\n  {YLW}{B}Sampai jumpa! 👋{R}\n")
            sys.exit(0)


if __name__ == "__main__":
    main()
