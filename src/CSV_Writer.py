import csv

path = ''  # If you want to test, set to a relevant place to write CSV files.
C = []
Losses = []
iterations = []


def appendIterations(I):
    global iterations
    iterations.append(I)


def appendC(c):
    global C
    C.append(c)


def appendLosses(L):
    global Losses
    Losses.append(L)


# Creates CSV file with two columns, C and Losses
def CSV_C_Losses():
    header = ['C', 'Losses']
    with open(str(path) + 'CSV_C_Losses_improved.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)

        writer.writerow(header)
        for i in range(len(C)):
            writer.writerow([C[i], Losses[i]])


def CSV_Iterations_Losses():
    header = ['Iterations', 'Losses']
    with open(str(path) + 'CSV_Iterations_Losses.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)

        writer.writerow(header)
        for i in range(len(iterations)):
            writer.writerow([iterations[i], Losses[i]])
