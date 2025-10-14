# swap_utils.py
def byteswap(data, swap_size):
    if swap_size <= 1:
        return data
    swapped = bytearray(len(data))
    for i in range(0, len(data), swap_size):
        chunk = data[i:i + swap_size]
        swapped[i:i + len(chunk)] = chunk[::-1]
    return bytes(swapped)

def determine_swap_size(swap_required=False, user_choice="Default"):
    if user_choice == "2 bytes":
        return 2
    elif user_choice == "4 bytes":
        return 4
    else:
        return 2 if swap_required else 1