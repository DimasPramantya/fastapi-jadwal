from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func, text
from typing import List

from model.mata_kuliah_model import MataKuliah as MataKuliahModel
from model.dosen_model import Dosen as DosenModel
from model.jadwal_sementara import JadwalSementara as JadwalSementaraModel
from model.jadwal_model import Jadwal as JadwalModel
from model.kelas_model import Kelas as KelasModel
from model.ruangan_model import Ruangan as RuanganModel
from model.pengajaran_model import Pengajaran as PengajaranModel
from model.slot_model import Slot as SlotModel
from exceptions.entity_not_found_exception import EntityNotFoundException
from exceptions.bad_request_exception import BadRequestException
from .cara1 import generate_schedule
from datetime import date, timedelta, datetime
from schemas.jadwal_sementara_schema import jadwal_sementara_to_dict

from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import RedirectResponse
from google_auth_oauthlib.flow import InstalledAppFlow, Flow
from googleapiclient.discovery import build
import secrets
import jwt  
import time  
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from pydantic import BaseModel
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
import os
import pytz

from dotenv import load_dotenv

load_dotenv()

TOKEN_URI=os.getenv("TOKEN_URI")
CLIENT_ID=os.getenv("CLIENT_ID")
CLIENT_SECRET=os.getenv("CLIENT_SECRET")
JWT_SECRET_KEY=os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM=os.getenv("JWT_ALGORITHM")

from .Classes import *
#from .algorithm import * 

async def generateJadwalSementara(session: AsyncSession):
    # FETCH KELAS
    result = await session.execute(select(KelasModel).limit(100).offset(0))
    kelas_list = result.scalars().all()
    Kelas.kelas = [Kelas(k.id, k.nama_kelas, k.kuota, k.shift) for k in kelas_list]

    # FETCH DOSEN & PREFERENSI
    result = await session.execute(select(DosenModel).limit(100).offset(0))
    dosen_list = result.scalars().all()
    Dosen.dosen = []
    for dosen in dosen_list:
        preferred_time_slots = [Schedule(pref.slot.id, pref.slot.start_time.strftime("%H:%M"), 
                                         pref.slot.end_time.strftime("%H:%M"), 
                                         pref.slot.day.lower(), pref.slot.is_lab_slot) 
                                for pref in dosen.preferensi_jadwal_dosen if pref.slot]
        Dosen.dosen.append(Dosen(dosen.id, dosen.nama_depan + " " + dosen.nama_belakang, preferred_time_slots))

    # FETCH COURSE
    result = await session.execute(select(MataKuliahModel).limit(100).offset(0))
    mata_kuliah_list = result.scalars().all()
    CourseClass.classes = [CourseClass(mk.id, mk.nama_mata_kuliah, mk.is_lab) for mk in mata_kuliah_list]

    # FETCH ROOM
    result = await session.execute(select(RuanganModel).limit(100).offset(0))
    ruangan_list = result.scalars().all()
    Room.rooms = [Room(r.id, r.nama_ruangan, r.kapasitas, r.is_lab) for r in ruangan_list]

    # FETCH SCHEDULE
    result = await session.execute(select(SlotModel).limit(100).offset(0))
    slot_list = result.scalars().all()
    Schedule.schedules = [Schedule(s.id, s.start_time.strftime("%H:%M"), s.end_time.strftime("%H:%M"), s.day, s.is_lab_slot) for s in slot_list]

    # FETCH CPG
    result = await session.execute(select(PengajaranModel).limit(100).offset(0))
    pengajaran_list = result.scalars().all()
    cpg = []
    for pengajaran in pengajaran_list:
        course_index = CourseClass.find(pengajaran.mata_kuliah.nama_mata_kuliah)
        dosen_index = Dosen.find(pengajaran.dosen.nama_depan + " " + pengajaran.dosen.nama_belakang)
        kelas_index = Kelas.find(pengajaran.kelas.nama_kelas)
        if course_index != -1 and dosen_index != -1 and kelas_index != -1:
            cpg.extend([course_index, dosen_index, kelas_index])

    # Map the indices to namas for the desired dictionary
    dosen_course_class_mapping = {}
    for i in range(0, len(cpg), 3):
        course_index = cpg[i]
        dosen_index = cpg[i + 1]
        kelas_index = cpg[i + 2]
        course_nama = CourseClass.classes[course_index].nama
        dosen_nama = Dosen.dosen[dosen_index].nama
        kelas_nama = Kelas.kelas[kelas_index].nama
        if dosen_nama not in dosen_course_class_mapping:
            dosen_course_class_mapping[dosen_nama] = {}
        if course_nama not in dosen_course_class_mapping[dosen_nama]:
            dosen_course_class_mapping[dosen_nama][course_nama] = []
        dosen_course_class_mapping[dosen_nama][course_nama].append(kelas_nama)
    
    print(Dosen.dosen)
    pengajaran_list = []

    # RUN THE ALGORITHM
    best_solution, best_violating_preferences, conflict_list_message, conflict_list = generate_schedule(Kelas.kelas, Dosen.dosen, CourseClass.classes, Room.rooms, Schedule.schedules, dosen_course_class_mapping)
    #delete data in temp table
    query = text("""
        DELETE FROM jadwal_sementara
    """)
    result = await session.execute(query)

    for e in best_solution:
        course, room, time, teacher, class_ = e
        check = False
        courseId = CourseClass.classes[CourseClass.find(course.nama)].id
        kelasId = Kelas.kelas[Kelas.find(class_.nama)].id
        dosenId = Dosen.dosen[Dosen.find(teacher.nama)].id
        for c in conflict_list:
            if dosenId == c[0] and courseId == c[1] and time.id == c[2] and kelasId == c[3] and room.id == c[4]:
                check = True
        query = text("""
            SELECT id, id_kelas, id_dosen, id_mata_kuliah, id_semester
            FROM pengajaran 
            WHERE id_mata_kuliah = :courseId AND id_kelas = :kelasId AND id_dosen = :dosenId
        """)
        result = await session.execute(query, {"courseId": courseId, "kelasId": kelasId, "dosenId": dosenId})
        pengajaran = result.fetchone()
        
        query = text("""
            INSERT INTO jadwal_sementara (id_slot, id_ruangan, id_pengajaran, is_conflicted, created_at, updated_at)
            VALUES (:idSlot, :idRuangan, :idJadwal, :check, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        """)
        result = await session.execute(query, {"idSlot": time.id, "idRuangan": room.id, "idJadwal": pengajaran.id, "check": check})
        await session.commit()
        print(f"Course {course.nama} in Room {room.nama} at {time.start_time}-{time.end_time} on {time.day} by {teacher.nama} for Class {class_.nama}")
    
    print("panjang: ", len(pengajaran_list))
    print(conflict_list)
    return best_violating_preferences, conflict_list_message

async def getJadwalSementaraPageable(session: AsyncSession, skip: int = 0, limit: int = 10) -> List[JadwalSementaraModel]:
    result = await session.execute(
        select(JadwalSementaraModel).offset(skip).limit(limit).order_by(JadwalSementaraModel.is_conflicted)
    )
    jadwal_list = result.scalars().all()
    return jadwal_list

async def getJadwalSementaraCount(session: AsyncSession) -> int:
    result = await session.execute(select(func.count(JadwalSementaraModel.id)))
    count = result.scalar_one()
    return count

async def generateJadwal(token, session: AsyncSession):
    payload = verify_token(token)
    if not payload:
        raise BadRequestException("Invalid token")
    creds = Credentials(
        token=payload['token'],
        refresh_token=None,
        token_uri=TOKEN_URI,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        scopes=["https://www.googleapis.com/auth/calendar.events", "https://www.googleapis.com/auth/userinfo.profile", "openid", "https://www.googleapis.com/auth/userinfo.email"]
    )

    service = build("calendar", "v3", credentials=creds)
    result = await session.execute(select(func.count(JadwalSementaraModel.id)))
    count = result.scalar_one()
    result = await session.execute(
        select(JadwalSementaraModel).offset(0).limit(count)
    )
    jadwal_list = result.scalars().all()
    start_date = date(2024, 8, 17)
    end_date = date(2024, 12, 31)
    jakarta_tz = pytz.timezone('Asia/Jakarta')
    for e in jadwal_list:
        jadwal = jadwal_sementara_to_dict(e)
        dates = get_dates_by_day(jadwal["slot"]["day"], start_date, end_date)
        for d in dates:
            jadwal = JadwalModel(
                id_slot=e.id_slot,
                id_ruangan=e.id_ruangan,
                id_pengajaran=e.id_pengajaran,
                is_created=False,
                start_date_time=datetime.combine(d, e.slot.start_time),
                end_date_time=datetime.combine(d, e.slot.end_time)
            )
            if(e.pengajaran.dosen.email):
                event = {
                    "summary": e.pengajaran.kelas.nama_kelas + " - " + e.pengajaran.mata_kuliah.nama_mata_kuliah,
                    "start": {"dateTime": jadwal.start_date_time.astimezone(pytz.utc).isoformat(), "timeZone": "Asia/Jakarta"},
                    "end": {"dateTime": jadwal.end_date_time.astimezone(pytz.utc).isoformat(), "timeZone": "Asia/Jakarta"},
                    "location": "ruangan " + e.ruangan.nama_ruangan,
                    "attendees": [{"email": e.pengajaran.dosen.email}]
                }
                event = service.events().insert(calendarId="primary", body=event).execute()
            session.add(jadwal)
        await session.commit()
        print(dates)
    return 

def get_dates_by_day(day_name, start_date: date, end_date: date):
    day_name_to_weekday = {
        'Mon': 0,
        'Tue': 1,
        'Wed': 2,
        'Thu': 3, 
        'Fri': 4, 
        'Sat': 5,
        'Sun': 6
    }

    if day_name not in day_name_to_weekday:
        raise ValueError(f"Invalid day name: {day_name}")

    target_weekday = day_name_to_weekday[day_name]

    current_date = start_date
    while current_date.weekday() != target_weekday:
        current_date += timedelta(days=1)

    target_dates = []
    while current_date <= end_date:
        target_dates.append(current_date)
        current_date += timedelta(weeks=1)

    return target_dates

def verify_token(token):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None