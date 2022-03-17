import sys
import os.path
import os
import interpreter

def run(file_name: str) -> None:
    interp = interpreter.Interpreter()
    output_dir = os.path.join(os.path.dirname(os.path.dirname(file_name)), "outputs")
    output_file = os.path.join(output_dir, os.path.basename(file_name).replace(".bq", ".out"))
    instructions = interp.parse(file_name)
    interp.run_instructions(instructions)
    with open(output_file, "r") as file:
        result = file.read()
    assert result.strip() == interp.stdout.strip()

class TestInterpreter:
    def test_one(self):
        run("tests/inputs/test1.bq")
    
    def test_two(self):
        run("tests/inputs/test2.bq")
    
    def test_three(self):
        run("tests/inputs/test3.bq")
    
    def test_four(self):
        run("tests/inputs/test4.bq")

    def test_five(self):
        run("tests/inputs/test5.bq")
    
    def test_six(self):
        run("tests/inputs/test6.bq")
    
    def test_seven(self):
        run("tests/inputs/test7.bq")
    
    def test_eight(self):
        run("tests/inputs/test8.bq")
    
    def test_nine(self):
        run("tests/inputs/test9.bq")
    
    def test_sorting(self):
        run("tests/inputs/testSorting.bq")

