from typer.testing import CliRunner

from recurse.cli import main

runner = CliRunner()


class TestCli:
    def test_hello_greets_the_world_by_default(self) -> None:
        result = runner.invoke(main, ["hello"])
        assert result.exit_code == 0
        assert "Hello, world!" in result.stdout

    def test_hello_greets_a_name(self) -> None:
        result = runner.invoke(main, ["hello", "--name", "recurse"])
        assert result.exit_code == 0
        assert "Hello, recurse!" in result.stdout
