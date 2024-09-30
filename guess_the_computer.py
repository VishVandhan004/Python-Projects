import random
def guess(x):
    random_n = random.randint(1,x)
    guess=0
    while guess !=random_n:
        guess = int(input(f'guess a number b/w 1 and {x}: '))
        if guess < random_n:
            print(' too low nigga')
        elif guess > random_n:
            print('too high nigga')
    print(f'nice guess {random_n}.')

# guess_number (USER)
def computer_guess(x):
    low = 1
    high = x
    feedback = ''
    while feedback != 'c':
        if low!=high:
            guess = random.randint(low,high)
        else:
            guess = low
        feedback = input(f'is {guess} too high , too low, or correct').lower()
        if feedback == 'h':
            high = guess - 1   #too high
        elif feedback == 'l':
            low = guess + 1  # too low
    print(f'computer guessed correctly {guess}')
# guess(10)
computer_guess(10)