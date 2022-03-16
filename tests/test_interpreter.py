import sys
import os.path
import os
import interpreter

def run(file_name: str) -> None:
    output_dir = os.path.join(os.path.dirname(os.path.dirname(file_name)), "outputs")
    output_file = os.path.join(output_dir, os.path.basename(file_name).replace(".code", ".out"))
    instructions = interpreter.parse(file_name)
    interpreter.run_instructions(instructions)
    with open(output_file, "r") as file:
        result = file.read()
    assert result.strip() == interpreter.stdout.strip()

class TestInterpreter:
    def test_one(self):
        run("tests/inputs/test1.code")
    
    def test_two(self):
        run("tests/inputs/test2.code")
    
    def test_three(self):
        run("tests/inputs/test3.code")
    
    def test_four(self):
        run("tests/inputs/test4.code")

    def test_five(self):
        run("tests/inputs/test5.code")
    
    def test_six(self):
        run("tests/inputs/test6.code")
    
    def test_seven(self):
        run("tests/inputs/test7.code")
    
    def test_eight(self):
        run("tests/inputs/test8.code")
    
    def test_nine(self):
        run("tests/inputs/test9.code")
    
    def test_sorting(self):
        run("tests/inputs/testSorting.code")

