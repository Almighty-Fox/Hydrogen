def function_for_lovushek(CL, VL, VT1, K1, ci):
    return (1 + VL / VT1 / (K1 + VL * CL * (1 - K1))) * CL - ci
    # return CL - ci
