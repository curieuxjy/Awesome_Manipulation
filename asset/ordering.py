import difflib
import os
import markdown

def alphabet_ordering(grouping_lines):
    grouping_lines.sort(key=str.lower)
    return grouping_lines

def remove_duplicates(lines):
    seen_titles = set()
    unique_lines = []
    for line in lines:
        if line.startswith("![]"):
            unique_lines.append(line)
        else:
            title = line.split(']')[0]  # Extract the title part
            short_title = title[:50]  # Consider only the first 50 characters
            if short_title not in seen_titles:
                unique_lines.append(line)
                seen_titles.add(short_title)
    return unique_lines

def order_md(file_stem: str):
    new_lines = []

    # Process the original {file_stem}.md file
    old_file_path = f'../{file_stem}.md'
    with open(old_file_path, 'r', encoding="UTF-8") as f:
        # Read and split into lines (remove the extra empty string if file ends with a newline)
        lines = f.read().split('\n')
        if lines and lines[-1] == '':
            lines = lines[:-1]

        grouping_lines = []
        for line in lines:
            if line.startswith('- ['):
                grouping_lines.append(line[3:])
            elif grouping_lines:
                # Flush the current grouping_lines before processing this non-group line
                ordered_list = alphabet_ordering(grouping_lines)
                unique_list = remove_duplicates(ordered_list)
                for oline in unique_list:
                    new_lines.append("- [" + oline)
                grouping_lines = []
                new_lines.append(line)
            else:
                new_lines.append(line)
        # Flush any remaining grouping_lines at end-of-file
        if grouping_lines:
            ordered_list = alphabet_ordering(grouping_lines)
            unique_list = remove_duplicates(ordered_list)
            for oline in unique_list:
                new_lines.append("- [" + oline)

    # Write the new content to {file_stem}_new.md
    new_file_path = f'../{file_stem}_new.md'
    with open(new_file_path, 'w', encoding='UTF-8') as f:
        for line in new_lines:
            f.write(line + '\n')

    # Read both files with preserved line endings for an accurate diff
    with open(old_file_path, 'r', encoding='UTF-8') as f:
        old_text = f.read()
        old_lines = old_text.splitlines(keepends=True)

    with open(new_file_path, 'r', encoding='UTF-8') as f:
        new_text = f.read()
        new_lines_for_diff = new_text.splitlines(keepends=True)

    # Generate unified diff (deleted lines are marked with a '-' sign)
    diff = list(difflib.unified_diff(
        old_lines,
        new_lines_for_diff,
        fromfile=f'{file_stem}.md',
        tofile=f'{file_stem}_new.md',
        lineterm=''
    ))

    # Alert the user to check the differences
    if diff:
        print(f"The difference between '{file_stem}.md' and '{file_stem}_new.md'. You can check the changes below:")
        print("\n".join(diff))

        # Confirm whether to update {file_stem}.md with the new file
        confirm = input(f"Do you want to update {file_stem}.md? [y]es/[n]o: ").strip().lower()
        if confirm.startswith('y'):
            # Replace {file_stem}.md with {file_stem}_new.md and remove the new file
            os.replace(new_file_path, old_file_path)
            print(f"{file_stem}.md updated successfully.")
        else:
            print("Update cancelled. The file {file_stem}_new.md remains available for review.")
    else:
        print(f"There is no difference between '{file_stem}.md' and '{file_stem}_new.md'. No re-odering is required.")
        os.remove(new_file_path)

order_md('README')
order_md('Learning')