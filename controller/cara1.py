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

rooms = []

schedules = []

classes = []

course_classes = []

dosen = []

dosen_course_class_mapping = {}

conflict_list_message = []

conflict_list = []

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
                conflict_list.append([teacher.id, course.id, time.id, class_.id, room.id])
                conflict_list_message.append(f"Conflict detected for {class_.nama}: {course.nama} overlaps with {existing_course.nama} on {time.day} at {time.start_time}-{time.end_time}")
                print(f"Conflict detected for {class_.nama}: {course.nama} overlaps with {existing_course.nama} on {time.day} at {time.start_time}-{time.end_time}")
                break  # No need to check further for this slot

        if not conflict:
            class_schedules[class_.nama].append(slot)
            new_schedule.append(slot)
        else:
            new_schedule.append(slot)  # Add the slot even if there is a conflict

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
            existing_course, existing_room, existing_time, _, existing_class = existing_slot
            if existing_time.day == time.day and (
                (existing_time.start_time <= time.start_time < existing_time.end_time) or
                (time.start_time <= existing_time.start_time < time.end_time)
            ):
                conflict = True
                conflict_list.append([teacher.id, course.id, time.id, class_.id, room.id])
                conflict_list.append([teacher.id, existing_course.id, existing_time.id, existing_class.id, existing_room.id])
                conflict_list_message.append(f"Conflict detected for {teacher.nama}: {course.nama} overlaps with {existing_course.nama} on {time.day} at {time.start_time}-{time.end_time}")
                print(f"Conflict detected for {teacher.nama}: {course.nama} overlaps with {existing_course.nama} on {time.day} at {time.start_time}-{time.end_time}")
                break

        if not conflict:
            teacher_schedules[teacher.nama].append(slot)
            new_schedule.append(slot)
        else:
            new_schedule.append(slot)  # Add the slot even if there is a conflict

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

def generate_mengajar_attribute():
    global dosen
    global dosen_course_class_mapping

    for teacher_name, course_map in dosen_course_class_mapping.items():
        for course_name, class_list in course_map.items():
            for dosen_obj in dosen:
                if dosen_obj.nama == teacher_name:
                    dosen_obj.mengajar.append(course_name)

def generate_schedule(_classes, _dosen, _course_classes, _rooms, _schedules, _dosen_course_class_mapping):
    # Example Data
    global classes
    classes = _classes

    global dosen 
    dosen = _dosen

    global course_classes
    course_classes = _course_classes

    global rooms 
    rooms = _rooms

    global schedules 
    schedules = _schedules

    global dosen_course_class_mapping 
    dosen_course_class_mapping = _dosen_course_class_mapping

    generate_mengajar_attribute()

    population_size = 50
    population = create_initial_population(population_size)

    generations = 500
    mutation_rate = 0.05
    initial_temperature = 10000
    cooling_rate = 0.99


    best_solution, best_violating_preferences, ga_fitness_history = genetic_algorithm(population, generations, mutation_rate)
    best_solution, best_violating_preferences, sa_fitness_history = simulated_annealing(best_solution, initial_temperature, cooling_rate)
    combined_fitness_history = ga_fitness_history + sa_fitness_history

    best_solution = enforce_shift_constraints(best_solution)
    best_solution = enforce_no_class_overlap(best_solution)
    best_solution = enforce_no_teacher_overlap(best_solution)

    best_score, _ = fitness(best_solution)  # Calculate the score
    print("Best Solution (Score: {}):".format(int(abs(best_score)/100)))
    
    return best_solution, best_violating_preferences, conflict_list_message, conflict_list