def get_num(num) -> int | float:
    num = float(num)
    return int(num) if num == int(num) else float(num)