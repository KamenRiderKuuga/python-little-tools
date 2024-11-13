import tkinter as tk


class StickyNote:
    def __init__(self, root):
        self.root = root
        self.root.title("Sticky Note")
        self.root.geometry("200x200")
        self.root.attributes("-topmost", True)  # 固定在屏幕最前
        self.root.configure(bg="#FFFFE0")  # 浅黄色背景
        self.root.attributes("-alpha", 0.9)  # 设置透明度

        # 隐藏任务栏图标
        self.root.withdraw()  # 先隐藏窗口
        self.root.after(10, self.show_window)  # 短暂延迟后显示窗口

        self.text = tk.Text(
            self.root,
            wrap="word",
            bg="#FFFFE0",
            font=("微软雅黑", 10),
            bd=0,
            padx=5,
            pady=5,
        )
        self.text.pack(expand=True, fill="both")

        self.root.bind("<Control-s>", self.save_note)
    def show_window(self):
        self.root.deiconify()  # 显示窗口
        self.root.wm_attributes("-toolwindow", True)  # 移除任务栏图标
        self.root.protocol("WM_DELETE_WINDOW", lambda: None)

    def save_note(self, event=None):
        # 每次保存之前自动将以✔结尾的内容放置到最后
        text = self.text.get("1.0", tk.END)
        lines = text.split("\n")
        checked = []
        unchecked = []
        for line in lines:
            if not line:
                continue
            if line.endswith("✔"):
                checked.append(line)
            else:
                unchecked.append(line)

        self.text.delete("1.0", tk.END)
        self.text.insert("1.0", "\n".join(unchecked + [""] + checked))

        with open("note.txt", "w", encoding="utf-8") as file:
            file.write(self.text.get("1.0", tk.END))


if __name__ == "__main__":
    root = tk.Tk()
    note = StickyNote(root)
    try:
        with open("note.txt", "r", encoding="utf-8") as file:
            note.text.insert("1.0", file.read())
    except FileNotFoundError:
        pass
    root.mainloop()
