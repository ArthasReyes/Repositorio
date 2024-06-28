from neoeduca import Movil, ADS1115

ads = ADS1115(sda_pin=14, scl_pin=15)


while True:
    A0 = ads.read(0, 0)
    A1 = ads.read(0, 1)
    A2 = ads.read(0, 2)
    A3 = ads.read(0, 3)
    print(A0, A1, A2, A3)
    