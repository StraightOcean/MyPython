import tkinter as tk
from tkinter import ttk, messagebox
import random

class LotteryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("点名程序")
        self.root.geometry("600x450")  # 增大窗口尺寸

        # 设置应用图标 (请替换为实际图标路径)
        try:
            self.root.iconbitmap('bin/image/Logo_Mr.X.ico')  # 请替换为实际图标路径
        except tk.TclError:
            # 如果图标文件不存在，则跳过设置
            pass

        # 设置窗口始终置顶
        self.root.attributes('-topmost', True)

        # 绑定窗口状态改变事件，检测最小化
        self.root.bind('<Unmap>', self.on_minimize)

        # 使主窗口居中显示
        self.center_window(self.root, 600, 450)

        # 示例数据 - 可以根据需要修改
        self.data = [
            ["从前往后数第1个", "从前往后数第2个", "从前往后数第3个", "从前往后数第4个", "从前往后数第5个"],
            ["从门口往内数第1个", "从门口往内数第2个", "从门口往内数第3个", "从门口往内数第4个", "从门口往内数第5个", "从门口往内数第6个", "从门口往内数第7个", "从门口往内数第8个"]
        ]
        # 创建8行，每行都是第一个子列表的数据
        self.data_rows = [self.data[0] for _ in range(8)]
        # 创建5列，每列都是第二个子列表的数据
        self.data_cols = [self.data[1] for _ in range(5)]

        # 记录每行/列剩余可选的元素
        self.available_rows = [row[:] for row in self.data_rows]  # 深拷贝每行数据
        self.available_cols = [col[:] for col in self.data_cols]  # 深拷贝每列数据

        # 悬浮窗变量
        self.floating_window = None

        self.setup_main_menu()

    def center_window(self, window, width, height):
        """使窗口居中显示"""
        # 获取屏幕尺寸
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        # 计算窗口应放置的坐标
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        # 设置窗口位置
        window.geometry(f"{width}x{height}+{x}+{y}")

    def on_minimize(self, event=None):
        """当窗口最小化时触发"""
        if self.root.state() == 'iconic':  # 检查窗口是否是最小化状态
            self.create_floating_window()

    def create_floating_window(self):
        """创建悬浮窗"""
        if self.floating_window is not None and self.floating_window.winfo_exists():
            return  # 如果悬浮窗已经存在则不再创建

        self.floating_window = tk.Toplevel(self.root)
        self.floating_window.title("快速点名")

        # 设置悬浮窗为工具窗口（不在任务栏显示）
        self.floating_window.attributes('-toolwindow', True)
        self.floating_window.attributes('-topmost', True)  # 始终置顶

        # 设置悬浮窗大小和位置
        self.floating_window.geometry("150x50+100+100")
        self.floating_window.overrideredirect(True)  # 移除窗口边框

        # 创建悬浮窗内容框架
        float_frame = tk.Frame(self.floating_window, bg='#2C3E50', relief='raised', bd=2,
                               highlightbackground='#34495E', highlightthickness=2)
        float_frame.pack(fill='both', expand=True)

        # 悬浮窗图标（使用字符模拟）
        icon_label = tk.Label(float_frame, text="🎯", bg='#2C3E50', fg='white', font=('Arial', 12))
        icon_label.pack(side='left', padx=(10, 5), pady=5)

        # 悬浮窗标签
        float_label = tk.Label(float_frame, text=" 快速点名 ", bg='#2C3E50', fg='white',
                               font=('Arial', 10, 'bold'))
        float_label.pack(side='left', pady=5)

        # 按钮框架
        button_frame = tk.Frame(float_frame, bg='#2C3E50')
        button_frame.pack(side='right', padx=(0, 5), pady=5)

        # 恢复主窗口按钮
        restore_btn = tk.Button(button_frame, text="▲", command=self.restore_main_window,
                               width=3, height=1, bg='#3498DB', fg='white',
                               font=('Arial', 10, 'bold'), relief='flat', bd=0,
                               activebackground='#2980B9', activeforeground='white')
        restore_btn.pack(side='left', padx=2)

        # 关闭悬浮窗按钮
        close_btn = tk.Button(button_frame, text="×", command=self.close_floating_window,
                             width=3, height=1, bg='#E74C3C', fg='white',
                             font=('Arial', 10, 'bold'), relief='flat', bd=0,
                             activebackground='#C0392B', activeforeground='white')
        close_btn.pack(side='left', padx=2)

        # 使悬浮窗可拖动
        self.make_draggable(self.floating_window, float_frame)

    def make_draggable(self, window, widget):
        """使窗口可通过指定部件拖动"""
        widget.bind("<Button-1>", lambda e: self.start_move(window, e))
        widget.bind("<B1-Motion>", lambda e: self.do_move(window, e))

    def start_move(self, window, event):
        """开始移动窗口"""
        self.x = event.x
        self.y = event.y

    def do_move(self, window, event):
        """执行窗口移动"""
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = window.winfo_x() + deltax
        y = window.winfo_y() + deltay
        window.geometry(f"+{x}+{y}")

    def restore_main_window(self):
        """恢复主窗口"""
        if self.floating_window:
            self.floating_window.destroy()
            self.floating_window = None
        self.root.deiconify()  # 显示主窗口
        self.root.state('normal')  # 恢复正常状态

    def close_floating_window(self):
        """关闭悬浮窗并退出程序"""
        if self.floating_window:
            self.floating_window.destroy()
            self.floating_window = None
        self.root.destroy()

    def reset_lists(self):
        """重置点名列表"""
        # 重新初始化可用列表
        self.available_rows = [row[:] for row in self.data_rows]
        self.available_cols = [col[:] for col in self.data_cols]
        messagebox.showinfo("重置成功", "点名列表已重置，可以重新开始点名！")

    def setup_main_menu(self):
        """设置主菜单界面"""
        # 清空当前界面
        for widget in self.root.winfo_children():
            widget.destroy()

        title_label = tk.Label(self.root, text="点名程序", font=("Arial", 20))  # 增大字体
        title_label.pack(pady=30)  # 增加间距

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=50)  # 增加间距

        row_button = tk.Button(
            button_frame,
            text="按行点名",
            command=self.row_lottery_mode,
            width=25,  # 增加宽度
            height=3   # 增加高度
        )
        row_button.pack(pady=15)  # 增加间距

        col_button = tk.Button(
            button_frame,
            text="按列点名",
            command=self.column_lottery_mode,
            width=25,  # 增加宽度
            height=3   # 增加高度
        )
        col_button.pack(pady=15)  # 增加间距

        # 添加重置按钮
        reset_button = tk.Button(
            button_frame,
            text="重置点名列表",
            command=self.reset_lists,
            width=25,  # 增加宽度
            height=2,   # 增加高度
            bg='#F39C12',  # 橙色背景
            fg='white',
            font=('Arial', 12)
        )
        reset_button.pack(pady=15)  # 增加间距

    def row_lottery_mode(self):
        """按行点名模式"""
        # 清空当前界面
        for widget in self.root.winfo_children():
            widget.destroy()

        title_label = tk.Label(self.root, text="按行点名", font=("Arial", 20))  # 增大字体
        title_label.pack(pady=30)  # 增加间距

        # 行选择
        row_frame = tk.Frame(self.root)
        row_frame.pack(pady=15)  # 增加间距

        tk.Label(row_frame, text="选择行:", font=("Arial", 14)).pack(side=tk.LEFT, padx=15)  # 增大字体和间距
        self.selected_row = tk.StringVar(value="1")  # 使用StringVar，初始值为"1"
        # 设置行选择的最大值为数据行数，但内部处理时减1得到实际索引
        row_spinbox = tk.Spinbox(
            row_frame,
            from_=1,  # 从1开始
            to=len(self.data_rows),
            textvariable=self.selected_row,
            width=8,  # 增加宽度
            font=("Arial", 14)  # 增大字体
        )
        row_spinbox.pack(side=tk.LEFT, padx=15)  # 增加间距

        # 点名按钮
        draw_button = tk.Button(
            self.root,
            text="开始点名",
            command=self.draw_from_row,
            width=20,  # 增加宽度
            height=3   # 增加高度
        )
        draw_button.pack(pady=30)  # 增加间距

        # 返回主菜单按钮
        back_button = tk.Button(
            self.root,
            text="返回主菜单",
            command=self.setup_main_menu,
            width=20,  # 增加宽度
            height=2   # 增加高度
        )
        back_button.pack(pady=15)  # 增加间距

    def column_lottery_mode(self):
        """按列点名模式"""
        # 清空当前界面
        for widget in self.root.winfo_children():
            widget.destroy()

        title_label = tk.Label(self.root, text="按列点名", font=("Arial", 20))  # 增大字体
        title_label.pack(pady=30)  # 增加间距

        # 列选择
        col_frame = tk.Frame(self.root)
        col_frame.pack(pady=15)  # 增加间距

        tk.Label(col_frame, text="选择列:", font=("Arial", 14)).pack(side=tk.LEFT, padx=15)  # 增大字体和间距
        self.selected_col = tk.StringVar(value="1")  # 使用StringVar，初始值为"1"
        # 设置列选择的最大值为数据列数，但内部处理时减1得到实际索引
        col_spinbox = tk.Spinbox(
            col_frame,
            from_=1,  # 从1开始
            to=len(self.data_cols),
            textvariable=self.selected_col,
            width=8,  # 增加宽度
            font=("Arial", 14)  # 增大字体
        )
        col_spinbox.pack(side=tk.LEFT, padx=15)  # 增加间距

        # 点名按钮
        draw_button = tk.Button(
            self.root,
            text="开始点名",
            command=self.draw_from_column,
            width=20,  # 增加宽度
            height=3   # 增加高度
        )
        draw_button.pack(pady=30)  # 增加间距

        # 返回主菜单按钮
        back_button = tk.Button(
            self.root,
            text="返回主菜单",
            command=self.setup_main_menu,
            width=20,  # 增加宽度
            height=2   # 增加高度
        )
        back_button.pack(pady=15)  # 增加间距

    def draw_from_row(self):
        """从指定行抽取一人"""
        row_num = int(self.selected_row.get())  # 用户看到的行号（1-based）
        row_idx = row_num - 1  # 内部使用的索引（0-based）

        if row_idx < 0 or row_idx >= len(self.data_rows):
            messagebox.showerror("错误", f"行索引超出范围 (1-{len(self.data_rows)})")
            return

        # 获取当前行剩余可选的元素
        if not self.available_rows[row_idx]:
            messagebox.showwarning("提示", f"第{row_num}行的所有人都已被点名过！")
            return

        # 随机选择一个元素并移除它
        winner = random.choice(self.available_rows[row_idx])
        self.available_rows[row_idx].remove(winner)

        # 显示结果
        self.show_result(winner)

    def draw_from_column(self):
        """从指定列抽取一人"""
        col_num = int(self.selected_col.get())  # 用户看到的列号（1-based）
        col_idx = col_num - 1  # 内部使用的索引（0-based）

        if col_idx < 0 or col_idx >= len(self.data_cols):
            messagebox.showerror("错误", f"列索引超出范围 (1-{len(self.data_cols)})")
            return

        # 获取当前列剩余可选的元素
        if not self.available_cols[col_idx]:
            messagebox.showwarning("提示", f"第{col_num}列的所有人都已被点名过！")
            return

        # 随机选择一个元素并移除它
        winner = random.choice(self.available_cols[col_idx])
        self.available_cols[col_idx].remove(winner)

        # 显示结果
        self.show_result(winner)

    def show_result(self, winner):
        """显示点名结果"""
        result_window = tk.Toplevel(self.root)
        result_window.title("点名结果")
        result_window.geometry("400x200")  # 增大结果窗口尺寸
        result_window.resizable(False, False)

        # 设置结果窗口图标
        try:
            result_window.iconbitmap('icon.ico')  # 请替换为实际图标路径
        except tk.TclError:
            pass

        # 设置结果窗口始终置顶
        result_window.attributes('-topmost', True)

        # 使结果窗口居中显示
        self.center_window(result_window, 400, 200)

        # 居中显示
        result_window.transient(self.root)
        result_window.grab_set()

        tk.Label(result_window, text=f"恭喜！", font=("Arial", 24)).pack(pady=25)  # 增大字体和间距
        tk.Label(result_window, text=f"{winner}", font=("Arial", 28), fg="red").pack(pady=15)  # 增大字体和间距

        ok_button = tk.Button(
            result_window,
            text="确定",
            command=result_window.destroy,
            width=12,  # 增加宽度
            height=2   # 增加高度
        )
        ok_button.pack(pady=15)  # 增加间距

if __name__ == "__main__":
    root = tk.Tk()
    app = LotteryApp(root)
    root.mainloop()
