def IsHex(s):
    try:
        int(s, 16)
        return True
    except (
        ValueError,
        TypeError,
    ):
        return False
