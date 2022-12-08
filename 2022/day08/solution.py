from dataclasses import dataclass


# with open("test.txt") as f:
with open("input.txt") as f:
    text = [t.strip() for t in f.readlines()]


@dataclass
class TreeAddress:
    x: int
    y: int


class Grove:
    def __init__(self, trees):
        self.trees = trees
        self.max_x = len(trees[0]) - 1
        self.max_y = len(trees) - 1
        self.addr = TreeAddress(0, 0)

    def next_tree(self):
        """ Move to the next tree """
        if (
            self.addr.x == self.max_x and
            self.addr.y == self.max_y
        ):
            return False

        if self.addr.x == self.max_x:
            self.addr.x = 0
            self.addr.y += 1
        else:
            self.addr.x += 1
        return True

    def get_height(self, x, y):
        return self.trees[y][x]

    @property
    def current_tree_height(self):
        return self.get_height(self.addr.x, self.addr.y)

    def _visible_from_north(self):
        if self.addr.y == 0:
            return True

        for y in range(self.addr.y-1, -1, -1):
            # print(f"current: {self.current_tree_height} compare: {self.get_height(self.addr.x, y)}")
            if self.current_tree_height <= self.get_height(self.addr.x, y):
                return False
        return True

    def _visible_from_south(self):
        if self.addr.y == self.max_y:
            return True

        for y in range(self.addr.y+1, self.max_y+1):
            if self.current_tree_height <= self.get_height(self.addr.x, y):
                return False
        return True

    def _visible_from_west(self):
        if self.addr.x == 0:
            return True

        for x in range(self.addr.x-1, -1, -1):
            if self.current_tree_height <= self.get_height(x, self.addr.y):
                return False
        return True

    def _visible_from_east(self):
        if self.addr.x == self.max_x:
            return True

        for x in range(self.addr.x+1, self.max_x+1):
            if self.current_tree_height <= self.get_height(x, self.addr.y):
                return False
        return True

    def tree_is_visible(self):
        return (
            self._visible_from_north() or
            self._visible_from_south() or
            self._visible_from_west() or
            self._visible_from_east()
        )

    def _view_distance_north(self):
        if self.addr.y == 0:
            return 0

        distance = 0
        for y in range(self.addr.y-1, -1, -1):
            distance += 1
            if self.current_tree_height <= self.get_height(self.addr.x, y):
                break
        return distance

    def _view_distance_south(self):
        if self.addr.y == self.max_y:
            return 0

        distance = 0
        for y in range(self.addr.y+1, self.max_y+1):
            distance += 1
            if self.current_tree_height <= self.get_height(self.addr.x, y):
                break
        return distance

    def _view_distance_west(self):
        if self.addr.x == 0:
            return 0

        distance = 0
        for x in range(self.addr.x-1, -1, -1):
            distance += 1
            if self.current_tree_height <= self.get_height(x, self.addr.y):
                break
        return distance

    def _view_distance_east(self):
        if self.addr.x == self.max_x:
            return 0

        distance = 0
        for x in range(self.addr.x+1, self.max_x+1):
            distance += 1
            if self.current_tree_height <= self.get_height(x, self.addr.y):
                break
        return distance

    def scenic_score(self):
        return (
            self._view_distance_north() *
            self._view_distance_south() *
            self._view_distance_west() *
            self._view_distance_east()
        )


trees = []
for line in text:
    trees.append(list(line))


# Part 1

grove = Grove(trees)

visible_trees = 1  # First tree is obviously visible
while grove.next_tree():
    if grove.tree_is_visible():
        visible_trees += 1

answer_1 = visible_trees
print(f"There are {answer_1} visible trees")


# Part 2

grove = Grove(trees)

scenic_scores = [grove.scenic_score()]  # (0, 0)
while grove.next_tree():
    scenic_scores.append(grove.scenic_score())

answer_2 = max(scenic_scores)
print(f"The maximum scenic score is {answer_2}")
