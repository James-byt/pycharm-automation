balance = 790


def calculate():
    amount = (balance * 10 / 100) // 5
    return amount


new_amount = calculate()

print(new_amount)