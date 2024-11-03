
# The two modules used in this assignment are built in python.
import os  # This module basically is used here to check, create and read files on the operating system in the specific path.
import re  # This  module is used to check the type of data and format of the data in python( strings,char,numbers,floats,etc.)

# Preprocessor class: Reads a file and performs basic cleanup tasks
class Preprocessor_task1:
    def __init__(self, file_name):
        self.file_name = file_name
        self.lines = []
        self.output_file = "output1.txt"

    def open_file(self):
        # Check if file exists before proceeding
        if not os.path.isfile(self.file_name):
            print("File does not exist.")
            return False
        else:
            return True

    def read_file(self):
        # Read file contents into a list of lines
        with open(self.file_name, 'r') as f:
            self.lines = f.readlines()

    def remove_blank_lines(self):
        # Remove empty lines from the file content
        self.lines = [line for line in self.lines if line.strip()]

    def remove_comments(self):
        # Remove single-line (//) and multi-line (/* ... */) comments
        in_multiline_comment = False
        cleaned_lines = []

        for line in self.lines:
            new_line = ""
            i = 0
            while i < len(line):
                if line[i:i+2] == "/*":
                    in_multiline_comment = True
                    i += 2
                elif line[i:i+2] == "*/" and in_multiline_comment:
                    in_multiline_comment = False
                    i += 2
                elif in_multiline_comment:
                    i += 1
                elif line[i:i+2] == "//":
                    break  # Skip the rest of the line
                else:
                    new_line += line[i]
                    i += 1
            if new_line.strip() and not in_multiline_comment:
                cleaned_lines.append(new_line.strip())

        self.lines = cleaned_lines

    def remove_excess_whitespace(self):
        # Remove extra spaces and tabs within lines
        self.lines = [" ".join(line.split()) for line in self.lines]

    def remove_imports_and_annotations(self):
        # Removing the  lines starting with "import" or annotations starting with "@"
        self.lines = [line for line in self.lines if not line.startswith("import") and not line.lstrip().startswith("@")]
    
    def write_output(self):
        # Creating the output1.txt file after removing by following the requirements in task 1.
        with open(self.output_file, 'w') as f:
            f.write("\n".join(self.lines))
        print(f"Output written to {self.output_file}")

#  Task2: Reads file character by character and writes it to a new output file
class Processor_task2 :
    def __init__(self, filename):
        self.filename = filename
        self.buffer = []

    def read_file(self):
        # Read file and add characters to buffer, ignoring newlines
        if not os.path.isfile(self.filename):
            raise FileNotFoundError(f"The file '{self.filename}' does not exist.")

        with open(self.filename, 'r') as file:
            for char in file.read():
                if char != '\n':
                    self.buffer.append(char)
        
        # Add sentinel value at the end of the buffer
        self.buffer.append('$')

    def write_output(self):
        # Writing buffer contents to output2.txt and display it
        output_content = ''.join(self.buffer)
        with open('output2.txt', 'w') as output_file:
            output_file.write(output_content)
        print(output_content)

    def process(self):
        # Full processing sequence
        self.read_file()
        self.write_output()

#  Task3 - LexicalAnalyzer class: Analyzes tokens in a file
class LexicalAnalyzer_Task_3:
    def __init__(self, filename):
        self.filename = filename
        # Tokens are defined based on the table given in Task 3.
        self.token_definitions = {
            "keywords": {"if", "else", "while", "for", "do", "int", "float", "double", "char", "void", "boolean", 
                         "true", "false", "return", "class", "public", "private", "protected", "static", "final", 
                         "try", "catch", "throw", "interface"},
            "operators": {"+", "-", "*", "/", "%", "=", "+=", "-=", "*=", "/=", "==", "!=", "<", ">", "<=", ">=", 
                          "++", "--", "&&", "||"},
            "punctuators": {"{", "}", "[", "]", "(", ")", ",", ";", ":", ".", "..."},
            "literals": {"true", "false", "null"},
            "annotations": {"@Override", "@Deprecated", "@SuppressWarnings"}
        }
        # Creating empty lists in which leximes are to be added for categorization.
        self.lexemes = {
            "Keywords": [],
            "Identifiers": [],
            "Operators": [],
            "Punctuators": [],
            "Literals": [],
            "Comments": [],
            "Annotations": [],
            "Imports": []
        }
    # Reading the file output2.txt
    def read_file(self):
        with open(self.filename, 'r') as file:
            self.content = file.read()
    # Splitting the tokens 
    def tokenize(self):
        """The re.split from the re package is used here to split the content of the txt file based on end of the word, even spaces. The 
        \s+ adds all spaces when the are separating words and is separted together as a single large space. The \b separtes words based on 
        when one word ends and another begins."""
        tokens = re.split(r'(\s+|\b)', self.content)
        
        for token in tokens:
            # token.strip() deletes whitespaces at the start and the end of the file. The codes continues if their is no white space.
            token = token.strip()
            if not token:
                continue

            # Check which category the token belongs to
            # Here we append the tokens to the lexemes categories based on the category to which they belong taken from token definations.
            if token in self.token_definitions["keywords"]:
                self.lexemes["Keywords"].append(token)
            elif token in self.token_definitions["operators"]:
                self.lexemes["Operators"].append(token)
            elif token in self.token_definitions["punctuators"]:
                self.lexemes["Punctuators"].append(token)
                """The re.match here is used to check whether the charchter starts with the following operators 
                then they are considered numbers or floats."""
            elif re.match(r'^[+-]?\d+(\.\d+)?$', token):  # Numbers (integers and floats)
                self.lexemes["Literals"].append(token)
                """The re.match here is used to check if the charachters starts with the folloeing symbols and classifies them as string or char"""
            elif re.match(r'^".*"$|^\'.*\'$', token):  # String or char literals
                self.lexemes["Literals"].append(token)
            elif token in self.token_definitions["literals"]:
                self.lexemes["Literals"].append(token)
            # starswith() method is used to check whether the token or content starts with a particular charachter.
            elif token.startswith("//") or token.startswith("/*"):
                self.lexemes["Comments"].append(token)
            elif token in self.token_definitions["annotations"]:
                self.lexemes["Annotations"].append(token)
            elif token.startswith("import"):
                self.lexemes["Imports"].append(token)
            elif re.match(r'^[a-zA-Z_]\w*$', token):  # Identifiers
                self.lexemes["Identifiers"].append(token)

    def display_lexemes(self):
        # Here we display the category of the lexemes and the lexemes itself.
        for category, lexemes in self.lexemes.items():
            print(f"{category}: {', '.join(lexemes)}")

    def process(self):
        self.read_file()
        self.tokenize()
        self.display_lexemes()

if __name__ == "__main__":
    # Performing all tasks in order
    input_file = str(input("Enter code file name with extension: ")) # Add the file path as well as the filename with extention.
    
    # Initialize and process the Preprocessor
    preprocessor = Preprocessor_task1(input_file)
    
    if preprocessor.open_file():
        preprocessor.read_file()
        preprocessor.remove_blank_lines()
        preprocessor.remove_comments()
        preprocessor.remove_excess_whitespace()
        preprocessor.remove_imports_and_annotations()
        preprocessor.write_output()  # Writing to output1.txt

        # Initialize and process the Processor
        processor = Processor_task2(preprocessor.output_file)
        processor.process()  # This will now read output1.txt after it's created

        # Lexical Analyzer
        lexical_analyzer = LexicalAnalyzer_Task_3("output2.txt")
        lexical_analyzer.process()
        
