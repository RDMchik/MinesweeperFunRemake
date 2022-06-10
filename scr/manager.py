import random


def build_block_info(is_bomb: bool, coordinates: tuple) -> dict:
    return {
        'x': coordinates[0],
        'y': coordinates[1],
        'is_bomb': is_bomb,
        'marked': False,
        'num': 0
    }


class Manager(object):
    """a class which is responsible for
    some of the main game logistics"""

    def __init__(self, conf: dict) -> None:
        self.conf = conf
        self._field = self._generate_new_field(
            (conf['field_size_x'], conf['field_size_y']),
            conf['block_size'], conf['bombs_amount']
        )

    def _generate_new_field(self, size: tuple, block_size: int, bombs: int) -> dict:
        """generate new game field"""
        bomb_locations = []
        for _ in range(bombs):
            while True:
                location = random.randint(1, self.conf['field_size_x'] * self.conf['field_size_y'] - 1)
                if location in bomb_locations:
                    continue
                bomb_locations.append(location)
                break
        field = {}
        total = 0
        for x in range(size[0]):
            x *= block_size
            for y in range(size[1]):
                total += 1
                y *= block_size
                # checking for an existence of x in a field
                # code would give an error if we just say
                # field[str(x)][str(y)] because field[str(x)]
                # might not be existing
                x_coordinate_exists = field.get(str(x))
                if not x_coordinate_exists:
                    field[str(x)] = {}
                field[str(x)][str(y)] = build_block_info(
                    True if total in bomb_locations else False,
                    (x, y)
                )
        
        # completing the field
        for x_key, x_value in field.items():
            for y_key, y_value in x_value.items():
                if y_value['is_bomb']:
                    # adding 1 to 8 blocks around bomb.
                    # all this exceptions are needed 
                    # because there is a chance of getting
                    # a key error when trying to access
                    # a block which does not actually exist
                    for x in range(-1, 2):
                        for y in range(-1, 2):
                            if x == y == 0: continue
                            try:
                                field[str(int(x_key) + x*block_size)][str(int(y_key) + y*block_size)]['num'] += 1
                            except KeyError:
                                pass
        return field

    def get_field(self) -> dict:
        return self._field

    def set_key(self, coordinates: tuple, key: str, value) -> None:
        self._field[str(coordinates[0])][str(coordinates[1])][str(key)] = value

    def game_finished(self) -> bool:
        """checking if game ended"""
        for _, x_value in self._field.items():
            for _, y_value in x_value.items():
                if y_value['is_bomb']:
                    if not y_value['marked']:
                        return False
        return True


