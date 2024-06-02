import random
import copy
from .Classes import *
from math import ceil, log2
import math
import time
import json
#from ics import Calendar, Event
from datetime import datetime, timedelta
#import matplotlib.pyplot as plt
max_score = None
cpg = []
lts = []
slots = []
bits_needed_backup_store = {}

def initialize_globals():
    global Kelas, Dosen, CourseClass, Room, Schedule
    Kelas.kelas = []
    Dosen.dosen = []
    CourseClass.classes = []
    Room.rooms = []
    Schedule.schedules = []

initialize_globals()

def bits_needed(x):
    global bits_needed_backup_store
    r = bits_needed_backup_store.get(id(x))
    if r is None:
        r = int(ceil(log2(len(x))))
        bits_needed_backup_store[id(x)] = r
    return max(r, 1)


def join_cpg_pair(_cpg):
    res = []
    for i in range(0, len(_cpg), 3):
        res.append(_cpg[i] + _cpg[i + 1] + _cpg[i + 2])
    return res


def convert_input_to_bin():
    global cpg, lts, slots, max_score
    print(cpg)

    for _c in range(len(cpg)):
        if _c % 3:  # CourseClass
            cpg[_c] = (bin(cpg[_c])[2:]).rjust(bits_needed(CourseClass.classes), '0')
        elif _c % 3 == 1:  # Dosen
            cpg[_c] = (bin(cpg[_c])[2:]).rjust(bits_needed(Dosen.dosen), '0')
        else:  # Kelas
            cpg[_c] = (bin(cpg[_c])[2:]).rjust(bits_needed(Kelas.kelas), '0')

    cpg = join_cpg_pair(cpg)
    for r in range(len(Room.rooms)):
        lts.append((bin(r)[2:]).rjust(bits_needed(Room.rooms), '0'))

    for t in range(len(Schedule.schedules)):
        slots.append((bin(t)[2:]).rjust(bits_needed(Schedule.schedules), '0'))

    max_score = (len(cpg) - 1) * 3 + len(cpg) * 3


def course_bits(chromosome):
    i = 0

    return chromosome[i:i + bits_needed(CourseClass.classes)]


def dosen_bits(chromosome):
    i = bits_needed(CourseClass.classes)

    return chromosome[i: i + bits_needed(Dosen.dosen)]


def kelas_bits(chromosome):
    i = bits_needed(CourseClass.classes) + bits_needed(Dosen.dosen)

    return chromosome[i:i + bits_needed(Kelas.kelas)]


def slot_bits(chromosome):
    i = bits_needed(CourseClass.classes) + bits_needed(Dosen.dosen) + \
        bits_needed(Kelas.kelas)

    return chromosome[i:i + bits_needed(Schedule.schedules)]


def lt_bits(chromosome):
    i = bits_needed(CourseClass.classes) + bits_needed(Dosen.dosen) + \
        bits_needed(Kelas.kelas) + bits_needed(Schedule.schedules)

    return chromosome[i: i + bits_needed(Room.rooms)]


def slot_clash(a, b):
    if slot_bits(a) == slot_bits(b):
        return 1
    return 0

def dosen_preferred_time_slots(chromosomes):
    scores = 0
    for _c in chromosomes:
        dosen_index = int(dosen_bits(_c), 2)
        dosen = Dosen.dosen[dosen_index]
        slot_index = int(slot_bits(_c), 2)
        preferred_slots = dosen.preferred_time_slots
        if Schedule.schedules[slot_index] in preferred_slots:
            scores += 1
    return scores


# checks that a faculty member teaches only one course at a time.
def faculty_member_one_class(chromosome):
    scores = 0
    for i in range(len(chromosome) - 1):  # select one cpg pair
        clash = False
        for j in range(i + 1, len(chromosome)):  # check it with all other cpg pairs
            if slot_clash(chromosome[i], chromosome[j])\
                    and dosen_bits(chromosome[i]) == dosen_bits(chromosome[j]):
                clash = True
        if not clash:
            scores = scores + 1
    return scores


# check that a kelas member takes only one class at a time.
def kelas_member_one_class(chromosomes):
    scores = 0

    for i in range(len(chromosomes) - 1):
        clash = False
        for j in range(i + 1, len(chromosomes)):
            if slot_clash(chromosomes[i], chromosomes[j]) and\
                    kelas_bits(chromosomes[i]) == kelas_bits(chromosomes[j]):
                clash = True
                break
        if not clash:
            scores = scores + 1
    return scores


# checks that a course is assigned to an available classroom. 
def use_spare_classroom(chromosome):
    scores = 0
    for i in range(len(chromosome) - 1):  # select one cpg pair
        clash = False
        for j in range(i + 1, len(chromosome)):  # check it with all other cpg pairs
            if slot_clash(chromosome[i], chromosome[j]) and lt_bits(chromosome[i]) == lt_bits(chromosome[j]):
                clash = True
        if not clash:
            scores = scores + 1
    return scores


# checks that the classroom capacity is large enough for the classes that
def classroom_size(chromosomes):
    scores = 0
    for _c in chromosomes:
        if Kelas.kelas[int(kelas_bits(_c), 2)].size <= Room.rooms[int(lt_bits(_c), 2)].size:
            scores = scores + 1
    return scores

# check that room is appropriate for particular class/lab
def appropriate_room(chromosomes):
    scores = 0
    for _c in chromosomes:
        room_index = int(lt_bits(_c), 2)
        room = Room.rooms[room_index]
        class_index = int(course_bits(_c), 2)
        course_class = CourseClass.classes[class_index]
        if room.is_lab == course_class.is_lab:
            scores += 1
    return scores


# check that lab is allocated appropriate time slot
def appropriate_timeslot(chromosomes):
    scores = 0
    for _c in chromosomes:
        class_index = int(course_bits(_c), 2)
        course_class = CourseClass.classes[class_index]
        slot_index = int(slot_bits(_c), 2)
        if course_class.is_lab == Schedule.schedules[slot_index].is_lab_slot:
            scores += 1
    return scores

MAX_EVENING_SCHEDULE = {
    "mon": Schedule("18:00", "22:00", "mon"),
    "tue": Schedule("18:00", "22:00", "tue"),
    "wed": Schedule("18:00", "22:00", "wed"),
    "thu": Schedule("18:00", "22:00", "thu"),
}

def is_evening_class(class_index, slot_index):
    class_shift = Kelas.kelas[class_index].shift
    schedule_day = Schedule.schedules[slot_index].day
    max_evening_schedule = MAX_EVENING_SCHEDULE.get(schedule_day)
    
    # Periksa apakah max_evening_schedule adalah None
    if max_evening_schedule is None:
        return False
    
    # Ambil waktu mulai dan waktu akhir dari jadwal kelas
    class_start_time = Schedule.schedules[slot_index].start
    class_end_time = Schedule.schedules[slot_index].end
    
    # Ambil waktu mulai dan waktu akhir dari batas waktu maksimum untuk kelas malam
    max_evening_start_time = max_evening_schedule.start
    max_evening_end_time = max_evening_schedule.end
    
    # Jika shift adalah malam dan waktu mulai kelas di bawah jam 18:00, maka kelas bukanlah kelas malam
    if class_shift == "malam" and class_start_time >= max_evening_start_time and class_end_time <= max_evening_end_time:
        return True
    
    # Jika shift adalah pagi dan waktu mulai kelas di atas jam 18:00, maka kelas bukanlah kelas malam
    if class_shift == "pagi" and class_start_time < max_evening_start_time:
        return True
    
    return False


def evaluate(chromosomes):
    global max_score
    print("inside evaluate")
    score = 0
    score = score + use_spare_classroom(chromosomes)
    score = score + faculty_member_one_class(chromosomes)
    score = score + classroom_size(chromosomes)
    score = score + kelas_member_one_class(chromosomes)
    score = score + appropriate_room(chromosomes)
    score = score + appropriate_timeslot(chromosomes)
    score += dosen_preferred_time_slots(chromosomes)

    # Tambahkan evaluasi khusus untuk jadwal kelas malam
    for chromosome in chromosomes:
        class_index = int(kelas_bits(chromosome), 2)
        slot_index = int(slot_bits(chromosome), 2)
        if not is_evening_class(class_index, slot_index):
            score -= 1  # Penalti untuk jadwal kelas malam di bawah jam 18:00
    
    score = max(1, score)  # Ensure score is at least 1
    return score / max_score
    

def cost(solution):
    return 1 / float(evaluate(solution))

def init_population(n):
    global cpg, lts, slots
    chromosomes = []
    for _n in range(n):
        chromosome = []
        for _c in cpg:
            chromosome.append(_c + random.choice(slots) + random.choice(lts))
        chromosomes.append(chromosome)
    return chromosomes


# Modified Combination of Row_reselect, Column_reselect
def mutate(chromosome):
    rand_slot = random.choice(slots)
    rand_lt = random.choice(lts)
    a = random.randint(0, len(chromosome) - 1)
    chromosome[a] = course_bits(chromosome[a]) + dosen_bits(chromosome[a]) +\
        kelas_bits(chromosome[a]) + rand_slot + rand_lt

def crossover(population):
    a = random.randint(0, len(population) - 1)
    b = random.randint(0, len(population) - 1)
    cut = random.randint(0, len(population[0]))  # assume all chromosome are of same len
    population.append(population[a][:cut] + population[b][cut:])
    

def selection(population, n):
    population.sort(key=evaluate, reverse=True)
    while len(population) > n:
        population.pop()


def print_chromosome(chromosome):
    print(
          Schedule.schedules[int(slot_bits(chromosome), 2)],"|",
          Room.rooms[int(lt_bits(chromosome), 2)],'|',
          Kelas.kelas[int(kelas_bits(chromosome), 2)], " | ",
          CourseClass.classes[int(course_bits(chromosome), 2)], " | ",
          Dosen.dosen[int(dosen_bits(chromosome), 2)]
          )

# Simple Searching Neighborhood
# It randomly changes timeslot of a class/lab
def ssn(solution):
    rand_slot = random.choice(slots)
    rand_lt = random.choice(lts)
    a = random.randint(0, len(solution) - 1)
    new_solution = copy.deepcopy(solution)
    new_solution[a] = course_bits(solution[a]) + dosen_bits(solution[a]) +\
        kelas_bits(solution[a]) + rand_slot + lt_bits(solution[a])
    return [new_solution]


# It randomy selects two classes 
def swn(solution):
    a = random.randint(0, len(solution) - 1)
    b = random.randint(0, len(solution) - 1)
    new_solution = copy.deepcopy(solution)
    temp = slot_bits(solution[a])
    new_solution[a] = course_bits(solution[a]) + dosen_bits(solution[a]) +\
        kelas_bits(solution[a]) + slot_bits(solution[b]) + lt_bits(solution[a])

    new_solution[b] = course_bits(solution[b]) + dosen_bits(solution[b]) +\
        kelas_bits(solution[b]) + temp + lt_bits(solution[b])
    return [new_solution]

def acceptance_probability(old_cost, new_cost, temperature):
    if new_cost < old_cost:
        return 1.0
    else:
        return math.exp((old_cost - new_cost) / temperature)

def simulated_annealing():
    global population 
    alpha = 0.9
    T = 1.0
    T_min = 0.00001
    start_time = time.time()  
    
    convert_input_to_bin()
    population = init_population(1) # as simulated annealing is a single-state method
    old_cost = cost(population[0])
    simulated_annealing_scores = []  # List to store scores of each iteration
    # Simulated annealing iteration
    for __n in range(500):
        new_solution = swn(population[0])
        new_solution = ssn(population[0])
        new_cost = cost(new_solution[0])
        ap = acceptance_probability(old_cost, new_cost, T)
        if ap > random.random():
            population = new_solution
            old_cost = new_cost
        T = T * alpha
        # Calculate and store score of the current iteration
        simulated_annealing_scores.append(evaluate(population[0]))
    end_time = time.time()  
    print("\n----------------------- -----------------------\n")
    for lec in population[0]:
        print_chromosome(lec)
    print("Score: ", evaluate(population[0]))
    print("Time taken for Simulated Annealing: {:.4f} seconds".format(end_time - start_time))
    
population = [] 

def chromosome_to_json(chromosome):
    schedule_data = []
    for chrom in chromosome:
        schedule_data.append({
            "schedule": str(Schedule.schedules[int(slot_bits(chrom), 2)]),
            "room": str(Room.rooms[int(lt_bits(chrom), 2)]),
            "class": str(Kelas.kelas[int(kelas_bits(chrom), 2)]),
            "course": str(CourseClass.classes[int(course_bits(chrom), 2)]),
            "lecturer": str(Dosen.dosen[int(dosen_bits(chrom), 2)])
        })
    return schedule_data

def print_schedule_per_class(best_solution):
    class_schedule = {}
    for chrom in best_solution:
        class_index = int(kelas_bits(chrom), 2)
        class_name = Kelas.kelas[class_index].name
        if class_name not in class_schedule:
            class_schedule[class_name] = []
        class_schedule[class_name].append({
            "schedule": str(Schedule.schedules[int(slot_bits(chrom), 2)]),
            "room": str(Room.rooms[int(lt_bits(chrom), 2)]),
            "course": str(CourseClass.classes[int(course_bits(chrom), 2)]),
            "lecturer": str(Dosen.dosen[int(dosen_bits(chrom), 2)])
        })
    
    # Print schedule per class
    for class_name, schedules in class_schedule.items():
        print(f"Class: {class_name}")
        for schedule in schedules:
            print(f"{schedule['schedule']} | {schedule['room']} | {schedule['course']} | {schedule['lecturer']}")
        print()


def genetic_algorithm():
    start_time = time.time() 
    generation = 0
    convert_input_to_bin()
    population = init_population(3)
    best_solution = None

    print("\n---------------- Genetic Algorithm ------------------\n")
    while True:
        
        # if termination criteria are satisfied, stop.
        if evaluate(max(population, key=evaluate)) == 1 or generation == 500:
            end_time = time.time()  # End time for tracking execution time
            best_solution = max(population, key=evaluate)
            print("Generations:", generation)
            print("Best Chromosome fitness value", evaluate(best_solution))
            print("Best Chromosome: ", best_solution)
            for lec in best_solution:
                print_chromosome(lec)
            print_schedule_per_class(best_solution)
            print("Time taken for Genetic Algorithm: {:.4f} seconds".format(end_time - start_time))
            break
        
        # Otherwise continue
        else:
            for _c in range(len(population)):
                crossover(population)
                selection(population, 5)
                mutate(population[_c])
        generation = generation + 1
        
    # Convert the best solution to JSON
    if best_solution:
        json_data = chromosome_to_json(best_solution)
        # Save JSON data to file
        with open("schedule_data.json", "w") as json_file:
            json.dump(json_data, json_file, indent=4)

def generate_schedule(kelas, dosen, course_classes, rooms, schedules, _cpg):
    print("inside generate schedule")
    Kelas.kelas = kelas

    Dosen.dosen = dosen

    CourseClass.classes = course_classes
    
    Room.rooms = rooms

    Schedule.schedules = schedules
    
    global cpg 
    cpg = _cpg

    random.seed()

    start_time = time.time()
    simulated_annealing()
    genetic_algorithm()

    all_schedules = []

    return