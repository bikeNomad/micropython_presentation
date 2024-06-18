
def dump(lc):
    for ra in range(0x1F):
        val = lc.getRegister(ra)
        print(f"{ra:02x} {val:02x} {val:03d}")