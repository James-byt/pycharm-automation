
trade = 0
session = [2, 3, 4]
lead = []
while trade < 3:
    for i in session:
        lead.append(i)
        trade =+ 1
        print(trade)

print(lead)
print(trade)