# main.py

from mylibrary.library import Library

library = Library()

def menu():
    print("\n--- سیستم مدیریت کتابخانه ---")
    print("1. اضافه کردن کتاب")
    print("2. حذف کتاب")
    print("3. جستجوی کتاب")
    print("4. نمایش همه کتاب‌ها")
    print("5. خروج")

if __name__ == "__main__":
    while True:
        menu()
        choice = input("یک گزینه انتخاب کنید: ")

        if choice == "1":
            title = input("عنوان کتاب: ")
            author = input("نویسنده: ")
            library.add_book(title, author)
            print("کتاب اضافه شد.")

        elif choice == "2":
            title = input("عنوان کتاب برای حذف: ")
            if library.remove_book(title):
                print("کتاب حذف شد.")
            else:
                print("کتاب یافت نشد.")

        elif choice == "3":
            title = input("عنوان کتاب برای جستجو: ")
            result = library.search_book(title)
            if result:
                print(f"پیدا شد: {result['title']} - {result['author']}")
            else:
                print("کتاب یافت نشد.")

        elif choice == "4":
            library.show_books()

        elif choice == "5":
            print("خروج...")
            break

        else:
            print("گزینه اشتباه است. دوباره تلاش کنید.")
