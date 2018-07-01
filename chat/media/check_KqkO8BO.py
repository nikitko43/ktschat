from random import randint

n = 100
print("Кол-во вопросов:")
n = int(input())

questions = 4
questions = int(input("В билете"))

t = 1
print("Тактика: 1 - первые 50%, 2 - первые 50% из каждой четверти")
t = int(input())

sucess = 0
times = 10000

asked_questions = {i: 0 for i in range(questions+1)}

if t == 1:
    for i in range(times):
        r = [randint(i * n//4, (i+1)* n//4) for i in range(questions)]
        asked = 0
        for num in r:
            if num <= n//2:
                asked += 1
        asked_questions[asked] += 1
    for num in asked_questions:
        asked_questions[num] /= times
    print(asked_questions)

if t == 2:
    for i in range(times):
        r = [randint(i * n//4, (i+1)* n//4) for i in range(questions)]
        asked = 0
        for num in r:

            if num % n//4 <= n//8:
                asked += 1
        asked_questions[asked] += 1
    for num in asked_questions:
        asked_questions[num] /= times

    print(asked_questions)

