"""Red Badger Martian Robot control tests."""

# pylint: disable=redefined-outer-name

import copy

import pytest
from click.testing import CliRunner

import red_badger_bot


@pytest.fixture
def grid():
    """Grid"""
    return red_badger_bot.Grid(40, 50)


@pytest.fixture
def robot(grid):
    """Robot"""
    return red_badger_bot.Robot(
        grid, x=20, y=40, direction=red_badger_bot.DIRECTIONS.Y_POSITIVE
    )


def test_end_to_end():
    """End-to-end test. Input and output taken straight from problem document."""
    runner = CliRunner()
    result = runner.invoke(
        red_badger_bot.main,
        input=(
            "5 3\n"
            "1 1 E\n"
            "RFRFRFRF\n"
            "\n"
            "3 2 N\n"
            "FRRFLLFFRRFLL\n"
            "\n"
            "0 3 W\n"
            "LLFFFLFLFL\n\0"
        ),
    )

    # Filter out output such as prompts.
    output_lines = []
    for output_line in result.output.split("\n"):
        if ":" not in output_line:
            output_lines.append(output_line)

    output = "\n".join(output_lines)

    assert output == ("1 1 E\n3 3 N LOST\n2 3 S\n")


def test_parse_coordinates():
    """Test parsing coordinates."""
    assert red_badger_bot.parse_coordinates("5 10") == (5, 10)


@pytest.mark.parametrize(
    "string, coords, direction",
    [
        ("0 0 N", (0, 0), red_badger_bot.DIRECTIONS.Y_POSITIVE),
        ("20 0 S", (20, 0), red_badger_bot.DIRECTIONS.Y_NEGATIVE),
        ("0 20 E", (0, 20), red_badger_bot.DIRECTIONS.X_POSITIVE),
        ("20 20 W", (20, 20), red_badger_bot.DIRECTIONS.X_NEGATIVE),
    ],
)
def test_parse_robot(string, coords, direction):
    """Test parsing a robot specification."""
    assert red_badger_bot.parse_robot(string) == (coords, direction)


def test_parse_robot_instructions():
    """Test parsing robot instructions."""
    assert list(red_badger_bot.parse_robot_instructions("RFRFL")) == [
        red_badger_bot.INSTRUCTIONS.RIGHT,
        red_badger_bot.INSTRUCTIONS.FORWARD,
        red_badger_bot.INSTRUCTIONS.RIGHT,
        red_badger_bot.INSTRUCTIONS.FORWARD,
        red_badger_bot.INSTRUCTIONS.LEFT,
    ]


def test_move_robot_forward(robot):
    """Test moving a robot forward."""
    robot.process_instructions([red_badger_bot.INSTRUCTIONS.FORWARD] * 5)
    assert robot.x == 20
    assert robot.y == 45
    assert robot.lost is False


def test_move_robot_off_edge(robot):
    """Test moving a robot off the edge of the grid."""
    robot.process_instructions([red_badger_bot.INSTRUCTIONS.FORWARD] * 20)
    assert robot.x == 20
    assert robot.y == 50
    assert robot.lost is True


def test_rotate_robot_left(robot):
    """Test rotating a robot to the left."""
    assert robot.direction == red_badger_bot.DIRECTIONS.Y_POSITIVE
    robot.process_instructions([red_badger_bot.INSTRUCTIONS.LEFT])
    assert robot.direction == red_badger_bot.DIRECTIONS.X_NEGATIVE
    robot.process_instructions([red_badger_bot.INSTRUCTIONS.LEFT])
    assert robot.direction == red_badger_bot.DIRECTIONS.Y_NEGATIVE
    robot.process_instructions([red_badger_bot.INSTRUCTIONS.LEFT])
    assert robot.direction == red_badger_bot.DIRECTIONS.X_POSITIVE
    robot.process_instructions([red_badger_bot.INSTRUCTIONS.LEFT])
    assert robot.direction == red_badger_bot.DIRECTIONS.Y_POSITIVE


def test_rotate_robot_right(robot):
    """Test rotating a robot to the right."""
    assert robot.direction == red_badger_bot.DIRECTIONS.Y_POSITIVE
    robot.process_instructions([red_badger_bot.INSTRUCTIONS.RIGHT])
    assert robot.direction == red_badger_bot.DIRECTIONS.X_POSITIVE
    robot.process_instructions([red_badger_bot.INSTRUCTIONS.RIGHT])
    assert robot.direction == red_badger_bot.DIRECTIONS.Y_NEGATIVE
    robot.process_instructions([red_badger_bot.INSTRUCTIONS.RIGHT])
    assert robot.direction == red_badger_bot.DIRECTIONS.X_NEGATIVE
    robot.process_instructions([red_badger_bot.INSTRUCTIONS.RIGHT])
    assert robot.direction == red_badger_bot.DIRECTIONS.Y_POSITIVE


@pytest.mark.parametrize(
    "x, y, out_of_bounds",
    [
        (-1, 20, True),
        (20, -1, True),
        (41, 20, True),
        (20, 51, True),
        (0, 20, False),
        (20, 0, False),
        (40, 20, False),
        (20, 50, False),
    ],
)
def test_out_of_bounds(grid, x, y, out_of_bounds):
    """Test grid's out-of-bounds calculation."""
    robot = red_badger_bot.Robot(grid, x, y, red_badger_bot.DIRECTIONS.Y_POSITIVE)
    assert grid.out_of_bounds(robot) == out_of_bounds


def test_cast_robot_to_string(robot):
    """Test casting a robot to a string."""
    assert str(robot) == "20 40 N"
    robot.process_instructions([red_badger_bot.INSTRUCTIONS.FORWARD] * 20)
    assert str(robot) == "20 50 N LOST"


def test_robot_scent(robot):
    """Assert that when a robot is lost, other robots can't get lost at the same place."""
    robot_2 = copy.copy(robot)

    robot.process_instructions([red_badger_bot.INSTRUCTIONS.FORWARD] * 20)
    assert robot.y == 50
    assert robot.lost is True

    robot_2.process_instructions([red_badger_bot.INSTRUCTIONS.FORWARD] * 20)
    assert robot_2.y == 50
    assert robot_2.lost is False
