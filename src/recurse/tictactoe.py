from enum import StrEnum
from typing import Iterator, Optional, Self


class InvalidMoveError(Exception):
    pass


class Mark(StrEnum):
    E = "E"
    X = "X"
    O = "O"  # noqa: E741


class Space(StrEnum):
    TopLeft = "top-left"
    TopCenter = "top-center"
    TopRight = "top-right"
    MiddleLeft = "middle-left"
    MiddleCenter = "middle-center"
    MiddleRight = "middle-right"
    BottomLeft = "bottom-left"
    BottomCenter = "bottom-center"
    BottomRight = "bottom-right"

    @classmethod
    def from_int(cls, value: int) -> Self:
        # Dial pad layout (1 indexed)
        value_map = {i + 1: space for i, space in enumerate(Space)}
        return value_map[value]

    def to_int(self) -> int:
        # Dial pad layout (1 indexed)
        value_map = {space: i + 1 for i, space in enumerate(Space)}
        return value_map[self]


class Player(StrEnum):
    X = "X"
    O = "O"  # noqa: E741

    def get_mark(self) -> Mark:
        match self:
            case self.X:
                return Mark.X
            case self.O:
                return Mark.O


class Board:
    cells: dict[Space, Mark]

    def __init__(self) -> None:
        self.cells = {space: Mark.E for space in Space}  # noqa: C420

    def get(self, space: Space) -> Mark:
        return self.cells[space]

    def set(self, space: Space, mark: Mark) -> None:
        self.cells[space] = mark

    def __repr__(self) -> str:
        ret = ""
        ret += "-" * 13 + "\n"
        for space_value in range(1, 10):
            space = Space.from_int(space_value)
            mark = self.get(space)
            mark = mark if mark in (Mark.X, Mark.O) else str(space_value)
            ret += f"| {mark} "

            if space_value % 3 == 0:
                ret += "|\n"
                ret += "-" * 13 + "\n"

        return ret


class Checker:
    @classmethod
    def iter_triples(cls, board: Board) -> Iterator[list[Mark]]:
        triples_ints = [
            # Rows
            (1, 2, 3),
            (4, 5, 6),
            (7, 8, 9),
            # Columns
            (1, 4, 7),
            (2, 5, 8),
            (3, 6, 9),
            # Diagonals
            (1, 5, 9),
            (3, 5, 7),
        ]
        for triple_ints in triples_ints:
            yield [board.get(Space.from_int(i)) for i in triple_ints]

    @classmethod
    def get_winner(cls, board: Board) -> Optional[Player]:
        for triple in cls.iter_triples(board):
            if all(mark == Mark.X for mark in triple):
                return Player.X
            if all(mark == Mark.O for mark in triple):
                return Player.O
        return None


class Game:
    board: Board
    current_player: Player

    def __init__(self) -> None:
        self.board = Board()
        self.current_player = Player.X

    def switch_current_player(self) -> None:
        match self.current_player:
            case Player.O:
                self.current_player = Player.X
            case Player.X:
                self.current_player = Player.O

    def make_move(self, space: Space) -> None:
        if self.board.get(space) != Mark.E:
            msg = f"board space {space} not empty"
            raise InvalidMoveError(msg)
        mark = self.current_player.get_mark()
        self.board.set(space, mark)
        self.switch_current_player()

    def play(self) -> None:
        game_over = False
        while not game_over:
            valid_input = False
            while not valid_input:
                print(self.board)
                print(f"move for {self.current_player}")
                player_input = input().strip()
                try:
                    space_int = int(player_input)
                except ValueError:
                    print("invalid space number, must be an integer from 1-9")
                    continue

                try:
                    space = Space.from_int(space_int)
                except KeyError:
                    print("invalid space number, must be 1-9")
                    continue

                try:
                    self.make_move(space)
                    valid_input = True

                    if winner := Checker.get_winner(self.board):
                        print(self.board)
                        print(f"winner is {winner}")
                        game_over = True
                        continue
                except InvalidMoveError:
                    print(f"invalid move, space {space.to_int()} already taken")
                    continue


if __name__ == "__main__":
    game = Game()
    game.play()
