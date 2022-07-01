#function that return false if folder is invalid
def checkIfFolderIsValid(folderName):
    invalidSymbols = "/\\:*?\"<>|"
    for invalidSymbol in invalidSymbols:
        if invalidSymbol in folderName:
            return False
    return True

print(checkIfFolderIsValid("/a"))
print(checkIfFolderIsValid("/\\/"))