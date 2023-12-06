import re


class Game:
    def __init__(self, line: str):
        self.max_red = 0
        self.max_green = 0
        self.max_blue = 0

        self.min_red = 0
        self.min_green = 0
        self.min_blue = 0

        game, rolls = line.split(":")
        self.id = int(game.split(" ")[1])
        for roll in rolls.split(";"):
            for data in roll.split(","):
                m = re.search(r"(?P<count>\d+) (?P<color>\w+)", data)
                if int(m["count"]) > getattr(self, f"max_{m['color']}"):
                    setattr(self, f"max_{m['color']}", int(m["count"]))
        
    def __repr__(self):
        return (f"Game {self.id}\n"
                f"    Max: {self.max_red} reds, {self.max_green} greens, {self.max_blue} blues\n"
                f"    Min: {self.min_red} reds, {self.min_green} greens, {self.min_blue} blues\n")
    
    def is_viable(self, red: int, green: int, blue: int) -> bool:
        if (
            red >= self.max_red and
            green >= self.max_green and
            blue >= self.max_blue
        ):
            return True
        return False
    
    @property
    def power(self) -> int:
        return self.max_red * self.max_green * self.max_blue


with open("input.txt", "r") as f:
    text = [t.strip() for t in f.readlines()]


def s1(text:str, red: int, green: int, blue: int) -> int:
    valid_games = []
    for line in text:
        game = Game(line)
        if game.is_viable(red, green, blue):
            valid_games.append(game.id)
    
    return sum(valid_games)


def s2(text: str) -> int:
    powers = []
    for line in text:
        powers.append(Game(line).power)
    
    return sum(powers)


print(s1(text, 12, 13, 14))
print(s2(text))
