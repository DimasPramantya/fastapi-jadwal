from fastapi import FastAPI
from contextlib import asynccontextmanager
from exceptions.bad_request_exception import BadRequestException
from exceptions.entity_not_found_exception import EntityNotFoundException, entityNotFoundExceptionHandler
from util.db_connection import init_db
from router.dosen_router import router as dosenRouter
from router.kelas_router import router as kelasRouter
from router.semester_router import router as semesterRouter
from router.ruangan_router import router as ruanganRouter
from router.mata_kuliah_router import router as mataKuliahRouter
from router.slot_router import router as slotRouter
from router.preferensi_jadwal_dosen_router import router as preferensiJadwalDosenRouter
from exceptions.global_exception import *

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(router= dosenRouter, prefix="/api/dosen", tags=["Dosen"])
app.include_router(router = kelasRouter, prefix="/api/kelas", tags=["Kelas"])
app.include_router(router = semesterRouter, prefix="/api/semester", tags=["Semester"])
app.include_router(router=ruanganRouter, prefix="/api/ruangan", tags=["Ruangan"])
app.include_router(router=mataKuliahRouter, prefix="/api/mata-kuliah", tags=["Mata Kuliah"])
app.include_router(router=slotRouter, prefix="/api/slot", tags=["Slot"])
app.include_router(router=preferensiJadwalDosenRouter, prefix="/api/preferensi", tags=["Preferensi Jadwal Dosen"])


app.add_exception_handler(EntityNotFoundException, entityNotFoundExceptionHandler)
app.add_exception_handler(BadRequestException, BadRequestException)
app.add_exception_handler(Exception, serverErrorExceptionHandler)
    

@app.get("/")
async def root():
    return {"message": "Hello World"}