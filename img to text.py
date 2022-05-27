import cv2
import pytesseract
from difflib import SequenceMatcher

# specify the path of the tesseract in the disk
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

modal_errors = {
    "SYSTEM SETTINGS RESET": ["invalid configuration information please run setup program",
                              "time-of-day not set - please run setup program"],
    "MEMORY SIZE CHANGE": ["alert! the amount of system memory has changed"],
    "MEMORY CONFIGURATION ERROR": [
        "error! memory configured incorrectly. please enter setup for memory information details"],
    "HARDWARE FAILED/MISSING": ["alert! hard drive fan failure",
                                "alert! cpu 0 fan failure",
                                "alert! front i/o cable failure",
                                "alert! rear fan failure",
                                "alert! air temperature sensor not detected",
                                "alert! hard drive not found"],
    "KEYBOARD INITIALIZATION FAILURE": ["alert! keyboard initialization failure"],
    "CPU MICROCODE UPDATE FAILED": ["alert! the cpu microcode update failed"],
    "JUMPER ERROR": ["alert! service mode jumper is set"],
    "BOOT ERROR": ["no bootable devices found"]
}


# Reversing a list using reversed()
def Reverse(lst):
    return [ele for ele in reversed(lst)]


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def main(img):
    img = cv2.imread(img)
    text = pytesseract.image_to_string(img, lang='eng')
    text_to_arr = (text.split('\n'))
    space_to_empty = [x.strip() for x in text_to_arr]
    space_clean_list = [x.lower() for x in space_to_empty if x]
    to_rm = []
    for rm_un in space_clean_list:
        if rm_un.startswith("to"):
            to_rm.append(space_clean_list.index(rm_un))
    for val in Reverse(to_rm):
        del space_clean_list[val]

    result = []
    for key, value in modal_errors.items():
        for val in value:
            for to_match in space_clean_list:
                # print(val)
                # print(to_match)
                if similar(val, to_match.lower()) > 0.85:
                    # print(val, '------', to_match.lower())
                    # print(key)
                    result.append((key, val))
    return result


res = main("dell_posterror/1dcb6fa86ed3ad359716532b1e252806062e85b43a1a42965628f892b54fc2c4.jpg")
print(res)
