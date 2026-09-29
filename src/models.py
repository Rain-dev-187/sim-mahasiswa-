"""
models.py — Dataclass model untuk entitas Mahasiswa dan DaftarMahasiswa.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Mahasiswa:
    """Representasi satu data mahasiswa."""

    nim: str
    nama: str
    program_studi: str
    angkatan: int
    ipk: float = 0.0

    def __post_init__(self) -> None:
        """Validasi atribut setelah inisialisasi."""
        if not self.nim or len(self.nim.strip()) < 6:
            raise ValueError(
                "NIM tidak boleh kosong dan minimal 6 karakter."
            )
        self.nim = self.nim.strip()

        if not self.nama or not self.nama.strip():
            raise ValueError("Nama tidak boleh kosong.")
        self.nama = self.nama.strip()

        if not self.program_studi or not self.program_studi.strip():
            raise ValueError("Program studi tidak boleh kosong.")
        self.program_studi = self.program_studi.strip()

        if not isinstance(self.angkatan, int) or self.angkatan < 1000:
            raise ValueError("Angkatan harus berupa tahun 4 digit (misal: 2023).")

        if not (0.0 <= self.ipk <= 4.0):
            raise ValueError("IPK harus berada di antara 0.0 dan 4.0.")

    def __str__(self) -> str:
        return (
            f"NIM       : {self.nim}\n"
            f"Nama      : {self.nama}\n"
            f"Prodi     : {self.program_studi}\n"
            f"Angkatan  : {self.angkatan}\n"
            f"IPK       : {self.ipk:.2f}"
        )


@dataclass
class DaftarMahasiswa:
    """Koleksi data mahasiswa dengan operasi CRUD sederhana."""

    _mahasiswa: list[Mahasiswa] = field(default_factory=list)

    @property
    def jumlah(self) -> int:
        """Kembalikan jumlah mahasiswa yang terdaftar."""
        return len(self._mahasiswa)

    def tambah(self, mhs: Mahasiswa) -> None:
        """
        Tambahkan mahasiswa ke daftar.

        Raises:
            ValueError: Jika NIM sudah terdaftar.
        """
        if self.cari(mhs.nim) is not None:
            raise ValueError(f"NIM '{mhs.nim}' sudah terdaftar.")
        self._mahasiswa.append(mhs)

    def cari(self, nim: str) -> Optional[Mahasiswa]:
        """
        Cari mahasiswa berdasarkan NIM.

        Returns:
            Mahasiswa jika ditemukan, None jika tidak.
        """
        nim = nim.strip()
        for mhs in self._mahasiswa:
            if mhs.nim == nim:
                return mhs
        return None

    def hapus(self, nim: str) -> bool:
        """
        Hapus mahasiswa berdasarkan NIM.

        Returns:
            True jika berhasil dihapus, False jika tidak ditemukan.
        """
        nim = nim.strip()
        for i, mhs in enumerate(self._mahasiswa):
            if mhs.nim == nim:
                self._mahasiswa.pop(i)
                return True
        return False

    def semua(self) -> list[Mahasiswa]:
        """Kembalikan salinan daftar semua mahasiswa."""
        return list(self._mahasiswa)
