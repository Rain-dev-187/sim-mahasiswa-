"""
test_main.py — Unit test untuk modul src.models (Mahasiswa & DaftarMahasiswa).

Jalankan: pytest tests/ -v
"""

import pytest

from src.models import DaftarMahasiswa, Mahasiswa


# ─────────────────────────── Fixtures ────────────────────────────────────────


@pytest.fixture
def mahasiswa_valid() -> Mahasiswa:
    """Objek Mahasiswa yang datanya valid."""
    return Mahasiswa(
        nim="22SI001",
        nama="Budi Santoso",
        program_studi="Sistem Informasi",
        angkatan=2022,
        ipk=3.75,
    )


@pytest.fixture
def daftar_kosong() -> DaftarMahasiswa:
    """DaftarMahasiswa tanpa isi."""
    return DaftarMahasiswa()


@pytest.fixture
def daftar_berisi(mahasiswa_valid: Mahasiswa) -> DaftarMahasiswa:
    """DaftarMahasiswa sudah berisi satu mahasiswa."""
    d = DaftarMahasiswa()
    d.tambah(mahasiswa_valid)
    return d


# ─────────────────────────── Test Mahasiswa ──────────────────────────────────


def test_mahasiswa_valid(mahasiswa_valid: Mahasiswa) -> None:
    """Test 1: Objek Mahasiswa valid terbentuk dengan benar."""
    assert mahasiswa_valid.nim == "22SI001"
    assert mahasiswa_valid.nama == "Budi Santoso"
    assert mahasiswa_valid.ipk == 3.75


def test_nim_kosong_raise_value_error() -> None:
    """Test 2: NIM kosong harus memunculkan ValueError."""
    with pytest.raises(ValueError, match="NIM"):
        Mahasiswa(
            nim="",
            nama="Andi",
            program_studi="SI",
            angkatan=2022,
        )


def test_nim_kurang_dari_6_karakter_raise_value_error() -> None:
    """Test 3: NIM kurang dari 6 karakter harus memunculkan ValueError."""
    with pytest.raises(ValueError, match="NIM"):
        Mahasiswa(
            nim="12345",  # hanya 5 karakter
            nama="Andi",
            program_studi="SI",
            angkatan=2022,
        )


def test_nama_kosong_raise_value_error() -> None:
    """Test 4: Nama kosong harus memunculkan ValueError."""
    with pytest.raises(ValueError, match="Nama"):
        Mahasiswa(
            nim="22SI001",
            nama="",
            program_studi="SI",
            angkatan=2022,
        )


def test_ipk_di_atas_4_raise_value_error() -> None:
    """Test 5: IPK > 4.0 harus memunculkan ValueError."""
    with pytest.raises(ValueError, match="IPK"):
        Mahasiswa(
            nim="22SI002",
            nama="Siti",
            program_studi="SI",
            angkatan=2022,
            ipk=4.01,
        )


def test_ipk_negatif_raise_value_error() -> None:
    """Test 6: IPK negatif harus memunculkan ValueError."""
    with pytest.raises(ValueError, match="IPK"):
        Mahasiswa(
            nim="22SI003",
            nama="Rudi",
            program_studi="SI",
            angkatan=2022,
            ipk=-0.1,
        )


def test_ipk_boundary_minimum() -> None:
    """Test 7: IPK tepat 0.0 harus valid (boundary minimum)."""
    mhs = Mahasiswa(
        nim="22SI004",
        nama="Dewi",
        program_studi="SI",
        angkatan=2022,
        ipk=0.0,
    )
    assert mhs.ipk == 0.0


def test_ipk_boundary_maksimum() -> None:
    """Test 8: IPK tepat 4.0 harus valid (boundary maksimum)."""
    mhs = Mahasiswa(
        nim="22SI005",
        nama="Hendra",
        program_studi="SI",
        angkatan=2022,
        ipk=4.0,
    )
    assert mhs.ipk == 4.0


# ─────────────────────────── Test DaftarMahasiswa ────────────────────────────


def test_tambah_dan_cari(
    daftar_kosong: DaftarMahasiswa, mahasiswa_valid: Mahasiswa
) -> None:
    """Test 9: Mahasiswa yang ditambahkan bisa dicari dengan NIM-nya."""
    daftar_kosong.tambah(mahasiswa_valid)
    hasil = daftar_kosong.cari("22SI001")
    assert hasil is not None
    assert hasil.nama == "Budi Santoso"


def test_tambah_nim_duplikat_raise_value_error(
    daftar_berisi: DaftarMahasiswa,
) -> None:
    """Test 10: Menambahkan NIM yang sudah ada harus memunculkan ValueError."""
    duplikat = Mahasiswa(
        nim="22SI001",  # NIM sama dengan fixture
        nama="Tiruan",
        program_studi="SI",
        angkatan=2022,
    )
    with pytest.raises(ValueError, match="sudah terdaftar"):
        daftar_berisi.tambah(duplikat)


def test_hapus_nim_ada(daftar_berisi: DaftarMahasiswa) -> None:
    """Test 11: Hapus NIM yang ada harus mengembalikan True dan mengurangi jumlah."""
    berhasil = daftar_berisi.hapus("22SI001")
    assert berhasil is True
    assert daftar_berisi.jumlah == 0


def test_hapus_nim_tidak_ada(daftar_berisi: DaftarMahasiswa) -> None:
    """Test 12: Hapus NIM yang tidak ada harus mengembalikan False."""
    berhasil = daftar_berisi.hapus("99XX999")
    assert berhasil is False
    assert daftar_berisi.jumlah == 1  # jumlah tidak berubah


def test_cari_nim_tidak_ada(daftar_berisi: DaftarMahasiswa) -> None:
    """Test 13: Mencari NIM yang tidak ada harus mengembalikan None."""
    hasil = daftar_berisi.cari("TIDAKADA")
    assert hasil is None


def test_jumlah_property(daftar_kosong: DaftarMahasiswa) -> None:
    """Test 14: Property jumlah mereflesikan data yang ada secara akurat."""
    assert daftar_kosong.jumlah == 0
    mhs1 = Mahasiswa(nim="22SI010", nama="A", program_studi="SI", angkatan=2022)
    mhs2 = Mahasiswa(nim="22SI011", nama="B", program_studi="SI", angkatan=2022)
    daftar_kosong.tambah(mhs1)
    assert daftar_kosong.jumlah == 1
    daftar_kosong.tambah(mhs2)
    assert daftar_kosong.jumlah == 2
