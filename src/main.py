"""
main.py — Program utama SIM Mahasiswa (console-based, memakai rich).

Jalankan dengan:
    python -m src.main
"""

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich import box
import sys

from src.models import DaftarMahasiswa, Mahasiswa

console = Console()
daftar = DaftarMahasiswa()


# ─────────────────────────── Helpers ────────────────────────────────────────


def _prompt(label: str, default: str = "") -> str:
    """
    Wrapper Prompt.ask() dengan fallback ke input() biasa.

    Python 3.14 di Windows kadang memunculkan EOFError pada rich Prompt;
    fallback ini memastikan program tetap berjalan di semua terminal.
    """
    try:
        return Prompt.ask(label, default=default) if default else Prompt.ask(label)
    except (EOFError, OSError):
        # Fallback: cetak label manual, baca via input() standar
        import re

        label_bersih = re.sub(r"\[.*?\]", "", label).strip()
        suffix = f" [{default}]" if default else ""
        try:
            hasil = input(f"{label_bersih}{suffix}: ")
            return hasil if hasil != "" else default
        except (EOFError, OSError):
            return default


def cetak_judul() -> None:
    console.print(
        Panel.fit(
            "[bold cyan]Sistem Informasi Mahasiswa[/bold cyan]\n"
            "[dim]Program Studi Sistem Informasi[/dim]",
            border_style="cyan",
        )
    )


def cetak_menu() -> None:
    console.print("\n[bold yellow]MENU UTAMA[/bold yellow]")
    menu_items = [
        ("1", "Tambah Mahasiswa"),
        ("2", "Tampilkan Semua Mahasiswa"),
        ("3", "Cari Mahasiswa (NIM)"),
        ("4", "Hapus Mahasiswa (NIM)"),
        ("5", "Edit IPK Mahasiswa"),
        ("0", "Keluar"),
    ]
    for kode, label in menu_items:
        warna = "red" if kode == "0" else "green"
        console.print(f"  [[bold {warna}]{kode}[/bold {warna}]] {label}")
    console.print()


def buat_tabel(mahasiswas: list[Mahasiswa]) -> Table:
    tabel = Table(
        title="[bold]Daftar Mahasiswa[/bold]",
        box=box.ROUNDED,
        border_style="cyan",
        header_style="bold magenta",
        show_lines=True,
    )
    tabel.add_column("No", style="dim", justify="center", width=4)
    tabel.add_column("NIM", style="bold", width=12)
    tabel.add_column("Nama", width=25)
    tabel.add_column("Program Studi", width=20)
    tabel.add_column("Angkatan", justify="center", width=10)
    tabel.add_column("IPK", justify="center", width=6)

    for i, mhs in enumerate(mahasiswas, start=1):
        ipk_str = f"{mhs.ipk:.2f}"
        ipk_style = (
            "green" if mhs.ipk >= 3.0 else ("yellow" if mhs.ipk >= 2.0 else "red")
        )
        tabel.add_row(
            str(i),
            mhs.nim,
            mhs.nama,
            mhs.program_studi,
            str(mhs.angkatan),
            f"[{ipk_style}]{ipk_str}[/{ipk_style}]",
        )
    return tabel


# ─────────────────────────── Aksi Menu ──────────────────────────────────────


def aksi_tambah() -> None:
    console.print("\n[bold green]── Tambah Mahasiswa ──[/bold green]")
    try:
        nim = _prompt("  NIM")
        nama = _prompt("  Nama")
        prodi = _prompt("  Program Studi")
        angkatan_str = _prompt("  Angkatan (tahun)")
        ipk_str = _prompt("  IPK", default="0.0")

        angkatan = int(angkatan_str)
        ipk = float(ipk_str)

        mhs = Mahasiswa(
            nim=nim,
            nama=nama,
            program_studi=prodi,
            angkatan=angkatan,
            ipk=ipk,
        )
        daftar.tambah(mhs)
        console.print(f"\n[bold green]✓ Mahasiswa '{nama}' berhasil ditambahkan.[/bold green]")
    except ValueError as e:
        console.print(f"\n[bold red]✗ Gagal:[/bold red] {e}")


def aksi_tampilkan_semua() -> None:
    console.print()
    if daftar.jumlah == 0:
        console.print("[yellow]Belum ada data mahasiswa.[/yellow]")
        return
    tabel = buat_tabel(daftar.semua())
    console.print(tabel)
    console.print(f"\n[dim]Total: {daftar.jumlah} mahasiswa[/dim]")


def aksi_cari() -> None:
    console.print("\n[bold green]── Cari Mahasiswa ──[/bold green]")
    nim = _prompt("  Masukkan NIM")
    mhs = daftar.cari(nim)
    if mhs is None:
        console.print(f"\n[bold red]✗ Mahasiswa dengan NIM '{nim}' tidak ditemukan.[/bold red]")
    else:
        console.print(
            Panel(
                str(mhs),
                title="[bold cyan]Detail Mahasiswa[/bold cyan]",
                border_style="cyan",
            )
        )


def aksi_hapus() -> None:
    console.print("\n[bold green]── Hapus Mahasiswa ──[/bold green]")
    nim = _prompt("  Masukkan NIM yang akan dihapus")
    berhasil = daftar.hapus(nim)
    if berhasil:
        console.print(f"\n[bold green]✓ Mahasiswa dengan NIM '{nim}' berhasil dihapus.[/bold green]")
    else:
        console.print(f"\n[bold red]✗ NIM '{nim}' tidak ditemukan.[/bold red]")


def aksi_edit_ipk() -> None:
    console.print("\n[bold green]── Edit IPK Mahasiswa ──[/bold green]")
    nim = _prompt("  Masukkan NIM")
    mhs = daftar.cari(nim)
    if mhs is None:
        console.print(f"\n[bold red]✗ NIM '{nim}' tidak ditemukan.[/bold red]")
        return
    try:
        ipk_baru_str = _prompt(f"  IPK baru (saat ini: {mhs.ipk:.2f})")
        ipk_baru = float(ipk_baru_str)
        if not (0.0 <= ipk_baru <= 4.0):
            raise ValueError("IPK harus berada di antara 0.0 dan 4.0.")
        mhs.ipk = ipk_baru
        console.print(f"\n[bold green]✓ IPK mahasiswa '{mhs.nama}' diperbarui menjadi {ipk_baru:.2f}.[/bold green]")
    except ValueError as e:
        console.print(f"\n[bold red]✗ Gagal:[/bold red] {e}")


# ─────────────────────────── Main Loop ──────────────────────────────────────


def main() -> None:
    cetak_judul()

    aksi = {
        "1": aksi_tambah,
        "2": aksi_tampilkan_semua,
        "3": aksi_cari,
        "4": aksi_hapus,
        "5": aksi_edit_ipk,
    }

    try:
        while True:
            cetak_menu()
            pilihan = _prompt("[bold]Pilih menu[/bold]", default="0")

            if pilihan == "0":
                console.print("\n[bold cyan]Terima kasih! Program selesai.[/bold cyan]")
                break
            elif pilihan in aksi:
                aksi[pilihan]()
            else:
                console.print(
                    "\n[bold red]✗ Pilihan tidak valid. Masukkan angka 0–5.[/bold red]"
                )
    except KeyboardInterrupt:
        console.print("\n\n[bold yellow]Program dihentikan (Ctrl+C).[/bold yellow]")
        sys.exit(0)


if __name__ == "__main__":
    main()
