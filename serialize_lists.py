import pickle
import os


def write_dump(list_to_save: list, file_name: str) -> None:
    """Writes an object to file in a binary format.
    :list_to_save : A list that we want to write file
    :file_name: A string that contains the file name
    """
    open_file = open(file_name, "wb")
    pickle.dump(list_to_save, open_file)
    open_file.close()


def read_dump(file_name: str) -> list:
    """Reads a list from binary file and returns it
    :file_name : A string that contains the file name
    :return: A list that was read from the file
    """
    open_file = open(file_name, "rb")
    loaded_list = pickle.load(open_file)
    open_file.close()
    return loaded_list


def merge_files():
    all_files = os.listdir("./data/")
    merged_list = []
    for file_name in all_files:
        if file_name.endswith('.attributes'):
            tmp_list = read_dump(f"./data/{file_name}")
            merged_list.append(tmp_list)
    print("This should be 20:", len(merged_list))
    write_dump(merged_list, "./data/MERGED_LIST.NLTK")
    return merged_list


#merge_files()