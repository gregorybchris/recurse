from enum import StrEnum, auto
from typing import Iterator, Optional, Self


class InvalidMoveError(Exception):
    pass


class Mark(StrEnum):
    E = auto()
    X = auto()
    O = auto()  # noqa: E741


class Space(StrEnum):
    TopLeft = auto()
    TopCenter = auto()
    TopRight = auto()
    MiddleLeft = auto()
    MiddleCenter = auto()
    MiddleRight = auto()
    BottomLeft = auto()
    BottomCenter = auto()
    BottomRight = auto()

    @classmethod
    def from_int(cls, value: int) -> Self:
        # Dial pad layout (1 indexed)
        value_map = {i + 1: space for i, space in enumerate(Space)}
        return value_map[value]


class Player(StrEnum):
    X = auto()
    O = auto()  # noqa: E741

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
        for space_value in range(1, 10):
            space = Space.from_int(space_value)
            mark = self.get(space)
            mark = mark if mark in (Mark.X, Mark.O) else str(space_value)
            ret += f"| {mark} "

            if space_value % 3 == 0:
                ret += "|\n"
        return ret


class Game:
    board: Board
    current_player: Player

    def __init__(self) -> None:
        self.board = Board()
        self.current_player = Player.X

    def make_move(self, space: Space) -> None:
        if self.board.get(space) != Mark.E:
            raise InvalidMoveError
        mark = self.current_player.get_mark()
        self.board.set(space, mark)

    def iter_rows(self) -> Iterator[list[Mark]]:
        yield [self.board.get(s) for s in (Space.TopLeft, Space.TopCenter, Space.TopRight)]
        yield [self.board.get(s) for s in (Space.MiddleLeft, Space.MiddleCenter, Space.MiddleRight)]
        yield [self.board.get(s) for s in (Space.BottomLeft, Space.BottomCenter, Space.BottomRight)]

    def iter_cols(self) -> Iterator[list[Mark]]:
        yield [self.board.get(s) for s in (Space.TopLeft, Space.MiddleLeft, Space.BottomLeft)]
        yield [self.board.get(s) for s in (Space.TopCenter, Space.MiddleCenter, Space.BottomCenter)]
        yield [self.board.get(s) for s in (Space.TopRight, Space.MiddleRight, Space.BottomRight)]

    def iter_diagonals(self) -> Iterator[list[Mark]]:
        yield [self.board.get(s) for s in (Space.TopLeft, Space.MiddleCenter, Space.BottomRight)]
        yield [self.board.get(s) for s in (Space.TopRight, Space.MiddleCenter, Space.BottomLeft)]

    def iter_triples(self) -> Iterator[list[Mark]]:
        yield from self.iter_rows()
        yield from self.iter_cols()
        yield from self.iter_diagonals()

    def get_winner(self) -> Optional[Player]:
        for triple in self.iter_triples():
            if all(mark == Mark.X for mark in triple):
                return Player.X
            if all(mark == Mark.O for mark in triple):
                return Player.O
        return None

    def switch_current_player(self) -> None:
        match self.current_player:
            case Player.O:
                self.current_player = Player.X
            case Player.X:
                self.current_player = Player.O

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
                    print("invalid space number, must be an int")
                    continue

                try:
                    space = Space.from_int(space_int)
                except ValueError:
                    print("invalid space number, must be 1-9")
                    continue

                try:
                    self.make_move(space)
                    valid_input = True
                    self.switch_current_player()

                    winner = self.get_winner()
                    if winner is not None:
                        print(self.board)
                        print(f"winner is {winner}")
                        game_over = True
                        continue
                except InvalidMoveError:
                    print(f"invalid move, space {space} already taken")
                    continue


if __name__ == "__main__":
    game = Game()
    game.play()
