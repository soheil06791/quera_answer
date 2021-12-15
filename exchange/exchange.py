with open('input.txt') as f:
    lines = f.readlines()
lines = [line.replace('\n','') for line in lines]

money_mohammad = int(lines[0])
exchange_coin = {'ADE':{int(lines[1].split(' ')[0]): int(lines[2].split(' ')[0])}, 'EUR':{int(lines[1].split(' ')[1]):int(lines[2].split(' ')[1])}, 'DOL':{int(lines[1].split(' ')[2]): int(lines[2].split(' ')[2])}}

mode = 0
remain = money_mohammad
for ex,coin in exchange_coin.items():
    exch =[]
    for key,val in coin.items():
        for i in range(key+1):
            exch.append(val*i)

    exchange_coin[ex] = exch
for i in exchange_coin['ADE']:
    for j in exchange_coin['EUR']:
        for k in exchange_coin['DOL']:
            if i+k+j == money_mohammad:
                mode += 1
print(mode)



