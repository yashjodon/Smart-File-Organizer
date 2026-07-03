import os
import shutil
LOG_FILE = "organizer.log"
FILE_TYPES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov"],
    "Music": [".mp3", ".wav", ".flac"],
    "PDFs": [".pdf"],
    "Documents": [".doc", ".docx", ".txt"],
    "Python": [".py"],
    "Archives": [".zip", ".rar", ".7z"],
}

stats = {}

# -----------------------------
# User Input
# -----------------------------
TARGET_FOLDER = input("📁 Enter folder path: ").strip()

if not os.path.exists(TARGET_FOLDER):
    print("❌ Folder not found!")
    exit()

# -----------------------------
# Create Log File
# -----------------------------
with open(LOG_FILE, "w") as log:
    log.write("===== Smart File Organizer =====\n\n")


def get_category(extension):
    """Return folder name based on file extension."""
    extension = extension.lower()

    for folder, extensions in FILE_TYPES.items():
        if extension in extensions:
            return folder

    return "Others"


def get_unique_filename(destination_folder, filename):
    """Avoid overwriting duplicate files."""

    name, extension = os.path.splitext(filename)

    counter = 1

    new_name = filename

    while os.path.exists(os.path.join(destination_folder, new_name)):
        new_name = f"{name}({counter}){extension}"
        counter += 1

    return new_name


# -----------------------------
# Organize Files
# -----------------------------
for file_name in os.listdir(TARGET_FOLDER):

    source = os.path.join(TARGET_FOLDER, file_name)

    if os.path.isdir(source):
        continue

    _, extension = os.path.splitext(file_name)

    category = get_category(extension)

    destination_folder = os.path.join(TARGET_FOLDER, category)

    os.makedirs(destination_folder, exist_ok=True)

    new_name = get_unique_filename(destination_folder, file_name)

    destination = os.path.join(destination_folder, new_name)

    try:

        shutil.move(source, destination)

        print(f"✅ {file_name} → {category}")

        stats[category] = stats.get(category, 0) + 1

        with open(LOG_FILE, "a") as log:
            log.write(f"{file_name} -> {category}\n")

    except Exception as error:
        print(f"❌ Error: {error}")

# -----------------------------
# Summary
# -----------------------------
print("\n" + "=" * 40)
print("📊 SUMMARY")
print("=" * 40)

total = 0

for category, count in stats.items():
    print(f"{category:<12}: {count}")
    total += count

print("-" * 40)
print(f"Total Files : {total}")

print("\n📝 Log File :", LOG_FILE)
print("🎉 File Organization Completed!")