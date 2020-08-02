import csv


def csv_2_array(music_csv):
    """
    Crea un arreglo para filtrar el número de notas y sus tiempos
    Info en el csv:
        0. track number
        1. channel number
        2. note number (midi encoding of pitch)
        3. velocity
        4. start time (seconds)
        5. end time (seconds)
        6. message number of note_on
        7. message number of note_of
    Librería utilizada: csv
    """
    music_array = []  # Arreglo
    with open(music_csv, newline='') as f:  # Función para leer el csv
        reader = csv.reader(f)
        for row in reader:
            music_array.append([int(row[2]), round(float(row[4]), 2), round(float(row[5]), 2)])
    return music_array


def music_length(music_array):
    # Establecer la duracion del programa en segundos
    duration = round(music_array[-1][2])
    # Redondear el resultado al siguiente entero
    # 43.3 -> 44
    if (music_array[-1][2] - duration) > 0:
        duration += 1
    return duration


def array_2_keys(music_array, duration):
    """
    Crea de cada tecla precionada cada mili segundo
    1 significa presionado
    0 significa no presionado
    """
    keys_array = [[0] * 128 for k in range(duration * 100)]
    for i in range(0, len(keys_array)):
        for j in range(0, len(music_array)):
            if (int(music_array[j][1] * 100 + 1) <= i) and (int(music_array[j][2] * 100 - 1) >= i):
                keys_array[i][music_array[j][0]] += 1
    return keys_array


def black_filter(keys_array):
    # Filtra las teclas negras
    base = [1, 3, 6, 8, 10]
    black_keys = [0] * 45
    for a in range(0, 9):
        black_keys[0 + 5 * a] = base[0] + 12 * a
        black_keys[1 + 5 * a] = base[1] + 12 * a
        black_keys[2 + 5 * a] = base[2] + 12 * a
        black_keys[3 + 5 * a] = base[3] + 12 * a
        black_keys[4 + 5 * a] = base[4] + 12 * a
    keys_array_filtered = []
    keys_filtered = []
    for row in range(0, len(keys_array)):
        for column in range(0, len(keys_array[0])):
            if column not in black_keys:
                keys_filtered.append(keys_array[row][column])
        keys_array_filtered.append(keys_filtered)
        keys_filtered = []
    return keys_array_filtered


def octaves(keys_array):
    octaves_array = []
    for keys in keys_array:
        octaves_array.append(keys[12:120])
    return octaves_array


def hand_position_array(keys_array):
    position = 0
    follower = 0
    hand_move_array = []
    for keys in keys_array:
        for j in range(0, len(keys)):
            if keys[j] == 1:
                follower = j-28
                break
        if follower != 0:
            if follower > position + 4:
                position = follower - 4
            elif follower < position:
                position = follower
        servos = keys[position+28:position+28+5]
        hand_move_array.append([position, servos])
        follower = 0
    return hand_move_array


def format_array(hand_array):
    b = []
    time = []
    cont = 0
    ant = hand_array[0]
    b.append(ant)
    for i in range(0, len(hand_array)):
        if hand_array[i] != ant:
            time.append(cont/100)
            b.append(hand_array[i])
            cont = 0
        cont += 1
        ant = hand_array[i]
    time.append(cont/100)

    keys_format_array = []
    for i in range(0, len(b)):
        keys_format_array.append([b[i][0], b[i][1], time[i]])

    return keys_format_array


csv_midi = 'Silent Night.csv'
array_midi = csv_2_array(csv_midi)
playing_time = music_length(array_midi)
array_keys = array_2_keys(array_midi, playing_time)
array_octaves = octaves(array_keys)
array_octaves_filtered = black_filter(array_octaves)
hand_move = hand_position_array(array_octaves_filtered)
array_format = format_array(hand_move)

for i in array_format:
    print(i)
