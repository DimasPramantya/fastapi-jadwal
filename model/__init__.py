#/model/__init__.py
from sqlalchemy.orm import declarative_base

Base = declarative_base()

from .dosen_model import Dosen
from .ruangan_model import Ruangan
from .mata_kuliah_model import MataKuliah
from .kelas_model import Kelas
from .slot_model import Slot
from .pengajaran_model import Pengajaran
from .jadwal_model import Jadwal
from .semester_model import Semester
from .slot_model import Slot

