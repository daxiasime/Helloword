people=list(range(1,42))
while len(people)>2:
    i=1
    while i<3:
        people.append(people.pop(0))
        i+=1
    print('{:2d}自杀了'.format(people.pop(0)))
print(f'\n安全的位置是{people[0],people[1]}')

# WISOFJFJFVMSGIHH
