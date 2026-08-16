import os

def get_desktop_path():
    return os.path.join(os.path.expanduser("~"), "Desktop")

def get_downloads_path():
    return os.path.join(os.path.expanduser("~"), "Downloads")

def list_files(folder_path, limit=10):
    if not os.path.exists(folder_path):
        return []

    files = []

    for file in os.listdir(folder_path):
        full_path = os.path.join(folder_path, file)

        if os.path.isfile(full_path):
            files.append(file)

    return files[:limit]

def find_files_by_keyword(folder_path, keyword):
    matches = []

    if not os.path.exists(folder_path):
        return matches

    for file in os.listdir(folder_path):
        if keyword.lower() in file.lower():
            matches.append(os.path.join(folder_path, file))

    return matches

def find_pdf_files(folder_path):
    pdfs = []

    if not os.path.exists(folder_path):
        return pdfs

    for file in os.listdir(folder_path):
        if file.lower().endswith(".pdf"):
            pdfs.append(os.path.join(folder_path, file))

    return pdfs

def open_file(file_path):
    if os.path.exists(file_path):
        os.startfile(file_path)
        return True

    return False