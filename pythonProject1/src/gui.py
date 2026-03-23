import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import random
import re
from shell_sort import shell_sort
from database import save_array, get_user_arrays, init_db, get_db
from auth import register_user, login_user


class ShellSortApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Сортировка Шелла")
        self.root.geometry("800x600")

        self.current_user = None
        self.current_user_id = None

        # Инициализируем атрибуты
        self.login_entry = None
        self.password_entry = None
        self.original_text = None
        self.sorted_text = None
        self.history_list = None

        # Создаем строку статуса
        self.status_bar = ttk.Label(self.root, text="Готов к работе", relief=tk.SUNKEN)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Создаем интерфейс
        self.create_login_frame()

    def create_login_frame(self):
        """Экран входа/регистрации"""
        self.clear_window()

        frame = ttk.Frame(self.root, padding="20")
        frame.pack(expand=True)

        ttk.Label(frame, text="Вход в систему", font=("Arial", 16)).pack(pady=10)

        ttk.Label(frame, text="Логин:").pack()
        self.login_entry = ttk.Entry(frame)
        self.login_entry.pack(pady=5)

        ttk.Label(frame, text="Пароль:").pack()
        self.password_entry = ttk.Entry(frame, show="*")
        self.password_entry.pack(pady=5)

        button_frame = ttk.Frame(frame)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Войти", command=self.login).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Регистрация", command=self.register).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Справка", command=self.show_help).pack(side=tk.LEFT, padx=5)

    def create_main_frame(self):
        """Главный экран приложения"""
        self.clear_window()

        # Верхняя панель с информацией о пользователе
        top_frame = ttk.Frame(self.root, padding="10")
        top_frame.pack(fill=tk.X)

        ttk.Label(top_frame, text=f"Пользователь: {self.current_user}").pack(side=tk.LEFT)
        ttk.Button(top_frame, text="Выйти", command=self.logout).pack(side=tk.RIGHT)

        # Основная панель
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Левая панель - ввод и сортировка
        left_frame = ttk.LabelFrame(main_frame, text="Работа с массивом", padding="10")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        # Подсказка для пользователя
        ttk.Label(left_frame, text="Введите числа через пробел в поле ниже:").pack(anchor=tk.W)

        # Поле для ввода/редактирования исходного массива
        ttk.Label(left_frame, text="Исходный массив:").pack(anchor=tk.W, pady=(10, 0))
        self.original_text = scrolledtext.ScrolledText(left_frame, height=5, font=("Courier", 10))
        self.original_text.pack(fill=tk.BOTH, expand=True, pady=5)

        # Кнопки управления
        button_frame = ttk.Frame(left_frame)
        button_frame.pack(pady=5)

        ttk.Button(button_frame, text="Случайный массив",
                   command=self.generate_random).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="Сортировать",
                   command=self.sort_array).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="Сохранить",
                   command=self.save_array).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="Очистить",
                   command=self.clear_arrays).pack(side=tk.LEFT, padx=2)

        # Поле для отсортированного массива
        ttk.Label(left_frame, text="Отсортированный массив:").pack(anchor=tk.W)
        self.sorted_text = scrolledtext.ScrolledText(left_frame, height=5, font=("Courier", 10))
        self.sorted_text.pack(fill=tk.BOTH, expand=True, pady=5)

        # Правая панель - история
        right_frame = ttk.LabelFrame(main_frame, text="Сохраненные массивы", padding="10")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)

        # Создаем список с прокруткой
        list_frame = ttk.Frame(right_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.history_list = tk.Listbox(list_frame, height=20,
                                       yscrollcommand=scrollbar.set,
                                       font=("Courier", 9))
        self.history_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar.config(command=self.history_list.yview)

        # Привязываем событие выбора элемента
        self.history_list.bind('<<ListboxSelect>>', self.on_history_select)

        ttk.Button(right_frame, text="Обновить",
                   command=self.load_history).pack(pady=5)

        # Загружаем историю
        self.load_history()

    def clear_arrays(self):
        """Очистить поля ввода"""
        self.original_text.delete(1.0, tk.END)
        self.sorted_text.delete(1.0, tk.END)
        self.status_bar.config(text="Поля очищены")

    def show_help(self):
        """Показывает окно со справкой"""
        help_text = """
        ========== ИНСТРУКЦИЯ ПО ИСПОЛЬЗОВАНИЮ ==========

        1. Вход в систему:
           • Если у вас нет аккаунта - нажмите "Регистрация"
           • Введите логин и пароль
           • Нажмите "Войти"

        2. Работа с массивами:
           • Введите числа через пробел в поле "Исходный массив"
             Например: 5 2 8 1 9 3 7 4 6
           • Или нажмите "Случайный массив" для генерации
           • Нажмите "Сортировать" для сортировки (алгоритм Шелла)
           • Нажмите "Сохранить" для сохранения в БД
           • Нажмите "Очистить" для очистки полей

        3. Просмотр истории:
           • Справа отображаются сохраненные массивы
           • Нажмите на элемент для просмотра деталей
           • Нажмите "Обновить" для обновления списка

        4. Выход:
           • Нажмите "Выйти" для возврата на экран входа

        ========== О ПРОГРАММЕ ==========
        Алгоритм: Сортировка Шелла (Shellsort)
        Версия: 3.0 с графическим интерфейсом и БД
        """

        help_window = tk.Toplevel(self.root)
        help_window.title("Справка")
        help_window.geometry("600x500")

        text_area = scrolledtext.ScrolledText(help_window, wrap=tk.WORD,
                                              font=("Consolas", 10))
        text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        text_area.insert(tk.END, help_text)
        text_area.config(state=tk.DISABLED)

        ttk.Button(help_window, text="Закрыть",
                   command=help_window.destroy).pack(pady=5)

    def generate_random(self):
        """Генерация случайного массива"""
        try:
            size = random.randint(5, 15)
            array = [random.randint(-50, 50) for _ in range(size)]
            self.original_text.delete(1.0, tk.END)
            self.original_text.insert(1.0, ' '.join(map(str, array)))
            self.sorted_text.delete(1.0, tk.END)
            self.status_bar.config(text=f"Сгенерирован массив из {size} элементов")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def sort_array(self):
        """Сортировка массива"""
        try:
            text = self.original_text.get(1.0, tk.END).strip()
            if not text:
                messagebox.showwarning("Предупреждение", "Введите массив или сгенерируйте случайный")
                return

            array = list(map(int, text.split()))

            if len(array) == 0:
                messagebox.showwarning("Предупреждение", "Массив не может быть пустым")
                return

            sorted_array = shell_sort(array)

            self.sorted_text.delete(1.0, tk.END)
            self.sorted_text.insert(1.0, ' '.join(map(str, sorted_array)))
            self.status_bar.config(text=f"Массив отсортирован. Размер: {len(array)}")

        except ValueError:
            messagebox.showerror("Ошибка", "Некорректный ввод. Используйте целые числа через пробел")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def save_array(self):
        """Сохранить массив в БД"""
        if not self.current_user_id:
            messagebox.showwarning("Предупреждение", "Сначала войдите в систему")
            return

        try:
            original_text = self.original_text.get(1.0, tk.END).strip()
            sorted_text = self.sorted_text.get(1.0, tk.END).strip()

            if not original_text:
                messagebox.showwarning("Предупреждение", "Нет исходного массива")
                return

            if not sorted_text:
                messagebox.showwarning("Предупреждение", "Сначала отсортируйте массив")
                return

            original = list(map(int, original_text.split()))
            sorted_arr = list(map(int, sorted_text.split()))

            save_array(self.current_user_id, original, sorted_arr)
            messagebox.showinfo("Успех", "Массив сохранен")
            self.load_history()
            self.status_bar.config(text="Массив успешно сохранен в БД")

        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def load_history(self):
        """Загрузить историю массивов пользователя"""
        if not self.current_user_id:
            return

        try:
            arrays = get_user_arrays(self.current_user_id)
            self.history_list.delete(0, tk.END)

            for arr in arrays:
                date_str = arr['created_at'][:16] if arr['created_at'] else "неизвестно"
                display = f"{date_str} | Размер: {arr['size']:3d} | ID: {arr['id']:3d}"
                self.history_list.insert(tk.END, display)

            if len(arrays) == 0:
                self.history_list.insert(tk.END, "Нет сохраненных массивов")

        except Exception as e:
            self.status_bar.config(text=f"Ошибка загрузки истории: {e}")

    def on_history_select(self, _event):
        """Обработка выбора элемента из истории"""
        selection = self.history_list.curselection()
        if not selection:
            return

        try:
            item_text = self.history_list.get(selection[0])
            if "Нет сохраненных" in item_text:
                return

            match = re.search(r'ID:\s*(\d+)', item_text)
            if not match:
                return

            array_id = int(match.group(1))

            with get_db() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT original_array, sorted_array 
                    FROM arrays 
                    WHERE id = ? AND user_id = ?
                ''', (array_id, self.current_user_id))

                row = cursor.fetchone()
                if row:
                    self.original_text.delete(1.0, tk.END)
                    self.original_text.insert(1.0, row['original_array'])

                    self.sorted_text.delete(1.0, tk.END)
                    self.sorted_text.insert(1.0, row['sorted_array'])

                    self.status_bar.config(text=f"Загружен массив ID: {array_id}")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить массив: {e}")

    def login(self):
        """Авторизация"""
        username = self.login_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showwarning("Предупреждение", "Заполните все поля")
            return

        success, result = login_user(username, password)

        if success:
            self.current_user = username
            self.current_user_id = result
            self.create_main_frame()
        else:
            messagebox.showerror("Ошибка", result)

    def register(self):
        """Регистрация"""
        username = self.login_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showwarning("Предупреждение", "Заполните все поля")
            return

        if len(password) < 4:
            messagebox.showwarning("Предупреждение", "Пароль должен быть не менее 4 символов")
            return

        success, message = register_user(username, password)

        if success:
            messagebox.showinfo("Успех", message)
        else:
            messagebox.showerror("Ошибка", message)

    def logout(self):
        """Выход из системы"""
        self.current_user = None
        self.current_user_id = None
        self.create_login_frame()

    def clear_window(self):
        """Очистить окно"""
        for widget in self.root.winfo_children():
            if widget != self.status_bar:
                widget.destroy()


def main():
    """Запуск приложения"""
    root = tk.Tk()
    init_db()
    ShellSortApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
