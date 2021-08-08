''' 
A naive implementation of a Dice class for non-transitive dice
with an illustration of the fact that Grimes dice (described https://singingbanana.com/dice/article.htm )
beat each other, but that this reverses when two dice of the same kind are added.
We further see that with three dice of the same kind it becomes possible (or even
likely) that there will be a draw. This pattern repeats, with the probabilities getting closer to 0.5
for more and more dice, with draws only possible with 0 mod 3 dice.
'''

from collections import OrderedDict, defaultdict

class Dice():
    def __init__(self, value_sides_count_dict):
        self.value_sides_count_dict = OrderedDict(sorted(value_sides_count_dict.items()))
        self.__gather_stats__()

    def __gather_stats__(self):
        self.sides_sum = 0
        self.num_sides = 0
        for value, repeats in self.value_sides_count_dict.items():
            self.sides_sum += value * repeats
            self.num_sides += repeats
    
    def mean(self):
        return self.sides_sum / self.num_sides
    
    def __str__(self):
        return self.value_sides_count_dict.__str__()
    
    def __add__(self, other):
        result = defaultdict(int)
        for value, repeats in self.value_sides_count_dict.items():
            for other_value, other_repeats in other.value_sides_count_dict.items():
                result[value + other_value] += repeats * other_repeats
        return Dice(result)
    
    def __mul__(self, integer):
        if not isinstance(integer, int):
            raise ValueError("Can only multiply by an integer")
        elif not integer > 0:
            raise ValueError("Can only multiply by a positive integer")
        elif integer == 1:
            return self
        else:
            ret = self
            for i in range(1, integer):
                ret += self
            return ret
    
    def __rmul__(self, integer):
        return self * integer
    
    def __compare_with_other__(self, other):
        wins, draws, losses = 0, 0, 0
        for value, repeats in self.value_sides_count_dict.items():
            for other_value, other_repeats in other.value_sides_count_dict.items():
                count = repeats * other_repeats
                if value > other_value:
                    wins += count
                elif value == other_value:
                    draws += count
                elif value < other_value:
                    losses += count
                else:
                    raise ValueError("Two values were not gt, lt or eq")
        return wins, draws, losses

    def __gt__(self, other):
        wins, draws, losses = self.__compare_with_other__(other)
        return wins / (wins + draws + losses)
    
    def __ge__(self, other):
        wins, draws, losses = self.__compare_with_other__(other)
        return (wins + draws) / (wins + draws + losses)

    def __eq__(self, other):
        wins, draws, losses = self.__compare_with_other__(other)
        return draws / (wins + draws + losses)
    
    def __le__(self, other):
        wins, draws, losses = self.__compare_with_other__(other)
        return (draws + losses) / (wins + draws + losses)
    
    def __lt__(self, other):
        wins, draws, losses = self.__compare_with_other__(other)
        return losses / (wins + draws + losses)


if __name__ == '__main__':
    red = Dice({3:5, 6:1})
    blue = Dice({2:3, 5:3})
    green = Dice({1:1, 4:5}) # Called Olive in James Grimes' article

    bag = OrderedDict(red=red, blue=blue, green=green)
    for colour, dice in bag.items():
        print(f"The {colour} dice has {dice.num_sides} sides with a mean of {dice.mean()}")
    
    for repeats in range(1, 201):
        for color, nextcolor in zip(['red', 'blue', 'green'], ['blue', 'green', 'red']):
            print(f"{repeats} {color.ljust(5)} dice beats {repeats} {nextcolor.ljust(5)} dice with probability {bag[color] > bag[nextcolor]}, draw: {bag[color] == bag[nextcolor]}")
        bag = OrderedDict(red=bag['red'] + red, blue=bag['blue'] + blue, green=bag['green'] + green)
