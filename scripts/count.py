import os
import argparse
from collections import defaultdict


def count_coordinate_templates(coordinates_dir="src/config/coordinates"):
    if not os.path.exists(coordinates_dir):
        print(f"❌ Directory not found: {coordinates_dir}")
        return

    total_files = 0
    bank_data = {}

    for bank_name in os.listdir(coordinates_dir):
        bank_path = os.path.join(coordinates_dir, bank_name)
        if os.path.isdir(bank_path):
            files_in_bank = [
                f
                for f in os.listdir(bank_path)
                if os.path.isfile(os.path.join(bank_path, f))
            ]
            file_count = len(files_in_bank)
            template_count = file_count // 2

            # Count extensions (excluding .json)
            extension_count_by_bank = defaultdict(int)
            for file in files_in_bank:
                _, ext = os.path.splitext(file)
                if ext and ext.lower() != ".json":
                    extension_count_by_bank[ext.lower()] += 1

            bank_data[bank_name] = {
                "files": file_count,
                "templates": template_count,
                "extensions": dict(extension_count_by_bank),
            }
            total_files += file_count

    total_templates = total_files // 2

    print(f"\n{'=' * 60}")
    print("📊 COORDINATE TEMPLATES COUNT")
    print(f"{'=' * 60}")

    for bank in sorted(bank_data.keys()):
        data = bank_data[bank]
        print(
            f"🏦 {bank:<20} : {data['templates']:>3} template(s) ({data['files']} files)"
        )

        if data["extensions"]:
            for ext in sorted(data["extensions"].keys()):
                count = data["extensions"][ext]
                percentage = (count / data["files"] * 100) if data["files"] > 0 else 0
                print(f"   📄 {ext:<14} : {count:>3} file(s) ({percentage:>5.1f}%)")

    print(f"{'-' * 60}")
    print(f"📊 Total: {total_templates} template(s)")
    print(f"🏦 Banks: {len(bank_data)}")
    print(f"{'=' * 60}\n")


def analyze_hierarchical_structure(root_path):
    extension_count = defaultdict(int)
    user_count = defaultdict(lambda: defaultdict(int))
    bank_count = defaultdict(lambda: defaultdict(int))

    real_path = os.path.realpath(root_path)

    if not os.path.exists(real_path):
        print(f"error: The path '{real_path}' does not exist.")
        return None

    if not os.path.isdir(real_path):
        print(f"error: The path '{real_path}' is not a directory.")
        return None

    total_files = 0

    try:
        for root, dirs, files in os.walk(real_path, followlinks=True):
            rel_path = os.path.relpath(root, real_path)

            if rel_path == ".":
                continue

            path_parts = rel_path.split(os.sep)

            if len(path_parts) >= 2:
                user = path_parts[0]
                bank = path_parts[1]

                for file in files:
                    total_files += 1
                    _, extension = os.path.splitext(file)

                    if not extension:
                        extension = "no_extension"
                    else:
                        extension = extension[1:].lower()

                    extension_count[extension] += 1
                    user_count[user][bank] += 1
                    bank_count[bank][extension] += 1
    except Exception as e:
        print(f"❌ system error: {e}")
        return None

    return {
        "extension_count": dict(extension_count),
        "user_count": dict(user_count),
        "bank_count": dict(bank_count),
        "total_files": total_files,
    }


def print_general_report(data):
    extension_count = data["extension_count"]
    total_files = data["total_files"]

    print("\n" + "=" * 60)
    print("📊 GENERAL REPORT - TOTAL BY EXTENSION")
    print("=" * 60)

    sorted_extensions = sorted(extension_count.items())

    for extension, count in sorted_extensions:
        percentage = (count / total_files * 100) if total_files > 0 else 0
        print(f"📄 .{extension:<15} : {count:>5} file(s) ({percentage:>5.1f}%)")

    print("-" * 60)
    print(f"📊 Total files: {total_files:>5}")
    print()


def print_user_report(data):
    user_count = data["user_count"]
    total_files = data["total_files"]

    print("\n" + "=" * 60)
    print("👤 REPORT BY USER")
    print("=" * 60)

    for user in sorted(user_count.keys()):
        banks = user_count[user]
        user_total = sum(banks.values())
        user_percentage = (user_total / total_files * 100) if total_files > 0 else 0

        print(f"\n👤 {user.upper()}: {user_total} file(s) ({user_percentage:.1f}%)")

        for bank in sorted(banks.keys()):
            count = banks[bank]
            bank_percentage = (count / user_total * 100) if user_total > 0 else 0
            print(f"   🏦 {bank:<15} : {count:>3} file(s) ({bank_percentage:>5.1f}%)")
    print()


def print_bank_report(data):
    bank_count = data["bank_count"]
    total_files = data["total_files"]

    print("\n" + "=" * 60)
    print("🏦 REPORT BY BANK")
    print("=" * 60)

    bank_totals = {}
    for bank, extensions in bank_count.items():
        bank_totals[bank] = sum(extensions.values())

    for bank in sorted(bank_totals.keys(), key=lambda x: bank_totals[x], reverse=True):
        extensions = bank_count[bank]
        bank_total = bank_totals[bank]
        bank_percentage = (bank_total / total_files * 100) if total_files > 0 else 0

        print(f"\n🏦 {bank.upper()}: {bank_total} file(s) ({bank_percentage:.1f}%)")

        for extension in sorted(extensions.keys()):
            count = extensions[extension]
            ext_percentage = (count / bank_total * 100) if bank_total > 0 else 0
            print(
                f"   📄 .{extension:<12} : {count:>3} file(s) ({ext_percentage:>5.1f}%)"
            )
    print()


def print_summary(data):
    user_count = data["user_count"]
    bank_count = data["bank_count"]
    total_files = data["total_files"]

    print("\n" + "=" * 60)
    print("📋 EXECUTIVE SUMMARY")
    print("=" * 60)
    print(f"📊 Total files: {total_files}")
    print(f"👥 Total users: {len(user_count)}")
    print(f"🏦 Total banks: {len(bank_count)}")
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="Hierarchical analysis of receipts by user and bank",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
            Expected structure: root_folder/user/bank/files

            Usage examples:
                python count.py
                python count.py -i /path/to/receipts
        """,
    )

    parser.add_argument(
        "-i",
        "--input",
        default="dataset",
        help="Input path to root folder (default: dataset)",
    )

    args = parser.parse_args()
    root_path = os.path.abspath(args.input)
    print(f"🔍 Analyzing hierarchical structure at: {root_path}")

    count_coordinate_templates()

    data = analyze_hierarchical_structure(root_path)

    if not data or data["total_files"] == 0:
        return

    print_summary(data)
    print_general_report(data)
    print_user_report(data)
    print_bank_report(data)


if __name__ == "__main__":
    main()
