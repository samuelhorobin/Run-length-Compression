''' Run-length encoder '''
import pickle
import os


class BitMap:
    def __init__(self, data = [[]]):
        self.data = data

    def append_data(self, data):
        if data == 2:
            self.data.append([])
        else:
            if len(self.data) > 1:
                if len(self.data[-1]) == len(self.data[-2]):
                    self.data.append([])
            self.data[-1].append(data)

    def display_data(self):
        print("\n"*10)
        for row in self.data:
            dispData = row.copy()
            for i, val in enumerate(dispData):
                if val == 0:
                    dispData[i] = "░"
                elif val == 1:
                    dispData[i] = "█"
            print(" ".join(dispData))

    def compress_bitmap(self):
        compressed = []
        for row in self.data:
            compressed.append(compress_list(row))
        return compressed

    def save(self):
        uncompressed = self.data
        compressed = self.compress_bitmap()
        print("Saving compressed...")
        with open("compressed.pickle", "wb") as f:
            pickle.dump(compressed, f, protocol=pickle.HIGHEST_PROTOCOL)
            f.close()
        print("Compressed saved!")
        
        print("Saving raw...")
        with open("raw.pickle", "wb") as f:
            pickle.dump(uncompressed, f, protocol=pickle.HIGHEST_PROTOCOL)
            f.close()
        print("Raw saved!")

def compress_list(list):
    compressedList = [[0, list[0]]]  # Tuple() = (frequency, token)
    for value in list:
        if value == compressedList[-1][1]:  # [-1][1] = recently-appended token
            compressedList[-1][0] += 1      # [-1][0] = recently-appended token's frequency
        else:
            compressedList.append([1, value])
    return compressedList

def get_bitmap_input():
    running = True
    while running:
        try:
            inputVal = int(
                input("\nEnter a value:\n0 - bitmap val\n1 - bitmap val\n2 - newLine\n3 - Exit\n"))
            if 0 <= inputVal <= 3:
                running = False
            else:
                raise ValueError
        except:
            print(" - Invalid value - ")
    return inputVal

def get_bitmap():
    bitmap = BitMap()
    active = True
    while active:
        userInput = get_bitmap_input()
        if userInput == 3:
            active = False
            break
        else:
            bitmap.append_data(userInput)
            bitmap.display_data()
    return bitmap

def get_input(*optionList: list):
    running = True
    message = "".join([f"{key}: {index}\n" for index, key in enumerate(optionList, 1)])
    while running:
        try:
            inputVal = int(
                input(f"{message}"))
            if 1 <= inputVal <= len(optionList):
                running = False
            else:
                raise ValueError
        except:
            print(" - Invalid value - ")
    return inputVal

def load():
    with open("raw.pickle", "rb") as f:
        raw = pickle.load(f)
        return BitMap(raw)

def main():
    running = True
    bitmap = None
    while running:
        choice = get_input("New bitmap", "Save", "Load", "View", "Compare sizes", "Exit")
        
        if choice == 1:
            bitmap = get_bitmap()

        if choice == 2:
            if bitmap != None:
                bitmap.save()
            else:
                print("Load or make a bitmap first")

        if choice == 3:
            print("Loading bitmap...")
            bitmap = load()
            print("...Bitmap loaded!")

        if choice == 4:
            if bitmap != None:
                bitmap.display_data()
            else:
                print("Load or make a bitmap first")

        if choice == 5:
            rawSize = os.path.getsize("raw.pickle")
            compressedSize = os.path.getsize("compressed.pickle")
            print(f"Raw: {rawSize}\nCompressed: {compressedSize}\n")

        if choice == 6:
            running = False

            


if __name__ == "__main__":
    main()
