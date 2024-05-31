class Kelas:
    kelas = None

    def __init__(self, name, size, shift="pagi"):  # Tambahkan parameter shift default ke "pagi"
        self.name = name
        self.size = size
        self.shift = shift  # Simpan informasi shift kelas

    @staticmethod
    def find(name):
        for i in range(len(Kelas.kelas)):
            if Kelas.kelas[i].name == name:
                return i
        return -1

    def __repr__(self):
        return f"Kelas: {self.name}, Shift: {self.shift}"


class Dosen:
    dosen = None

    def __init__(self, name, preferred_time_slots=None):
        self.name = name
        self.preferred_time_slots = preferred_time_slots if preferred_time_slots else []

    @staticmethod
    def find(name):
        for i in range(len(Dosen.dosen)):
            if Dosen.dosen[i].name == name:
                return i
        return -1

    def __repr__(self):
        #return "Dosen Pengampu: " + self.name
        return f"Dosen Pengampu: {self.name}, preferred_time_slots: {self.preferred_time_slots}"


class CourseClass:
    classes = None

    def __init__(self, code, is_lab=False):
        self.code = code
        self.is_lab = is_lab

    @staticmethod
    def find(code):
        for i in range(len(CourseClass.classes)):
            if CourseClass.classes[i].code == code:
                return i
        return -1

    def __repr__(self):
        return "Kode Matakuliah: " + self.code


class Room:
    rooms = None

    def __init__(self, name, size, is_lab=False):
        self.name = name
        self.size = size
        self.is_lab = is_lab

    @staticmethod
    def find(name):
        for i in range(len(Room.rooms)):
            if Room.rooms[i].name == name:
                return i
        return -1

    def __repr__(self):
        return "Ruangan:  " + self.name


class Schedule:
    schedules = None

    def __init__(self, start, end, day, is_lab_slot=False):
        self.start = start
        self.end = end 
        self.day = day
        self.is_lab_slot = is_lab_slot

    def __repr__(self):
        return "Pukul :" + self.start + "-" + self.end + " Day: " + self.day