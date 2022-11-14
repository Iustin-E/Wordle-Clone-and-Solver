import random

autosolve = False
#       Deschiderea si creerea listei
file = open('cuvinte', 'r')
cuvinte_data = file.read().replace('\n', ' ').split(' ')
file.close()

file = open('cuvinte', 'r')
cuvinte_ramase = file.read().replace('\n', ' ').split(' ')
file.close()


#       Alegerea unui cuvant random
cuvant_corect = random.choice(cuvinte_data)
#cuvant_corect = 'LENTE'
#print(cuvant_corect)

def solve(last_guess, last_feedback):
    global cuvinte_ramase
    for i in range(5):
        j = 0
        n = len(cuvinte_ramase) - 1
        while j < n:
            if last_feedback[i] == 'G':
                if cuvinte_ramase[j][i] != last_guess[i]:
                    cuvinte_ramase.remove(cuvinte_ramase[j])
                    j -= 1

            elif last_feedback[i] == 'Y':
                if last_guess[i] not in cuvinte_ramase[j]:
                    cuvinte_ramase.remove(cuvinte_ramase[j])

            elif last_feedback[i] == '_':
                if last_guess[i] == cuvinte_ramase[j][i]:
                    cuvinte_ramase.remove(cuvinte_ramase[j])

            j += 1
            n = len(cuvinte_ramase)
        print(len(cuvinte_ramase), cuvinte_ramase)

def incorect(guess):
    #       Dictionar cu aparitia fiecarei litere - pentru litere care apar de mai multe ori
    d = {x : 0 for x in cuvant_corect}
    for el in cuvant_corect:
        d[el] += 1
    l = ['_', '_', '_', '_', '_']

    for i in range(len(guess)):
        if guess[i] == cuvant_corect[i]:
            l[i] = "G"
            d[guess[i]] -= 1
    for i in range(len(guess)):
        if (l[i] == '_') and (guess[i] in cuvant_corect) and d[guess[i]]>0:
            l[i] = "Y"
            d[guess[i]] -= 1
    return ''.join(l)


# Returneaza -1 daca e invalid, 0 daca e corect, string cu rezultatul daca e incorect
def verifica(guess):
    if (len(guess) != 5) or (guess not in cuvinte_data):
        return -1
    elif guess == cuvant_corect:
        return 0
    else:
        return incorect(guess)


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
    else:
        guess_feedback = verifica(guess)

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

