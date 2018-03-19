import os
import csv
import numpy as np

INPUT_DIR = "K:/Projects/Gardner Russo Gardner Offices.2018103/SLM data"
OUTPUT_THIRD = "K:/Projects/Gardner Russo Gardner Offices.2018103/SLM data/third_octave.csv"
OUTPUT_OCTAVE = "K:/Projects/Gardner Russo Gardner Offices.2018103/SLM data/octave.csv"

line_info = [
    (172, "Leq_third", 11 ), 
    (188, "Max_third", 19 ),
    (173, "Min_third", 17),
]

def preprocess(line):
    return line.replace("\n", "").replace('Hz', '').replace("/ ", ".").replace(" ", "").split(",")

def get_line_number(line):
    try:
        return float (preprocess(line) [0][1:])
    except ValueError:
        return None

def octave_band(third_octave_values):
    def dB_add(a):
        return 10 * np.log10(10 ** (float(third_octave_values[a + 0]) / 10) + \
                             10 ** (float(third_octave_values[a + 1]) / 10) + \
                             10 ** (float(third_octave_values[a + 2]) / 10))
    assert len(third_octave_values) % 3 == 0
    return [dB_add(n) for n in range(0, len(third_octave_values), 3)]


filename = os.listdir(INPUT_DIR)[0]
with open(os.path.join(INPUT_DIR, filename), encoding="latin-1") as f:
    for line in f:
        print(line)
        if get_line_number(line) == 174:
            third_octave_band = ['','', "dBA"] + preprocess(line)[1:]
            break
        
with open(OUTPUT_THIRD, "w", newline="") as third_csv,\
        open(OUTPUT_OCTAVE, "w", newline="") as octave_csv:
    third_writer = csv.writer(third_csv)
    octave_writer = csv.writer(octave_csv)

    octave_header = third_octave_band[:3] 
    octave_header += [third_octave_band[i] for i in range(4, len(third_octave_band), 3)]

    for third_octave_line, category, dBA_line in line_info:
        third_writer.writerow(third_octave_band)
        octave_writer.writerow(octave_header)
        
        for file_name in os.listdir(INPUT_DIR):
            with open(os.path.join (INPUT_DIR,file_name), encoding="latin-1") as slmdl:
   
                for line in slmdl:
                    line_number = get_line_number(line)

                    if line_number == third_octave_line:
                        third_octave_values = preprocess(line)[1:]
                    if line_number == dBA_line:
                        dBA = preprocess(line.replace('Hz', ''))[1]        
                
                third_octave_row = [file_name, category, dBA] + third_octave_values
                third_writer.writerow(third_octave_row)
                octave_row = [file_name, category, dBA] + octave_band(third_octave_values)

                octave_writer.writerow(octave_row)
