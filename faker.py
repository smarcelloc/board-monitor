from urandom import getrandbits  # use 'random' no Python normal


class Faker:

    @staticmethod
    def temperature(min: float = 20.0, max: float = 40.0, places: int = 4) -> float:
        return Faker._random_range(places, min, max)

    @staticmethod
    def humidity(min: float = 30.0, max: float = 90.0, places: int = 4) -> float:
        return Faker._random_range(places, min, max)

    @staticmethod
    def pressure(min: float = 990.0, max: float = 1035.0, places: int = 4) -> float:
        return Faker._random_range(places, min, max)

    @staticmethod
    def _random_range(places: int, min: float, max: float) -> float:
        scale = 10**places
        min_int = int(min * scale)
        max_int = int(max * scale)
        rand_int = min_int + getrandbits(16) % (max_int - min_int + 1)
        return round(rand_int / scale, places)
