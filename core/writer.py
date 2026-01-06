def write_output_file(output, structure, contents, stats):
    with open(output, "w", encoding="utf-8") as f:
        f.write("=" * 80 + "\n")
        f.write("GIT REPOSITORY STRUCTURE\n")
        f.write("=" * 80 + "\n\n")
        f.write("\n".join(structure))

        f.write("\n\n" + "=" * 80 + "\n")
        f.write("FILE CONTENTS\n")
        f.write("=" * 80 + "\n")

        for item in contents:
            f.write("\n" + "-" * 80 + "\n")
            f.write(f"FILE: {item['path']}\n")
            f.write("-" * 80 + "\n")
            f.write(item["content"] + "\n")

        f.write("\n" + "=" * 80 + "\n")
        f.write("SUMMARY\n")
        f.write("=" * 80 + "\n")
        for k, v in stats.items():
            f.write(f"{k.replace('_', ' ').title():25}: {v}\n")
