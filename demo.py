import os


def traverse_dir(dir_path: str):
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            file_path = os.path.join(root, file)
            yield file_path


def reanme_file():
    print('rename file')


if __name__ == '__main__':

    traverse_dir('./data')
