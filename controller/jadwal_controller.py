from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from typing import List
from .scheduler import generate_schedule

from schemas.kelas_schema import KelasCreate, KelasUpdate, Kelas as KelasSchema, kelas_model_to_dict
from model.mata_kuliah_model import MataKuliah as MataKuliahModel
from model.dosen_model import Dosen as DosenModel
from model.kelas_model import Kelas as KelasModel
from model.ruangan_model import Ruangan as RuanganModel
from model.pengajaran_model import Pengajaran as PengajaranModel
from model.slot_model import Slot as SlotModel
from schemas.mata_kuliah_schema import mata_kuliah_model_to_dict
from schemas.ruangan_schema import ruangan_model_to_dict
from schemas.slot_schema import slot_model_to_dict
from schemas.pengajaran_schema import pengajaran_model_to_dict
from exceptions.entity_not_found_exception import EntityNotFoundException
from exceptions.bad_request_exception import BadRequestException

from .Classes import *
#from .algorithm import *

async def generateJadwal(
    session: AsyncSession
):
    #FETCH KELAS
    result = await session.execute(
        select(KelasModel).limit(100).offset(0)
    )
    kelas_list = result.scalars().all()
    kelas_dict = [kelas_model_to_dict(d) for d in kelas_list]
    Kelas.kelas = [Kelas(name=k["nama_kelas"], size=k["kuota"], shift=k.get("shift", "pagi")) for k in kelas_dict]
    print(Kelas.kelas)

    #FETCH DOSEN & PREFERENSI
    result = await session.execute(
        select(DosenModel).offset(0).limit(100)
    )
    dosen_list = result.scalars().all()
    
    Dosen.dosen = []
    for dosen in dosen_list:
        preferred_time_slots = []
        for pref in dosen.preferensi_jadwal_dosen:  # Iterate through preferences
            if pref.slot:
                preferred_time_slots.append(Schedule(
                    pref.slot.start_time.strftime("%H:%M"),  # Format start_time
                    pref.slot.end_time.strftime("%H:%M"),    # Format end_time
                    pref.slot.day.lower()                     # Make day lowercase
                ))

        Dosen.dosen.append(Dosen(dosen.nama_depan + " " + dosen.nama_belakang, preferred_time_slots=preferred_time_slots))

    print(Dosen.dosen)  # To verify the output
    print("Panjang dosen adalah" + str(len(Dosen.dosen)))

    #FETCH COURSE
    result = await session.execute(
        select(MataKuliahModel).limit(100).offset(0)
    )
    mata_kuliah_list = result.scalars().all()
    mataKuliahDict = [mata_kuliah_model_to_dict(d) for d in mata_kuliah_list]
    CourseClass.classes = [CourseClass(code=k["nama_mata_kuliah"], is_lab=k["is_lab"]) for k in mataKuliahDict]
    print("element kelas")
    print(CourseClass.classes)

    #Fetch room
    result = await session.execute(
        select(RuanganModel).limit(100).offset(0)
    )
    ruanganList = result.scalars().all()
    ruanganDict = [ruangan_model_to_dict(d) for d in ruanganList]
    Room.rooms = [Room(name=k["nama_ruangan"], size=k["kapasitas"], is_lab=k["is_lab"]) for k in ruanganDict]
    print(Room.rooms)

    #Fetch schedule
    result = await session.execute(
        select(SlotModel).offset(0).limit(100)
    )
    slot_list = result.scalars().all()
    slotDict = [slot_model_to_dict(d) for d in slot_list]
    Schedule.schedules = [Schedule(start=k["start_time"].strftime("%H:%M"), end=k["end_time"].strftime("%H:%M"), day=k["day"], is_lab_slot=k["is_lab_slot"]) for k in slotDict]
    print(Schedule.schedules)

    #FETCH CPG
    result = await session.execute(
        select(PengajaranModel).limit(100).offset(0)
    )
    pengajaran_list = result.scalars().all()
    pengajaranDict = [pengajaran_model_to_dict(d) for d in pengajaran_list]
    cpg = []
    for pengajaran in pengajaran_list:
        course_index = CourseClass.find(pengajaran.mata_kuliah.nama_mata_kuliah)
        dosen_index = Dosen.find(pengajaran.dosen.nama_depan + " " + pengajaran.dosen.nama_belakang)
        kelas_index = Kelas.find(pengajaran.kelas.nama_kelas)

        if course_index != -1 and dosen_index != -1 and kelas_index != -1:
            cpg.extend([course_index, dosen_index, kelas_index])
 
    generate_schedule(Kelas.kelas, Dosen.dosen, CourseClass.classes, Room.rooms, Schedule.schedules, cpg)

    return cpg
