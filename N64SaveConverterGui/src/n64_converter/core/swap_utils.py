# swap_utils.py

def byteswap(data: bytes, swap_size: int) -> bytes:
    """Swap the byte order of data in chunks of the given size."""
    if swap_size <= 1:
        return data

    swapped = bytearray(len(data))
    for i in range(0, len(data), swap_size):
        chunk = data[i:i + swap_size]
        swapped[i:i + len(chunk)] = chunk[::-1]
    return bytes(swapped)
