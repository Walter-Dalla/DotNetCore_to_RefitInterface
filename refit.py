import os
import re
import sys

def search_cs_files(directory):
    """Recursively search for .cs files in the given directory"""
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".cs"):
                yield os.path.join(root, file)


def get_path(match, fileContent):
    start = match.start()
    end = match.end()
    line_start = fileContent.rfind('\n', 0, start) + 1
    line_end = fileContent.find('\n', end)
    if line_end == -1:
        line_end = len(fileContent)
    line = fileContent[line_start:line_end]    

    path = ""
    method = ""

    pattern = r'".*"'
    match = re.search(pattern, line)
    if match:
        path =  match.group().replace("\"","")
    
    
    matchMethod = re.search(METHOD_REGEX, line)
    if matchMethod:
        method =  matchMethod.group().replace("Http","")

    return path, line_end, method

def get_function_decaration(match, fileContent, line_end):
    nextline_start = line_end + 1
    nextline_end = fileContent.find('\n', nextline_start)
    if nextline_end == -1:
        nextline_end = len(fileContent)
    nextLine = fileContent[nextline_start:nextline_end]

    pattern = r'\w+\(.*\)'
    match = re.search(pattern, nextLine)
    if match:
        return match.group()

def get_class_decaration(match, fileContent, line_end):
    nextline_start = line_end + 1
    nextline_end = fileContent.find('\n', nextline_start)
    if nextline_end == -1:
        nextline_end = len(fileContent)
    nextLine = fileContent[nextline_start:nextline_end]

    pattern = r'class \w+'
    match = re.search(pattern, nextLine)
    if match:
        return match.group().replace("class ", "").replace("Controller", "")
    return ""


METHOD_REGEX = 'HttpPost|HttpGet'
ROUTE_REGEX = "\[Route\("
def search_for_string_in_files(directory_path):
    path = ""
    functionDeclaration = ""
    classDeclaration = ""
    method = ""

    # Search for all .cs files in the directory and subdirectories
    cs_files = list(search_cs_files(directory_path))

    for file in cs_files:
        if "obj"in file or "bin" in file: # Compilation folders
            continue

        with open(file, 'r') as f:

            fileContent = f.read()
             
            if re.search(ROUTE_REGEX, fileContent):
                for match in re.finditer(ROUTE_REGEX, fileContent):
                    _path2, line_end, _method2 = get_path(match, fileContent)
                    classDeclaration = get_class_decaration(match, fileContent, line_end)
                    classDeclaration = _path2.replace("[controller]", classDeclaration)
                    
                    if re.search(METHOD_REGEX, fileContent):
                        for match in re.finditer(METHOD_REGEX, fileContent):
                            path, line_end, method = get_path(match, fileContent)
                            functionDeclaration = get_function_decaration(match, fileContent, line_end)
    
                            print(f"\t[{method}(\"/{classDeclaration}/{path}\")]\n"+
                                f"\tTask<object> {functionDeclaration};\n")


directory_path = sys.argv[1] #"F:\Projets\ProjectName"

print("public interface IApi {\n")
search_for_string_in_files(directory_path)
print("}")