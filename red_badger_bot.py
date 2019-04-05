"""Red Badger Martian Robots coding challenge."""

import re
from enum import Enum

import click


class DIRECTIONS(Enum):
    """Direction enumeration."""

    Y_POSITIVE = "N"
    Y_NEGATIVE = "S"
    X_POSITIVE = "E"
    X_NEGATIVE = "W"


class INSTRUCTIONS(Enum):
    """Instruction enumeration."""

    FORWARD = "F"
    RIGHT = "R"
    LEFT = "L"


class Grid:
    """Grid"""

    def __init__(self, x, y):
        """Constructor"""
        self.x = x
        self.y = y
        self.scents = []

    def out_of_bounds(self, robot):
        """Determine if a robot is out-of-bounds."""
        if 0 <= robot.x <= self.x and 0 <= robot.y <= self.y:
            return False

        return True


class Robot:
    """Robot"""

    def __init__(self, grid, x, y, direction):
        """Constructor"""
        self.grid = grid
        self.x = x
        self.y = y
        self.direction = direction
        self.lost = grid.out_of_bounds(self)

    def process_instructions(self, instructions):
        """Process a list of instructions."""
        for instruction in instructions:
            self.process_instruction(instruction)

    def process_instruction(self, instruction):
        """Process a single instruction."""
        if instruction == INSTRUCTIONS.FORWARD:
            return self.move_forward()

        if instruction == INSTRUCTIONS.RIGHT:
            return self.rotate_right()

        if instruction == INSTRUCTIONS.LEFT:
            return self.rotate_left()

        raise ValueError(f'Unrecognised instruction "{instruction}"')

    def move_forward(self):
        """Move forward."""
        if self.lost:
            return

        initial_x = self.x
        initial_y = self.y

        if self.direction == DIRECTIONS.X_POSITIVE:
            self.x += 1
        if self.direction == DIRECTIONS.X_NEGATIVE:
            self.x -= 1
        if self.direction == DIRECTIONS.Y_POSITIVE:
            self.y += 1
        if self.direction == DIRECTIONS.Y_NEGATIVE:
            self.y -= 1

        if self.grid.out_of_bounds(self):
            self.x = initial_x
            self.y = initial_y

            # If another robot left a scent at this point, this robot is not lost.
            self.lost = (self.x, self.y) not in self.grid.scents

            # Leave a scent in the grid.
            self.grid.scents.append((self.x, self.y))

    def rotate_left(self):
        """Rotate left."""
        if self.direction == DIRECTIONS.Y_POSITIVE:
            self.direction = DIRECTIONS.X_NEGATIVE
        elif self.direction == DIRECTIONS.X_NEGATIVE:
            self.direction = DIRECTIONS.Y_NEGATIVE
        elif self.direction == DIRECTIONS.Y_NEGATIVE:
            self.direction = DIRECTIONS.X_POSITIVE
        elif self.direction == DIRECTIONS.X_POSITIVE:
            self.direction = DIRECTIONS.Y_POSITIVE

    def rotate_right(self):
        """Rotate right."""
        if self.direction == DIRECTIONS.Y_POSITIVE:
            self.direction = DIRECTIONS.X_POSITIVE
        elif self.direction == DIRECTIONS.X_POSITIVE:
            self.direction = DIRECTIONS.Y_NEGATIVE
        elif self.direction == DIRECTIONS.Y_NEGATIVE:
            self.direction = DIRECTIONS.X_NEGATIVE
        elif self.direction == DIRECTIONS.X_NEGATIVE:
            self.direction = DIRECTIONS.Y_POSITIVE

    def __str__(self):
        """String representation of this robot."""
        desc = f"{self.x} {self.y} {self.direction.value}"
        if self.lost:
            desc += " LOST"

        return desc


def parse_coordinates(coordinates):
    """Parse coordinates."""
    match = re.search(r"^(\d+)\s+(\d+)$", coordinates)
    return (int(match.group(1)), int(match.group(2)))


def parse_robot_instructions(instructions):
    """Parse a list of robot instructions."""
    for instruction in instructions:
        yield INSTRUCTIONS(instruction)


def parse_robot(robot_spec):
    """Parse a robot spec into starting coordinates and direction."""
    direction_values = "".join([d.value for d in DIRECTIONS])
    match = re.search(rf"^(\d+)\s+(\d+)\s+([{direction_values}])$", robot_spec)
    return ((int(match.group(1)), int(match.group(2))), DIRECTIONS(match.group(3)))


@click.command()
def main():
    """Red Badger Martian Robots coding challenge."""
    grid_size = click.prompt("Mars size", value_proc=parse_coordinates)
    grid = Grid(*grid_size)

    robot_count = 0
    while True:
        coords, direction = click.prompt(
            f"Starting coordinates and direction for robot #{robot_count + 1}",
            value_proc=parse_robot,
        )
        instructions = click.prompt(
            f"Instructions for robot #{robot_count + 1}",
            value_proc=parse_robot_instructions,
        )

        robot = Robot(grid, *coords, direction)
        robot.process_instructions(instructions)
        click.echo(robot)
        robot_count = robot_count + 1


if __name__ == "__main__":
    main()
