from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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
from router.jadwal_router import router as jadwalRouter;
from router.pengajaran_router import router as PengajaranRouter
from router.principal_router import router as principalRouter
from router.user_router import router as userRouter
from exceptions.global_exception import *

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, PUT, etc.)
    allow_headers=["*"],  # Allow all headers
)

app.include_router(router= principalRouter, prefix="/principal", tags=["Principal"])
app.include_router(router= dosenRouter, prefix="/api/dosen", tags=["Dosen"])
app.include_router(router = kelasRouter, prefix="/api/kelas", tags=["Kelas"])
app.include_router(router = semesterRouter, prefix="/api/semester", tags=["Semester"])
app.include_router(router=ruanganRouter, prefix="/api/ruangan", tags=["Ruangan"])
app.include_router(router=mataKuliahRouter, prefix="/api/mata-kuliah", tags=["Mata Kuliah"])
app.include_router(router=slotRouter, prefix="/api/slot", tags=["Slot"])
app.include_router(router=preferensiJadwalDosenRouter, prefix="/api/preferensi", tags=["Preferensi Jadwal Dosen"])
app.include_router(router=jadwalRouter, prefix="/api/jadwal", tags=["Jadwal"])
app.include_router(router=PengajaranRouter, prefix="/api/pengajaran", tags=["Pengajaran"])
app.include_router(router=userRouter, prefix="/api/user", tags=["User"])


app.add_exception_handler(EntityNotFoundException, entityNotFoundExceptionHandler)
app.add_exception_handler(BadRequestException, BadRequestException)
app.add_exception_handler(Exception, serverErrorExceptionHandler)
    

@app.get("/")
async def root():
    return {"message": "Hello World"}