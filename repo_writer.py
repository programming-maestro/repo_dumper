def write_output_file(output_path, structure, contents, stats):
    with open(output_path, "w", encoding="utf-8") as f:

        f.write("=" * 80 + "\n")
        f.write("GIT REPOSITORY STRUCTURE\n")
        f.write("=" * 80 + "\n\n")

        for line in structure:
            f.write(line + "\n")

        f.write("\n\n" + "=" * 80 + "\n")
        f.write("FILE CONTENTS\n")
        f.write("=" * 80 + "\n\n")

        for file in contents:
            f.write("\n" + "-" * 80 + "\n")
            f.write(f"FILE: {file['path']}\n")
            f.write("-" * 80 + "\n")
            f.write(file["content"] + "\n")

        f.write("\n\n" + "=" * 80 + "\n")
        f.write("SUMMARY\n")
        f.write("=" * 80 + "\n")

        f.write(f"Total files scanned  : {stats['files_total']}\n")
        f.write(f"Files dumped (text)  : {stats['files_dumped']}\n")
        f.write(f"Files skipped        : {stats['files_skipped']}\n")
        f.write(f"Folders scanned      : {stats['folders_total']}\n")

