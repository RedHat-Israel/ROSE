def joing_files(file_name1, file_name2, out_file_name):
    """
    Reads the first two files, joins them and writes the data to the third one.
    """
    try:
        file1 = open(file_name1, "r").read()
        file2 = open(file_name2, "r").read()
        open(out_file_name, "w").write(file1 + file2)
        print("The files were joined successfully!")
    except Exception as e:
        print(e)
        print("Reading or writing error with one of the files!")


file_name_1 = input("Enter the first file name: ")
file_name_2 = input("Enter the second file name: ")
file_name_3 = input("Enter the third file name: ")

joing_files(file_name_1, file_name_2, file_name_3)
