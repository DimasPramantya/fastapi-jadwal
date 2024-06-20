# class Kelas:
#     kelas = None

#     def __init__(self, nama, kapasitas, shift="pagi"):  # Tambahkan parameter shift default ke "pagi"
#         self.nama = nama
#         self.kapasitas = kapasitas
#         self.shift = shift  # Simpan informasi shift kelas

#     @staticmethod
#     def find(nama):
#         for i in range(len(Kelas.kelas)):
#             if Kelas.kelas[i].nama == nama:
#                 return i
#         return -1

#     def __repr__(self):
#         return f"Kelas: {self.nama}, Shift: {self.shift}"


# class Dosen:
#     dosen = None

#     def __init__(self, nama, preferred_time_slots=None):
#         self.nama = nama
#         self.preferred_time_slots = preferred_time_slots if preferred_time_slots else []
#         self.mengajar = []

#     @staticmethod
#     def find(nama):
#         for i in range(len(Dosen.dosen)):
#             if Dosen.dosen[i].nama == nama:
#                 return i
#         return -1

#     def __repr__(self):
#         #return "Dosen Pengampu: " + self.nama
#         return f"Dosen Pengampu: {self.nama}, preferred_time_slots: {self.preferred_time_slots}"


# class CourseClass:
#     classes = None

#     def __init__(self, nama, is_lab=False):
#         self.nama = nama
#         self.is_lab = is_lab

#     @staticmethod
#     def find(nama):
#         for i in range(len(CourseClass.classes)):
#             if CourseClass.classes[i].nama == nama:
#                 return i
#         return -1

#     def __repr__(self):
#         return "Kode Matakuliah: " + self.nama


# class Room:
#     rooms = None

#     def __init__(self, nama, kapasitas, is_lab=False):
#         self.nama = nama
#         self.kapasitas = kapasitas
#         self.is_lab = is_lab

#     @staticmethod
#     def find(nama):
#         for i in range(len(Room.rooms)):
#             if Room.rooms[i].nama == nama:
#                 return i
#         return -1

#     def __repr__(self):
#         return "Ruangan:  " + self.nama


# class Schedule:
#     schedules = None

#     def __init__(self, start_time, end_time, day, is_lab_slot=False):
#         self.start_time = start_time
#         self.end_time = end_time
#         self.day = day
#         self.is_lab_slot = is_lab_slot

#     def __repr__(self):
#         return "Pukul :" + self.start_time + "-" + self.end_time + " Day: " + self.day

class Kelas:
    def __init__(self, id, nama, kapasitas, shift):
        self.id = id
        self.nama = nama
        self.kapasitas = kapasitas
        self.shift = shift
    
    @staticmethod
    def find(nama):
        for i in range(len(Kelas.kelas)):
            if Kelas.kelas[i].nama == nama:
                return i
        return -1

class Dosen:
    def __init__(self, id, nama, preferred_time_slots):
        self.id = id
        self.nama = nama
        self.preferred_time_slots = preferred_time_slots
        self.mengajar = []
    
    @staticmethod
    def find(nama):
        for i in range(len(Dosen.dosen)):
            if Dosen.dosen[i].nama == nama:
                return i
        return -1

class Schedule:
    def __init__(self, id, start_time, end_time, day, is_lab_slot):
        self.id = id
        self.start_time = start_time
        self.end_time = end_time
        self.day = day
        self.is_lab_slot = is_lab_slot

class CourseClass:
    def __init__(self, id, nama, is_lab=False):
        self.id = id
        self.nama = nama
        self.is_lab = is_lab
   
    @staticmethod
    def find(nama):
        for i in range(len(CourseClass.classes)):
            if CourseClass.classes[i].nama == nama:
                return i
        return -1

class Room:
    def __init__(self, id, nama, kapasitas, is_lab=False):
        self.id = id
        self.nama = nama
        self.kapasitas = kapasitas
        self.is_lab = is_lab
    
    @staticmethod
    def find(nama):
        for i in range(len(Room.rooms)):
            if Room.rooms[i].nama == nama:
                return i
        return -1