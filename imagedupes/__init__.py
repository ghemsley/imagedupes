#!/usr/bin/python3

def checkHashAlgorithmChoice(__algorithmString):

    from sys import exit

    __acceptableChoices = ['dhash', 'dhash_vertical', 'ahash', 'phash', 'phash_simple', 'whash_haar', 'whash_db4']
    if __algorithmString not in __acceptableChoices:
        print("Error: please choose a valid hash algorithm. Use the -h command line flag for help.")
        exit()

def getImagePaths(__dirPath, __recursiveBoolean, __followLinksBoolean):
    "Creates a list of image paths within a given directory"

    import os

    __filePathList = []

    print("Searching for duplicate images...")
    if __recursiveBoolean == True:
        for __root, __dirs, __files in os.walk(__dirPath, followlinks=__followLinksBoolean):
            for __file in __files:
                if str(__file).lower().endswith(".jpg") or str(__file).lower().endswith(".jpeg")\
                or str(__file).lower().endswith(".png") or str(__file).lower().endswith(".tif")\
                or str(__file).lower().endswith(".tiff") or str(__file).lower().endswith(".webp")\
                or str(__file).lower().endswith(".bmp"):
                    __filePathList.append(os.path.join(__root, __file))
    else:
        for __file in os.listdir(__dirPath):
            if str(__file).lower().endswith(".jpg") or str(__file).lower().endswith(".jpeg")\
            or str(__file).lower().endswith(".png") or str(__file).lower().endswith(".tif")\
            or str(__file).lower().endswith(".tiff") or str(__file).lower().endswith(".webp")\
            or str(__file).lower().endswith(".bmp"):
                __filePathList.append(os.path.join(__dirPath, __file))
    return __filePathList

def generateHashDict(__imagePathList, __hashAlgorithm, __hashSizeInt):

    from PIL import Image
    from imagehash import dhash
    from imagehash import dhash_vertical
    from imagehash import average_hash
    from imagehash import phash
    from imagehash import phash_simple
    from imagehash import whash

    __imageHashDict = {}
    __image = None

    if __hashSizeInt == None:
        __hashSizeInt = 8
    for __imagePath in __imagePathList:
        print("Hashing " + str(__imagePath))
        __image = Image.open(__imagePath)
        if __hashAlgorithm == 'dhash':
            __imageHashDict[__imagePath] = dhash(__image, hash_size=__hashSizeInt)
        elif __hashAlgorithm == 'dhash_vertical':
            __imageHashDict[__imagePath] = dhash_vertical(__image, hash_size=__hashSizeInt)
        elif __hashAlgorithm == 'ahash':
            __imageHashDict[__imagePath] = average_hash(__image, hash_size=__hashSizeInt)
        elif __hashAlgorithm == 'phash':
            __imageHashDict[__imagePath] = phash(__image, hash_size=__hashSizeInt)
        elif __hashAlgorithm == 'phash_simple':
            __imageHashDict[__imagePath] = phash_simple(__image, hash_size=__hashSizeInt)
        elif __hashAlgorithm == 'whash_haar':
            __imageHashDict[__imagePath] = whash(__image, hash_size=__hashSizeInt)
        elif __hashAlgorithm == 'whash_db4':
            __imageHashDict[__imagePath] = whash(__image, hash_size=__hashSizeInt, mode='db4')
        elif __hashAlgorithm == None:
            __imageHashDict[__imagePath] = phash(__image, hash_size=__hashSizeInt)
        __image.close

    return __imageHashDict


def compareHashes(__imageHashDict):

    __reverseMultiDict = {}
    __duplicateListOfSets = {}
    __duplicateListOfLists = []

    for __key, __value in __imageHashDict.items():
        __reverseMultiDict.setdefault(__value, set()).add(__key)
    __duplicateListOfSets = [__values for __key, __values in __reverseMultiDict.items() if len(__values) > 1]
    for __i in range(0, len(__duplicateListOfSets)):
        __duplicateListOfLists.append(list(__duplicateListOfSets[__i]))
    return __duplicateListOfLists

def printDuplicates(__imageListOfLists):

    for __i in range(0, len(__imageListOfLists)):
        for __j in range(0, len(__imageListOfLists[__i])):
            print("Found possible duplicate: " + str(__imageListOfLists[__i][__j]))
    return __imageListOfLists

def displayImage(__imageListOfLists):

    import webbrowser

    for __i in range(0, len(__imageListOfLists)):
        input("Press enter to open the next set of possible duplicates: ")
        for __j in range(0, len(__imageListOfLists[__i])):
            webbrowser.open(__imageListOfLists[__i][__j])


def main():

    from argparse import ArgumentParser
    import os
    from sys import exit

    __recursive = False

    __parser = ArgumentParser(description="Finds visually similar images and opens them in the default image file handler, one group of matches at a time. If no options are specified, it defaults to searching the current working directory non-recursively using a perceptual image hash algorithm with a hash size of 8 and does not follow symbolic links.")
    __parser.add_argument("-a", "--algorithm", type=str, help="Specify a hash algorithm to use. Acceptable inputs:\n'dhash' (horizontal difference hash),\n'dhash_vertical',\n'ahash' (average hash),\n'phash' (perceptual hash),\n'phash_simple',\n'whash_haar' (Haar wavelet hash),\n'whash_db4' (Daubechles wavelet hash). Defaults to 'phash' if not specified.")
    __parser.add_argument("-d", "--directory", type=str, help="Directory to search for images")
    __parser.add_argument("-l", "--links", action="store_true", help="Follow symbolic links. Defaults to off if not specified.")
    __parser.add_argument("-r", "--recursive", action="store_true", help="Search through directories recursively. Defaults to off if not specified.")
    __parser.add_argument("-s", "--hash_size", type=int, help="Resolution of the hash; higher is more sensitive to differences. Must be a power of 2 (2, 4, 8, 16...). Defaults to 8 if not specified.")
    __args = __parser.parse_args()

    if __args.algorithm is not None:
        checkHashAlgorithmChoice(__args.algorithm)
    if __args.directory is not None:
        displayImage(printDuplicates(compareHashes(generateHashDict(getImagePaths(__args.directory, __args.recursive, __args.links), __args.algorithm, __args.hash_size))))
    else:
        displayImage(printDuplicates(compareHashes(generateHashDict(getImagePaths(os.path.curdir, __args.recursive, __args.links), __args.algorithm, __args.hash_size))))
    exit()
