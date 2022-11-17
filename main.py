import random
from collections import Counter
from multiprocessing import Process

autosolve = True
#       Deschiderea si creerea listei
file = open('cuvinte', 'r')
cuvinte_data = file.read().replace('\n', ' ').split(' ')
file.close()

cuvinte_data2 = list(cuvinte_data)
cuvinte_toate = list(cuvinte_data)


#       Alegerea unui cuvant random
cuvant_corect = random.choice(cuvinte_data)
#cuvant_corect = 'GALON'
#print(cuvant_corect)


def solve(last_guess, last_feedback):
    locked = [0, 0, 0, 0, 0]  # vector pentru pozitiile care au sigur o litera
    for i in range(5):
        #TODO - daca sunt 2-3 caractere la fel in guess si la unul e _,
        # atunci stergem toate cuv cu caracterul in ele care nu e la pozitia unde a dat G
        global cuvinte_data2
        for cuvant in cuvinte_data2:
            if last_feedback[i] == 'G':
                if cuvant[i] != last_guess[i]:
                    cuvinte_data.remove(cuvant)

            elif last_feedback[i] == 'Y':
                if (last_guess[i] not in cuvant) or (last_guess[i] == cuvant[i]):
                    cuvinte_data.remove(cuvant)

            elif last_feedback[i] == '_':
                if last_guess[i] == cuvant[i]:
                    cuvinte_data.remove(cuvant)
                if last_guess[i] in locked:  # inseamna ca litera e a n-a litera este deja de nr maxim de ori
                    cuvinte_data.remove(cuvant)
            cuvinte_data2 = list(cuvinte_data)
    #print(len(cuvinte_data2), cuvinte_data2)
    return cuvinte_data2


def incorect(guess_m, cuvant_corect_m):
    #       Dictionar cu aparitia fiecarei litere - pentru litere care apar de mai multe ori
    d_cuvant = Counter(cuvant_corect_m)
    l = ['_', '_', '_', '_', '_']

    for i in range(len(guess_m)):
        if guess_m[i] == cuvant_corect_m[i]:
            l[i] = "G"
            d_cuvant[guess_m[i]] -= 1
    for i in range(len(guess_m)):
        if (l[i] == '_') and (guess_m[i] in cuvant_corect) and d_cuvant[guess_m[i]]>0:
            l[i] = "Y"
            d_cuvant[guess[i]] -= 1
    return ''.join(l)


# Returneaza -1 daca e invalid, 0 daca e corect, string cu rezultatul daca e incorect
def verifica(guess_m, cuvant_corect_m):
    if (len(guess_m) != 5) or (guess_m not in cuvinte_toate):
        return -1
    elif guess_m == cuvant_corect_m:
        return 0
    else:
        return incorect(guess_m, cuvant_corect_m)


def test_for_all():
    global guess, cuvinte_data
    lista_mare = []
    nr_guesses = []
    for cuvant_corect_t in cuvinte_toate:
        global cuvinte_data2
        cuvinte_data2 = list(cuvinte_toate)
        cuvinte_ramase_t = list(cuvinte_toate)
        cuvinte_data = list(cuvinte_toate)
        guess = 'AVION'
        lista_mica = []
        guess_feedback_t = 1
        while guess_feedback_t:  # guess_feedback_t e 0 cand cuvantul e corect
            guess_feedback_t = verifica(guess, cuvant_corect_t)
            if guess_feedback_t == 0:
                lista_mica.append(guess)
                nr_guesses.append(len(lista_mica))
                print(f"Rezolvat: {cuvant_corect_t} in {len(lista_mica)} guesses: {lista_mica}")
                break
            cuvinte_ramase_t = solve(guess, guess_feedback_t)
            lista_mica.append(guess)
            guess = cuvinte_ramase_t[0]
        lista_mare.append(lista_mica)
        #print(lista_mica)
    print(nr_guesses, len(nr_guesses), nr_guesses/len(nr_guesses))

#       Input
guesses = []
feedbacks = []
ok = True
while ok:
    guess = input("Guess: ").upper()
    if guess == "*":
        if not autosolve:
            print('Auto-Solve turned on!')
            autosolve = True
        else:
            print('Auto-Solve turned off!')
            autosolve = False
    elif guess == "TEST":
        test_for_all()
    else:
        guess_feedback = verifica(guess, cuvant_corect)

        if guess_feedback == -1:
            print("Invalid")
        elif guess_feedback == 0:
            print("Corect")
            guesses.append(guess)
            feedbacks.append('GGGGG')
            ok = False
        else:
            print(guess_feedback)
            guesses.append(guess)
            feedbacks.append(guess_feedback)
            if autosolve:
                solve(guesses[len(guesses) - 1], feedbacks[len(feedbacks) - 1])

print(guesses, f' - {len(guesses)} guesses')

