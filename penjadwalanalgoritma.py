# -*- coding: utf-8 -*-
"""PenjadwalanAlgoritma.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ufPD2x-w38aT9FMv_UnTRCT5nH75MtOO
"""

import random
import math
import matplotlib.pyplot as plt

"""# Definisi Kelas

"""

class Kelas:
    def __init__(self, nama, kapasitas, shift):
        self.nama = nama
        self.kapasitas = kapasitas
        self.shift = shift

class Dosen:
    def __init__(self, nama, preferred_time_slots, mengajar):
        self.nama = nama
        self.preferred_time_slots = preferred_time_slots
        self.mengajar = mengajar  # Menyimpan informasi mata kuliah yang diajar dosen

class Schedule:
    def __init__(self, start_time, end_time, day):
        self.start_time = start_time
        self.end_time = end_time
        self.day = day

class CourseClass:
    def __init__(self, nama, kapasitas, is_lab=False):
        self.nama = nama
        self.kapasitas = kapasitas
        self.is_lab = is_lab

class Room:
    def __init__(self, nama, kapasitas, is_lab=False):
        self.nama = nama
        self.kapasitas = kapasitas
        self.is_lab = is_lab

"""# Dataset"""

# # Example Data
# classes = [
#     Kelas("TI-20-PA", 20, shift="pagi"), Kelas("TI-21-PA", 20, shift="pagi"),
#     Kelas("TI-22-PA", 20, shift="pagi"), Kelas("TI-23-PA", 20, shift="pagi"),
#     Kelas("TI-20-KA", 20, shift="malam"), Kelas('TI-24-PA', 20, shift="pagi"),
#     Kelas('TI-21-KA', 25, shift="malam"), Kelas("TI-25-PA", 20, shift="pagi"),
#     Kelas("TI-26-PA", 20, shift="pagi"), Kelas("TI-27-PA", 20, shift="pagi"),
#     Kelas("TI-28-PA", 20, shift="pagi"), Kelas("TI-22-KA", 20, shift="malam"),
#     Kelas('TI-29-PA', 20, shift="pagi"), Kelas('TI-23-KA', 25, shift="malam"),
#     Kelas("TI-30-PA", 20, shift="pagi"), Kelas("TI-31-PA", 20, shift="pagi"),
#     Kelas("TI-32-PA", 20, shift="pagi"), Kelas("TI-33-PA", 20, shift="pagi"),
#     Kelas("TI-24-KA", 20, shift="malam"), Kelas('TI-34-PA', 20, shift="pagi"),
#     Kelas('TI-25-KA', 25, shift="malam")
# ]

# dosen = [
#     Dosen("Septian Cahyadi", [Schedule("13:15", "15:00", "Thu"), Schedule("20:15", "22:00", "Wed")], mengajar=["Basis Data"]),
#     Dosen("Edi Nurachmad", [Schedule("13:15", "15:00", "Mon"), Schedule("15:15", "17:00", "Mon")], mengajar=["Lab Pemrograman Web"]),
#     Dosen("Anton Sukamto", [Schedule("20:15", "22:00", "Tue"), Schedule("15:15", "17:00", "Tue")], mengajar=["Manajemen Projek"]),
#     Dosen("Febri Damatraseta", [Schedule("13:15", "15:00", "Wed"), Schedule("15:15", "17:00", "Wed")], mengajar=["Kecerdasan Buatan"]),
#     Dosen("Suci Sutjipto", [Schedule("13:15", "15:00", "Fri"), Schedule("15:15", "17:00", "Fri")], mengajar=["Statistika"]),
#     Dosen("Isnan Mulia", [Schedule("13:15", "15:00", "Mon"), Schedule("20:15", "22:00", "Mon")], mengajar=["Jaringan Komputer"]),
#     Dosen("Lina Fithriyah", [Schedule("13:15", "15:00", "Tue"), Schedule("15:15", "17:00", "Tue")], mengajar=["Sistem Operasi"]),
#     Dosen("Dewi Suryati", [Schedule("13:15", "15:00", "Wed"), Schedule("15:15", "17:00", "Wed")], mengajar=["Manajemen Sistem Informasi"]),
#     Dosen("Ahmad Farhan", [Schedule("13:15", "15:00", "Thu"), Schedule("15:15", "17:00", "Thu")], mengajar=["Pemrograman Dasar"]),
#     Dosen("Tina Larasati", [Schedule("13:15", "15:00", "Fri"), Schedule("15:15", "17:00", "Fri")], mengajar=["Algoritma dan Pemrograman"]),
#     Dosen("Yoga Pratama", [Schedule("13:15", "15:00", "Mon"), Schedule("15:15", "17:00", "Mon")], mengajar=["teori graf"]),
#     Dosen("Budi Santoso", [Schedule("13:15", "15:00", "Tue"), Schedule("15:15", "17:00", "Tue")], mengajar=[ "Pemrograman Lanjut"]),
#     Dosen("Rina Suryani", [Schedule("13:15", "15:00", "Wed"), Schedule("15:15", "17:00", "Wed")], mengajar=["Tata kelola"]),
#     Dosen("Gilang Rahman", [Schedule("13:15", "15:00", "Thu"), Schedule("15:15", "17:00", "Thu")], mengajar=["Keamanan Informasi"]),
#     Dosen("Ika Permatasari", [Schedule("13:15", "15:00", "Fri"), Schedule("15:15", "17:00", "Fri")], mengajar=["Rekayasa Perangkat Lunak"]),
#     Dosen("Farah Azmi", [Schedule("13:15", "15:00", "Mon"), Schedule("15:15", "17:00", "Mon")], mengajar=["TIK"]),
#     Dosen("Ali Rahman", [Schedule("13:15", "15:00", "Tue"), Schedule("15:15", "17:00", "Tue")], mengajar=["Matematika Diskrit"]),
#     Dosen("Siti Nurjanah", [Schedule("13:15", "15:00", "Wed"), Schedule("15:15", "17:00", "Wed")], mengajar=["Matematika Dasar"])
# ]

# course_classes = [
#     CourseClass("Basis Data", 20), CourseClass("Tata Kelola TI", 20), CourseClass("Pengantar Teknologi Informasi", 20),
#     CourseClass("Matematika Diskrit", 20), CourseClass("Lab Pemrograman Web", 20, is_lab=True),
#     CourseClass("Kecerdasan Buatan", 20), CourseClass("Manajemen Projek", 20), CourseClass("Matematika Dasar", 20),
#     CourseClass("Jaringan Komputer", 20), CourseClass("Keamanan Informasi", 20), CourseClass("Sistem Operasi", 20),
#     CourseClass("Pemrograman Lanjut", 20), CourseClass("Pemrograman Dasar", 20), CourseClass("Sistem Basis Data", 20),
#     CourseClass("Sistem Informasi", 20), CourseClass("Rekayasa Perangkat Lunak", 20), CourseClass("Manajemen Sistem Informasi", 20),
#     CourseClass("Teori Graf", 20), CourseClass("Algoritma dan Pemrograman", 20), CourseClass("Statistika", 20), CourseClass("TIK", 20)
# ]

rooms = [
    Room("415", 40), Room("409", 40), Room("408", 40), Room("215", 20, is_lab=True), Room("210", 20, is_lab=True),
    Room("411", 40), Room("412", 40), Room("413", 40), Room("214", 20, is_lab=True), Room("211", 20, is_lab=True),
    Room("416", 40), Room("417", 40), Room("418", 40), Room("216", 20, is_lab=True), Room("212", 20, is_lab=True)
]

schedules = [
    Schedule("08:15", "10:00", "Mon"), Schedule("10:15", "12:00", "Mon"),
    Schedule("13:15", "15:00", "Mon"), Schedule("15:15", "17:00", "Mon"),
    Schedule("08:15", "10:00", "Tue"), Schedule("10:15", "12:00", "Tue"),
    Schedule("13:15", "15:00", "Tue"), Schedule("15:15", "17:00", "Tue"),
    Schedule("08:15", "10:00", "Wed"), Schedule("10:15", "12:00", "Wed"),
    Schedule("13:15", "15:00", "Wed"), Schedule("15:15", "17:00", "Wed"),
    Schedule("08:15", "10:00", "Thu"), Schedule("10:15", "12:00", "Thu"),
    Schedule("13:15", "15:00", "Thu"), Schedule("15:15", "17:00", "Thu"),
    Schedule("18:00", "20:00", "Mon"), Schedule("20:15", "22:00", "Mon"),
    Schedule("18:00", "20:00", "Tue"), Schedule("20:15", "22:00", "Tue"),
    Schedule("18:00", "20:00", "Wed"), Schedule("20:15", "22:00", "Wed"),
    Schedule("18:00", "20:00", "Thu"), Schedule("20:15", "22:00", "Thu"),
    Schedule("08:15", "10:00", "Fri"), Schedule("10:15", "12:00", "Fri"),
    Schedule("13:15", "15:00", "Fri"), Schedule("15:15", "17:00", "Fri"),
    Schedule("08:15", "10:00", "Sat"), Schedule("10:15", "12:00", "Sat"),
    Schedule("13:15", "15:00", "Sat"), Schedule("15:15", "17:00", "Sat"),
    Schedule("18:00", "20:00", "Fri"), Schedule("20:15", "22:00", "Fri"),
    Schedule("18:00", "20:00", "Sat"), Schedule("20:15", "22:00", "Sat")
]

# dosen_course_class_mapping = {
#     "Septian Cahyadi": {"Basis Data": ["TI-20-PA", "TI-21-PA"]},
#     "Edi Nurachmad": {"Lab Pemrograman Web": ["TI-22-PA", "TI-23-PA"]},
#     "Anton Sukamto": {"Manajemen Projek": ["TI-24-PA", "TI-25-PA"]},
#     "Febri Damatraseta": {"Kecerdasan Buatan": ["TI-26-PA", "TI-27-PA"]},
#     "Suci Sutjipto": {"Statistika": ["TI-28-PA", "TI-29-PA"]},
#     "Isnan Mulia": {"Jaringan Komputer": ["TI-30-PA", "TI-31-PA"]},
#     "Lina Fithriyah": {"Sistem Operasi": ["TI-32-PA", "TI-33-PA"]},
#     "Dewi Suryati": {"Manajemen Sistem Informasi": ["TI-34-PA"]},
#     "Ahmad Farhan": {"Pemrograman Dasar": ["TI-20-KA", "TI-21-KA"]},
#     "Tina Larasati": {"Algoritma dan Pemrograman": ["TI-22-KA", "TI-23-KA"]},
#     "Budi Santoso": {"Pemrograman Lanjut": ["TI-20-PA", "TI-21-PA"]},
#     "Rina Suryani": {"Tata Kelola TI": ["TI-23-KA", "TI-23-PA"]},
#     "Gilang Rahman": {"Keamanan Informasi": ["TI-24-PA", "TI-25-PA"]},
#     "Ika Permatasari": {"Rekayasa Perangkat Lunak": ["TI-26-PA", "TI-27-PA"]},
#     "Farah Azmi": {"TIK": ["TI-24-PA", "TI-24-KA"]},
#     "Ali Rahman": {"Matematika Diskrit": ["TI-20-PA", "TI-20-KA"]},
#     "Siti Nurjanah": {"Matematika Dasar": ["TI-21-PA", "TI-21-KA"]}
# }

classes = [
    Kelas("PW-22-PB", 20, shift="pagi"), Kelas("PW-22-PA", 20, shift="pagi"),
    Kelas("PW-22-KA", 20, shift="pagi"), Kelas("PW-21-PA", 20, shift="pagi"),
    Kelas("PW-21-PB", 20, shift="pagi"), Kelas("PW-21-KA", 20, shift="pagi")
]


course_classes = [
    CourseClass("Pengantar Aplikasi Komputer",20), CourseClass("Ekologi Wisata & Rekreasi Alam", 20),
    CourseClass("Pengantar Hospitality & Tourism", 20), CourseClass("Bahasa Inggris Untuk Pariwisata 1", 20),
    CourseClass("Perencanaan Pariwisata", 20), CourseClass("Manajemen Pemasaran", 20),
    CourseClass("Pendidikan Karakter", 20), CourseClass("Kewirausahaan", 20),
    CourseClass("Bahasa Inggris Untuk Pariwisata 3", 20), CourseClass("Manajemen Travel", 20),
    CourseClass("Psikologi Pelayanan", 20), CourseClass("Etika Profesional", 20)
]
dosen = [
    Dosen("Febry Lodwyk Rihe Riwoe", [Schedule("08:00", "10:00", "Mon"), Schedule("10:15", "12:15", "Mon")], mengajar=["Pengantar Aplikasi Komputer"]),
    Dosen("Wulandari Dwi Utari", [Schedule("08:00", "10:00", "Tue"), Schedule("10:15", "12:15", "Tue")], mengajar=["Ekologi Wisata & Rekreasi Alam"]),
    Dosen("Sri Endah Yuwantiningrum", [Schedule("08:00", "10:00", "Wed"), Schedule("10:15", "12:15", "Wed")], mengajar=["Pengantar Hospitality & Tourism"]),
    Dosen("Ir. Tarida Marlin Surya Manurung", [Schedule("08:00", "10:00", "Thu"), Schedule("10:15", "12:15", "Thu")], mengajar=["Bahasa Inggris Untuk Pariwisata 1"]),
    Dosen("Ir. Cecilia Valentina Srihadi Suryanti", [Schedule("08:00", "10:00", "Fri"), Schedule("10:15", "12:15", "Fri")], mengajar=["Perencanaan Pariwisata"]),
    Dosen("Bambang Hengky Rainanto", [Schedule("14:00", "16:00", "Mon"), Schedule("16:15", "18:15", "Mon")], mengajar=["Manajemen Pemasaran"]),
    Dosen("Charles Parnauli Saragi", [Schedule("14:00", "16:00", "Tue"), Schedule("16:15", "18:15", "Tue")], mengajar=["Pendidikan Karakter"]),
    Dosen("Mesy Mayangsari", [Schedule("14:00", "16:00", "Wed"), Schedule("16:15", "18:15", "Wed")], mengajar=["Kewirausahaan"]),
    Dosen("Nisa Rahmaniah Utami", [Schedule("14:00", "16:00", "Thu"), Schedule("16:15", "18:15", "Thu")], mengajar=["Bahasa Inggris Untuk Pariwisata 3"]),
    Dosen("Tb. Dicky Faldy S.N.", [Schedule("14:00", "16:00", "Fri"), Schedule("16:15", "18:15", "Fri")], mengajar=["Manajemen Travel"]),
    Dosen("Galih Nugraha", [Schedule("08:00", "10:00", "Mon"), Schedule("10:15", "12:15", "Mon")], mengajar=["Psikologi Pelayanan"]),
    Dosen("Sri Pujiastuti", [Schedule("08:00", "10:00", "Tue"), Schedule("10:15", "12:15", "Tue")], mengajar=["Etika Profesional"])
]

dosen_course_class_mapping = { "Febry Lodwyk Rihe Riwoe": {"Pengantar Aplikasi Komputer": ["PW-22-PB", "PW-22-KA"]}, "Wulandari Dwi Utari": {"Ekologi Wisata & Rekreasi Alam": ["PW-22-PB", "PW-22-KA", "PW-22-PA"]}, "Sri Endah Yuwantiningrum": {"Pengantar Hospitality & Tourism": ["PW-22-PA", "PW-22-PB", "PW-22-KA"]}, "Ir. Tarida Marlin Surya Manurung": {"Bahasa Inggris Untuk Pariwisata 1": ["PW-22-PA", "PW-22-PB", "PW-22-KA"]}, "Ir. Cecilia Valentina Srihadi Suryanti": {"Perencanaan Pariwisata": ["PW-22-PA", "PW-22-PB", "PW-22-KA"]}, "Bambang Hengky Rainanto": {"Manajemen Pemasaran": ["PW-22-PA", "PW-22-PB", "PW-22-KA"]}, "Charles Parnauli Saragi": {"Pendidikan Karakter": ["PW-22-PA", "PW-22-PB", "PW-22-KA"]}, "Mesy Mayangsari": {"Kewirausahaan": ["PW-22-PA", "PW-22-PB", "PW-22-KA"]}, "Nisa Rahmaniah Utami": {"Bahasa Inggris Untuk Pariwisata 3": ["PW-22-PA", "PW-22-PB", "PW-22-KA"]}, "Tb. Dicky Faldy S.N.": {"Manajemen Travel": ["PW-22-PA", "PW-22-PB", "PW-22-KA"]}, "Galih Nugraha": {"Psikologi Pelayanan": ["PW-22-PA", "PW-22-PB", "PW-22-KA"]}, "Sri Pujiastuti": {"Etika Profesional": ["PW-22-PA", "PW-22-PB", "PW-22-KA"]} }

"""# Fungsi Fitness


"""

def fitness(schedule):
    fitness_value = 0
    time_slots = {}
    dosen_mapping = {}
    room_schedule = {}
    class_schedule = {}
    violating_preferences = []

    # Map dosen-mata kuliah-kelas
    for d in dosen:
        for mengajar in d.mengajar:
            for c in classes:
                dosen_mapping[(d.nama, mengajar, c.nama)] = []

    for slot in schedule:
        course, room, time, teacher, class_ = slot

        # Check room capacity
        if room.kapasitas < class_.kapasitas:
            fitness_value -= 1

        # Check if it's a lab class in a lab room
        if course.is_lab and not room.is_lab:
            fitness_value -= 10

        # Check teacher preference
        preference_matched = False
        for pref in teacher.preferred_time_slots:
            if (time.start_time == pref.start_time and
                time.end_time == pref.end_time and
                time.day == pref.day):
                preference_matched = True
                break
        if not preference_matched:
            fitness_value -= 2
            violating_preferences.append(f"{teacher.nama} prefers {time.day} {time.start_time}-{time.end_time}")

        # Check class shift
        if (class_.shift == 'pagi' and time.start_time >= '18:00') or (class_.shift == 'malam' and time.start_time < '18:00'):
            fitness_value -= 5

        # Check for time conflicts
        if (time.start_time, time.day) in time_slots:
            if (room.nama in time_slots[(time.start_time, time.day)] or
                teacher.nama in time_slots[(time.start_time, time.day)] or
                class_.nama in time_slots[(time.start_time, time.day)]):
                fitness_value -= 20  # Heavy penalty for conflict
            else:
                time_slots[(time.start_time, time.day)].append(room.nama)
                time_slots[(time.start_time, time.day)].append(teacher.nama)
                time_slots[(time.start_time, time.day)].append(class_.nama)
        else:
            time_slots[(time.start_time, time.day)] = [room.nama, teacher.nama, class_.nama]

        # Check dosen-mata kuliah-kelas mapping
        if (teacher.nama, course.nama, class_.nama) not in dosen_mapping:
            fitness_value -= 5
        else:
            dosen_mapping[(teacher.nama, course.nama, class_.nama)].append(slot)

        # Track room and class schedules
        if (room.nama, time.start_time, time.day) in room_schedule:
            fitness_value -= 20  # Heavy penalty for room conflict
        else:
            room_schedule[(room.nama, time.start_time, time.day)] = slot

        if (class_.nama, time.start_time, time.day) in class_schedule:
            fitness_value -= 20  # Heavy penalty for class conflict
        else:
            class_schedule[(class_.nama, time.start_time, time.day)] = slot

    # Check if each dosen-mata kuliah-kelas combination has exactly one schedule
    for key, value in dosen_mapping.items():
        if len(value) != 1:
            fitness_value -= 20  # Heavy penalty for multiple schedules or no schedule

    return fitness_value, violating_preferences

"""### enforce constraints"""

def enforce_shift_constraints(schedule):
    # Enforce shift constraints
    new_schedule = []
    for slot in schedule:
        course, room, time, teacher, class_ = slot
        if class_.shift == 'malam' and time.start_time < '18:00':
            # Find a suitable evening time slot
            new_time = next((t for t in schedules if t.start_time >= '18:00'), None)
            if new_time:
                slot = (course, room, new_time, teacher, class_)
        elif class_.shift == 'pagi' and time.start_time >= '18:00':
            # Find a suitable morning time slot
            new_time = next((t for t in schedules if t.start_time < '18:00'), None)
            if new_time:
                slot = (course, room, new_time, teacher, class_)
        new_schedule.append(slot)
    return new_schedule



def enforce_no_class_overlap(schedule):
    """
    Enforces no overlap of courses within the same class and same time slot.
    """
    class_schedules = {}
    new_schedule = []

    for slot in schedule:
        course, room, time, teacher, class_ = slot
        if class_.nama not in class_schedules:
            class_schedules[class_.nama] = []

        # Check for time conflicts within the same class
        conflict = False
        for existing_slot in class_schedules[class_.nama]:
            existing_course, existing_room, existing_time, _, _ = existing_slot
            if existing_time.day == time.day and (
                (existing_time.start_time <= time.start_time < existing_time.end_time) or
                (time.start_time <= existing_time.start_time < time.end_time)
            ):
                conflict = True
                print(f"Conflict detected for {class_.nama}: {course.nama} overlaps with {existing_course.nama} on {time.day} at {time.start_time}-{time.end_time}")
                break  # No need to check further for this slot

        if not conflict:
            class_schedules[class_.nama].append(slot)
            new_schedule.append(slot)

    return new_schedule

def enforce_no_teacher_overlap(schedule):
    """
    Enforces no overlap of courses for the same teacher at the same time.
    """
    teacher_schedules = {}
    new_schedule = []

    for slot in schedule:
        course, room, time, teacher, class_ = slot
        if teacher.nama not in teacher_schedules:
            teacher_schedules[teacher.nama] = []

        # Check for time conflicts for the teacher
        conflict = False
        for existing_slot in teacher_schedules[teacher.nama]:
            existing_course, existing_room, existing_time, _, _ = existing_slot
            if existing_time.day == time.day and (
                (existing_time.start_time <= time.start_time < existing_time.end_time) or
                (time.start_time <= existing_time.start_time < time.end_time)
            ):
                conflict = True
                print(f"Conflict detected for {teacher.nama}: {course.nama} overlaps with {existing_course.nama} on {time.day} at {time.start_time}-{time.end_time}")
                break

        if not conflict:
            teacher_schedules[teacher.nama].append(slot)
            new_schedule.append(slot)

    return new_schedule

"""# Genetic Algorithm"""

def genetic_algorithm(population, generations, mutation_rate):
    fitness_history = []  # To store fitness values for each generation
    for generation in range(generations):
        population = sorted(population, key=lambda x: fitness(x), reverse=True)
        next_generation = population[:2]

        for i in range(len(population) // 2 - 1):
            parent1 = random.choice(population[:10])
            parent2 = random.choice(population[:10])
            child1, child2 = crossover(parent1, parent2)
            next_generation.extend([mutate(child1, mutation_rate), mutate(child2, mutation_rate)])

        population = next_generation
        best_fitness, _ = fitness(population[0])  # Get fitness of the best solution
        fitness_history.append(best_fitness)

    best_solution = population[0]
    _, best_violating_preferences = fitness(best_solution)
    return best_solution, best_violating_preferences, fitness_history


def crossover(parent1, parent2):
    point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2

def mutate(individual, mutation_rate):
    if random.random() < mutation_rate:
        index = random.randint(0, len(individual) - 1)
        course, room, time, teacher, class_ = individual[index]

        # Ensure valid mutation
        valid_teachers = [d for d in dosen if course.nama in d.mengajar]
        if valid_teachers:
            new_teacher = random.choice(valid_teachers)
            valid_classes = dosen_course_class_mapping[new_teacher.nama][course.nama]
            if valid_classes:
                new_class = random.choice([c for c in classes if c.nama in valid_classes])
                new_room = random.choice([r for r in rooms if r.kapasitas >= new_class.kapasitas and (course.is_lab == r.is_lab)])
                new_time = random.choice(schedules)
                individual[index] = (course, new_room, new_time, new_teacher, new_class)
    return individual

"""# Simulated Annealing"""

def simulated_annealing(solution, temperature, cooling_rate):
    fitness_history = []  # To store fitness values for each iteration
    current_solution = solution
    current_fitness, current_violating_preferences = fitness(current_solution)
    fitness_history.append(current_fitness)

    while temperature > 1:
        new_solution = mutate(current_solution[:], 1.0)
        new_fitness, new_violating_preferences = fitness(new_solution)

        if (new_fitness, len(new_violating_preferences)) > (current_fitness, len(current_violating_preferences)) or \
           math.exp(((new_fitness - current_fitness) - (len(new_violating_preferences) - len(current_violating_preferences))) / temperature) > random.random():
            current_solution, current_fitness, current_violating_preferences = new_solution, new_fitness, new_violating_preferences

        fitness_history.append(current_fitness)
        temperature *= cooling_rate

    return current_solution, current_violating_preferences, fitness_history

"""# Initial Population

"""

def create_initial_population(population_size):
    population = []
    for _ in range(population_size):
        schedule = []
        for teacher, courses in dosen_course_class_mapping.items():
            for course_name, class_list in courses.items():
                for class_name in class_list:
                    # Use a try-except block to handle potential errors
                    try:
                        course = next(c for c in course_classes if c.nama == course_name)
                        class_ = next(cl for cl in classes if cl.nama == class_name)
                        teacher_obj = next(t for t in dosen if t.nama == teacher)
                        room = random.choice([r for r in rooms if r.kapasitas >= class_.kapasitas and (course.is_lab == r.is_lab)])
                        time = random.choice(schedules)
                        schedule.append((course, room, time, teacher_obj, class_))
                    except StopIteration:
                        print(f"Warning: No match found for course: {course_name}, class: {class_name}, or teacher: {teacher}")
        population.append(schedule)
    return population

# Initial Population
population_size = 50
population = create_initial_population(population_size)

"""### Notes

**Parameter:**
* populasi: Daftar jadwal (setiap jadwal adalah daftar tupel yang mewakili mata pelajaran, ruangan, slot waktu, guru, dan kelas).
* generasi: Jumlah iterasi/generasi untuk menjalankan algoritma genetika.
* mutasi_rate: Kemungkinan mutasi pada algoritma genetika.
**Step:**
* Inisialisasi: dimulai dengan populasi awal jadwal.
* Evaluasi fitness: Evaluasi fitness setiap jadwal menggunakan fungsi fitness.
* Seleksi: Pilih jadwal berkinerja terbaik (elit) untuk menjadi bagian dari generasi berikutnya tanpa perubahan.
* Crossover: Memilih secara acak orang tua dari populasi saat ini, melakukan crossover untuk menghasilkan keturunan (anak).
* Mutasi: Mutasi keturunannya dengan probabilitas tertentu (mutation_rate).
* Replacement: Menggantikan populasi saat ini dengan jadwal generasi baru.
Iterasi: Ulangi proses ini selama beberapa generasi tertentu.

**Output**
best_solution: Jadwal terbaik yang ditemukan setelah semua generasi.
best_violating_preferences: Daftar preferensi yang melanggar dalam solusi terbaik.
fitness_history: Daftar berisi skor kebugaran terbaik untuk setiap generasi

# Parameters
"""

generations = 500
mutation_rate = 0.05
initial_temperature = 10000
cooling_rate = 0.99

"""# Running the hybrid"""

# Running the hybrid algorithm
best_solution, best_violating_preferences, ga_fitness_history = genetic_algorithm(population, generations, mutation_rate)
best_solution, best_violating_preferences, sa_fitness_history = simulated_annealing(best_solution, initial_temperature, cooling_rate)
combined_fitness_history = ga_fitness_history + sa_fitness_history

# Enforce shift constraints
best_solution = enforce_shift_constraints(best_solution)
best_solution = enforce_no_class_overlap(best_solution)
best_solution = enforce_no_teacher_overlap(best_solution)

# Print the best solution and score
best_score, _ = fitness(best_solution)  # Calculate the score
print("Best Solution (Score: {}):".format(int(abs(best_score)/100)))
class_schedules = {}  # Dictionary to store schedules by class

for slot in best_solution:
    course, room, time, teacher, class_ = slot
    print(f"Course {course.nama} in Room {room.nama} at {time.start_time}-{time.end_time} on {time.day} by {teacher.nama} for Class {class_.nama}")


# Print the violating preferences
if best_violating_preferences:
    print("\nViolating Preferences:")
    for pref in best_violating_preferences:
        print(pref)
else:
    print("\nNo violating preferences found.")

"""# Visualization"""

# Graphical Schedule
days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
time_slots = ["08:15-10:00", "10:15-12:00", "13:15-15:00", "15:15-17:00", "18:00-20:00", "20:15-22:00"]

class_schedules = {}  # Dictionary to store schedules by class

for slot in best_solution:
    course, room, time, teacher, class_ = slot
    if class_.nama not in class_schedules:
        class_schedules[class_.nama] = []
    class_schedules[class_.nama].append((course.nama, room.nama, time.day, time.start_time, time.end_time, teacher.nama))

for class_name, schedule in class_schedules.items():
    fig, ax = plt.subplots(figsize=(5, 3))

    for slot in schedule:
        course, room, day, time_start, time_end, teacher = slot
        day_index = days.index(day)
        time_index = time_slots.index(f"{time_start}-{time_end}")
        ax.text(day_index, time_index, f"{course}\n{room}\n{teacher}",
                ha="center", va="center", bbox=dict(facecolor='lightblue', edgecolor='black', boxstyle='round,pad=0.5'))

    ax.set_xticks(range(len(days)))
    ax.set_xticklabels(days)
    ax.set_yticks(range(len(time_slots)))
    ax.set_yticklabels(time_slots)
    ax.set_xlabel("Day")
    ax.set_ylabel("Time Slot")
    ax.set_title(f"Schedule for Class {class_name}")

    plt.show()

"""# Fitness History Plot"""

# Plot Fitness History for Genetic Algorithm
plt.figure(figsize=(10, 5))
plt.plot(ga_fitness_history)
plt.xlabel("Generation")
plt.ylabel("Fitness Score")
plt.title("Genetic Algorithm - Fitness over Generations")
plt.grid(True)
plt.show()

# Plot Fitness History for Simulated Annealing
plt.figure(figsize=(10, 5))
plt.plot(sa_fitness_history)
plt.xlabel("Iteration")
plt.ylabel("Fitness Score")
plt.title("Simulated Annealing - Fitness over Iterations")
plt.grid(True)
plt.show()

# Plot Combined Fitness History for Hybrid Algorithm
plt.figure(figsize=(10, 5))
plt.plot(combined_fitness_history)
plt.xlabel("Generation/Iteration")
plt.ylabel("Fitness Score")
plt.title("Hybrid Algorithm (Genetic Algorithm + Simulated Annealing) - Fitness over Generations/Iterations")
plt.grid(True)
plt.show()

"""# Convert data for google calendar"""

import json
from datetime import datetime, timedelta
import pytz # Import the pytz library

def solution_to_google_calendar_json(best_solution, timezone="Asia/Jakarta"):
    """Converts the scheduling solution to a JSON format for Google Calendar events."""
    events = []
    tz = pytz.timezone(timezone) # Create a timezone object
    for slot in best_solution:
        course, room, time, teacher, class_ = slot

        start_time_str = time.start_time.split(":")
        start_time = datetime(2024, 6, 16, int(start_time_str[0]), int(start_time_str[1]), tzinfo=tz)  # Assuming date
        end_time = datetime(2024, 6, 16, int(time.end_time.split(":")[0]), int(time.end_time.split(":")[1]), tzinfo=tz)  # Assuming date

        # Find the corresponding day in the upcoming week (assuming today is Sunday)
        today = datetime.now(tz)
        days_ahead = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"].index(time.day)
        event_date = today + timedelta(days=days_ahead)

        # Update start and end times with the correct date
        start_time = start_time.replace(year=event_date.year, month=event_date.month, day=event_date.day)
        end_time = end_time.replace(year=event_date.year, month=event_date.month, day=event_date.day)

        event = {
            'summary': f"{course.nama} - {teacher.nama}",
            'location': room.nama,
            'description': f"Class: {class_.nama}",
            'start': {
                'dateTime': start_time.isoformat(),
                'timeZone': timezone,
            },
            'end': {
                'dateTime': end_time.isoformat(),
                'timeZone': timezone,
            },
            'attendees': [
                {'email': teacher.email if hasattr(teacher, 'email') else f"{teacher.nama.lower().replace(' ', '')}@ibik.ac.id"}
            ]
        }
        events.append(event)

    return events

calendar_events = solution_to_google_calendar_json(best_solution)

# Save the calendar events to a JSON file
with open("calendar_events.json", "w") as outfile:
    json.dump(calendar_events, outfile)