import random
import math

fingerprint_length = 12
fingerprint_range = (0, 255)
pin_length = 4
euclidean_distance_threshold = 27

def generate_roll_number():
    prefix = "B17"
    num = "".join([str(random.randint(0,9)) for i in range(4)])
    suffix = "CS"
    return prefix + num + suffix

def generate_pin():
    pin = "".join([str(random.randint(0,9)) for i in range(pin_length)])
    return pin

def generate_fingerprint():
    fingerprint = [random.randint(*fingerprint_range) for i in range(fingerprint_length)]
    return fingerprint

def generate_random_user():
    user = {
        "roll_no": generate_roll_number(),
        "pin": generate_pin(),
        "fingerprint": generate_fingerprint()
    }
    return user

def generate_fingerprint_noise(vector_length, exceed_threshold = False):
    if (exceed_threshold == False):
        pieces = []
        alterations = 3
        for i in range(vector_length):
            if (alterations > 0) and random.randint(0, 9) < 7:
                alter_max = int(math.sqrt(euclidean_distance_threshold / alterations))
                diff = random.randint(1, alter_max - 1)
                # diff = -diff if random.randint(0, 9) < 5 else diff # Changing sign of difference
                pieces.append(diff)
                alterations = alterations - 1
            else:
                pieces.append(0)
        return pieces
    else:
        pieces = [0 for i in range(vector_length)]
        while True:
            index = random.randint(0, vector_length-1)
            diff = random.randint(0, euclidean_distance_threshold)
            # diff = -diff if random.randint(0, 9) < 5 else diff
            pieces[index] = diff
            if sum([x*x for x in pieces]) >= euclidean_distance_threshold:
                break
        return pieces

def alter_fingerprint(fingerprint, exceed_threshold = False):
    noise = generate_fingerprint_noise(len(fingerprint), exceed_threshold)
    altered = [(fingerprint[i] + noise[i]) for i in range(len(fingerprint))]
    for i in range(len(altered)):
        if altered[i] < fingerprint_range[0]:
            altered[i] = fingerprint_range[0]
        if altered[i] >= fingerprint_range[1]:
            altered[i] = fingerprint_range[1]
    return altered
