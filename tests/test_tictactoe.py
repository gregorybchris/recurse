import re

import pytest

from recurse.tictactoe import Board, Checker, Game, InvalidMoveError, Mark, Player, Space


class TestMark:
    def test_mark_size(self) -> None:
        assert len(Mark) == 3


class TestSpace:
    def test_from_int(self) -> None:
        assert Space.from_int(1) == Space.TopLeft
        assert Space.from_int(3) == Space.TopRight
        assert Space.from_int(9) == Space.BottomRight


class TestPlayer:
    def test_get_mark(self) -> None:
        assert Player.X.get_mark() == Mark.X
        assert Player.O.get_mark() == Mark.O


class TestBoard:
    def test_get_all_empty_on_init(self) -> None:
        board = Board()
        for space in Space:
            assert board.get(space) == Mark.E

    def test_get_set(self) -> None:
        board = Board()
        board.set(Space.TopCenter, Mark.X)
        assert board.get(Space.TopCenter) == Mark.X


class TestChecker:
    def test_iter_triples(self) -> None:
        board = Board()
        triples = list(Checker.iter_triples(board))
        assert len(triples) == 8
        for triple in triples:
            assert len(triple) == 3

    def test_get_winner_row_o(self) -> None:
        board = Board()
        board.set(Space.TopLeft, Mark.O)
        board.set(Space.TopCenter, Mark.O)
        board.set(Space.TopRight, Mark.O)

        assert Checker.get_winner(board) == Player.O

    def test_get_winner_col_x(self) -> None:
        board = Board()
        board.set(Space.TopLeft, Mark.X)
        board.set(Space.MiddleLeft, Mark.X)
        board.set(Space.BottomLeft, Mark.X)

        assert Checker.get_winner(board) == Player.X

    def test_get_winner_diagonal(self) -> None:
        board = Board()
        board.set(Space.TopLeft, Mark.X)
        board.set(Space.MiddleCenter, Mark.X)
        board.set(Space.BottomRight, Mark.X)

        assert Checker.get_winner(board) == Player.X

    def test_get_winner_none(self) -> None:
        board = Board()
        board.set(Space.TopLeft, Mark.O)
        board.set(Space.TopCenter, Mark.O)

        assert Checker.get_winner(board) is None


class TestGame:
    def test_make_first_move(self) -> None:
        game = Game()
        assert game.board.get(Space.TopRight) == Mark.E
        assert game.current_player == Player.X
        game.make_move(Space.TopRight)
        assert game.board.get(Space.TopRight) == Mark.X
        assert game.current_player == Player.O

    def test_make_taken_move(self) -> None:
        game = Game()
        game.make_move(Space.TopLeft)
        with pytest.raises(InvalidMoveError, match=re.escape("board space top-left not empty")):
            game.make_move(Space.TopLeft)
