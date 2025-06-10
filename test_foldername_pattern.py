# regex_testing.py
# validate regex expression of the filename
import pytest
import re
#TODO: Fix the patter pattern_unknown to accept folder names that are 1 cahracter long.

pattern_bad     = r"^[A-Za-z0-9_()\(\)]([A-Za-z0-9\.\-_ \(\)]*)[A-Za-z0-9_()\(\)]$" #file must be >= 2 characters, and \n is not allowd, but still returning a match object if \n is trailing character-
# even through that match object always excludes the trailing \n in the span range (which is technically valid, but not our intended behavior of the match function)
pattern_bad2    = r"^[A-Za-z0-9_()\(\)]([A-Za-z0-9\.\-_ \(\)]*)?[A-Za-z0-9_()\(\)]$" # Supposed to fix >=2 char problem ()
pattern_unknown = r"^[A-Za-z0-9_()\(\)]([A-Za-z0-9\.\-_ \(\)]*)?[A-Za-z0-9_()\(\)]\Z" # fix \n trailing problem (and supposed to fix 2 char)

PATTERN = pattern_unknown

valid_filenames = [
    "A", "z", "0", "_", "(", ")",
    "A_file-name.0)", "0filename_", "(filename_1)", "_A0.z-(",
    "AfileA", "0file0", "Afile0", "0fileA", "_file_", "(file)", ")file(", "_fileA", "Afile_", "0file(", "(file0"
]

invalid_filenames = [
    ".file", "-file", " file", "file.", "file-", "file ",
    ".", "-", " ", "file\n", "file\nfile", "\nfile", " \nfile\n ", "\nfile\nfile\n", "ffile\tfile", "folder/file", "folderwindows\\file", "C:\\", "C:", ":", "/", "/root",
    "..file", "--file", "  file",
    "file..", "file--", "file  "
]

@pytest.mark.parametrize("filename", valid_filenames)
def test_valid_filenames(filename):
    assert re.match(PATTERN, filename) is not None, f"Valid {filename} was not matched"

@pytest.mark.parametrize("filename", invalid_filenames)
def test_invalid_filenames(filename):
    assert re.match(PATTERN, filename) is None, f"An INVALID {filename} was matched, !!!!!!!you could have destroyed the filesystem!"

if __name__ == '__main__':
    pytest.main() # Run Command: pytest test_foldername_pattern.py


#Run command reccomended by ?copiolot right or better?: python -m pytest -v -s test_foldername_pattern.py
# TODO: after test pattern, then simplyfy pattern and then retest
