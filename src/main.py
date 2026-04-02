import os
import sys
import subprocess

def create_virtualenv():
    venv_dir = "venv"
    if not os.path.exists(venv_dir):
        print("\n📦 Mempersiapkan virtual environment... (Membuat folder 'venv')")
        subprocess.check_call([sys.executable, "-m", "venv", venv_dir])
    
    # Menentukan path python executable di dalam venv
    if os.name == "nt":  # Windows
        python_exe = os.path.join(venv_dir, "Scripts", "python.exe")
        pip_exe = os.path.join(venv_dir, "Scripts", "pip.exe")
    else:  # Linux/macOS
        python_exe = os.path.join(venv_dir, "bin", "python")
        pip_exe = os.path.join(venv_dir, "bin", "pip")

    return python_exe, pip_exe

def main():
    print("🔄 Memeriksa environment...")
    
    # 1. Pastikan virtual environment tersedia
    python_exe, pip_exe = create_virtualenv()

    # 2. Install dependencies jika ada requirements.txt
    if os.path.exists("requirements.txt"):
        print("📥 Menginstall dependencies dari requirements.txt...")
        subprocess.check_call([pip_exe, "install", "-r", "requirements.txt", "--quiet"])
    else:
        print("✅ git_activity.py hanya menggunakan library bawaan Python, tidak perlu install external package.")

    print("\n🚀 Menjalankan git_activity.py...\n")
    
    # 3. Jalankan git_activity.py menggunakan python dari virtual environment
    try:
        subprocess.run([python_exe, "git_activity.py"])
    except KeyboardInterrupt:
        print("\n👋 Dihentikan.")
    except Exception as e:
        print(f"\n❌ Terjadi kesalahan saat menjalankan: {e}")

if __name__ == "__main__":
    main()
