import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

FILE_TYPES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov"],
    "Music": [".mp3", ".wav", ".flac"],
    "PDFs": [".pdf"],
    "Documents": [".doc", ".docx", ".txt"],
    "Python": [".py"],
    "Archives": [".zip", ".rar", ".7z"],
}


def get_category(ext):
    ext = ext.lower()

    for folder, extensions in FILE_TYPES.items():
        if ext in extensions:
            return folder

    return "Others"


def unique_name(folder, filename):

    name, ext = os.path.splitext(filename)

    counter = 1

    new_name = filename

    while os.path.exists(os.path.join(folder, new_name)):
        new_name = f"{name}({counter}){ext}"
        counter += 1

    return new_name


def browse_folder():
    folder = filedialog.askdirectory()

    if folder:
        folder_entry.delete(0, tk.END)
        folder_entry.insert(0, folder)


def organize():

    folder = folder_entry.get()

    if not os.path.exists(folder):
        messagebox.showerror("Error", "Folder not found")
        return

    output.delete("1.0", tk.END)

    stats = {}

    for file in os.listdir(folder):

        source = os.path.join(folder, file)

        if os.path.isdir(source):
            continue

        _, ext = os.path.splitext(file)

        category = get_category(ext)

        destination_folder = os.path.join(folder, category)

        os.makedirs(destination_folder, exist_ok=True)

        new_name = unique_name(destination_folder, file)

        destination = os.path.join(destination_folder, new_name)

        shutil.move(source, destination)

        output.insert(tk.END, f"✅ {file} → {category}\n")

        stats[category] = stats.get(category, 0) + 1

    output.insert(tk.END, "\n------ SUMMARY ------\n")

    total = 0

    for k, v in stats.items():
        output.insert(tk.END, f"{k}: {v}\n")
        total += v

    output.insert(tk.END, f"\nTotal Files: {total}\n")

    messagebox.showinfo("Done", "Files Organized Successfully!")


root = tk.Tk()

root.title("Smart File Organizer")

root.geometry("700x500")

title = tk.Label(
    root,
    text="Smart File Organizer",
    font=("Arial", 20, "bold")
)

title.pack(pady=10)

folder_entry = tk.Entry(root, width=60)

folder_entry.pack(pady=5)

browse = tk.Button(
    root,
    text="Browse Folder",
    command=browse_folder
)

browse.pack()

run = tk.Button(
    root,
    text="Organize Files",
    command=organize,
    bg="green",
    fg="white",
    width=20
)

run.pack(pady=10)

output = scrolledtext.ScrolledText(
    root,
    width=80,
    height=18
)

output.pack()

root.mainloop()