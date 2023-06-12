import math
import datetime

class GlickoPlayer:
    def __init__(self, name, rating=1500, rd=350, vol=0.06, last_game_date=None):
        self.name = name
        self.rating = rating
        self.rd = rd
        self.vol = vol
        self.last_game_date = last_game_date
        
    def update_rating(self, opponent, result):
        if self.last_game_date is None:
            self.last_game_date = datetime.datetime.now()
        if opponent.last_game_date is None:
            opponent.last_game_date = datetime.datetime.now()
        if self.last_game_date > opponent.last_game_date:
            self.periodic_update()
            
        q = math.log(10) / 400
        g = 1 / math.sqrt(1 + 3 * q ** 2 * opponent.rd ** 2 / math.pi ** 2)
        expected_score = 1 / (1 + 10 ** (-g * (self.rating - opponent.rating) / 400))
        delta = q / (1 / self.rd ** 2 + 1 / (g ** 2 * opponent.rd ** 2))
        variance = 1 / (1 / self.rd ** 2 + 1 / (g ** 2 * opponent.rd ** 2))
        d_squared = (delta ** 2 * expected_score * (1 - expected_score)) / variance
        self.rating += q / (1 / self.rd ** 2 + 1 / (g ** 2 * opponent.rd ** 2)) * g * (result - expected_score)
        self.rd = math.sqrt(1 / (1 / self.rd ** 2 + 1 / (g ** 2 * opponent.rd ** 2)))
        self.vol = self._update_volatility(d_squared)
        self.last_game_date = datetime.datetime.now()
    
    def periodic_update(self):
        c = 60  # Default constant for 6-month period
        time_diff = (datetime.datetime.now() - self.last_game_date).days / 30  # Assuming 30 days per month
        phi = math.sqrt(self.rd ** 2 + self.vol ** 2)
        self.rd = math.sqrt(self.rd ** 2 + self.vol ** 2 * time_diff / c ** 2)
        self.vol = math.sqrt(self.vol ** 2 * (1 - time_diff / c ** 2))
    
    def _update_volatility(self, d_squared):
        a = math.log(self.vol ** 2)
        tau = 0.5  # Time constant for volatility
        x = a / math.sqrt(1 + (3 * d_squared) / math.pi ** 2)
        new_vol_squared = 1 / (1 / x ** 2 + 1 / self.rd ** 2)
        return math.sqrt(new_vol_squared)
    
    # create player dictionary for json
    def to_json_dict(self):
        return {
            'rating': self.rating,
            'rd': self.rd,
            'vol': self.vol,
            'last_game_date': self.last_game_date.strftime("%Y-%m-%d %H:%M:%S") if self.last_game_date else None
        }