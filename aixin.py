import tkinter as tk
import random
import math

# 温馨提示消息列表
messages = [
    "天冷了 多穿衣服", "你很棒", "所有烦恼都消失", "今天过得开心哦",
    "愿你平安喜乐", "勇敢一点", "一切都会好起来的", "保持微笑呀",
    "记得吃水果", "早点休息", "多喝水哦", "好好爱自己",
    "梦想成真", "万事如意", "少熬夜", "保持好心情",
    "你是独一无二的光", "金榜题名"
]

# 弹窗背景颜色列表
bg_colors = [
    "lightcoral", "lightpink", "lightblue", "lightgreen",
    "lightyellow", "lavender", "palevioletred", "skyblue",
    "honeydew", "mintcream", "aliceblue", "antiquewhite"
]

class LovePopupApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()  # 隐藏主窗口
        self.windows = []
        self.active_count = 0
        self.popup_creation_completed = False
        self.auto_close_scheduled = False
        self.is_animating = False
        self.heart_points = []
        self.message_index = 0

    def create_popup(self, x, y, message, bg_color):
        top = tk.Toplevel(self.root)
        top.overrideredirect(True)  # 去除窗口边框
        top.attributes('-topmost', True)  # 窗口置顶
        top.geometry(f"200x100+{x}+{y}")
        top.configure(bg=bg_color)

        label = tk.Label(top, text=message, font=("微软雅黑", 12), bg=bg_color, wraplength=180)
        label.pack(pady=10)

        # 关闭按钮
        def close_window():
            if self.popup_creation_completed and not self.auto_close_scheduled:
                self.start_animation()
            top.destroy()
            if top in self.windows:
                self.windows.remove(top)
            self.active_count -= 1

        close_btn = tk.Button(top, text="×", font=("微软雅黑", 10), bg=bg_color, command=close_window)
        close_btn.place(x=180, y=0)

        self.windows.append(top)
        self.active_count += 1
        return top

    def generate_random_popups(self, num_popups=50):
        self.popup_creation_completed = False
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        for _ in range(num_popups):
            x = random.randint(0, screen_width - 200)
            y = random.randint(0, screen_height - 100)
            msg = random.choice(messages)
            color = random.choice(bg_colors)
            self.create_popup(x, y, msg, color)
            self.root.after(100)  # 间隔创建弹窗
            self.root.update()

        self.popup_creation_completed = True

    def calculate_heart_points(self, center_x, center_y, size=100, num_points=len(messages)):
        points = []
        for i in range(num_points):
            t = i * 2 * math.pi / num_points
            x = center_x + size * 16 * math.sin(t) ** 3
            y = center_y - size * (13 * math.cos(t) - 5 * math.cos(2*t) - 2 * math.cos(3*t) - math.cos(4*t))
            points.append((int(x), int(y)))
        return points

    def start_animation(self):
        if self.is_animating:
            return
        self.is_animating = True
        center_x = self.root.winfo_screenwidth() // 2 - 100
        center_y = self.root.winfo_screenheight() // 2 - 50
        self.heart_points = self.calculate_heart_points(center_x, center_y)
        self.animate_heart(0)

    def animate_heart(self, index):
        if index >= len(self.windows) or index >= len(self.heart_points):
            self.fade_out(0)
            return

        win = self.windows[index]
        target_x, target_y = self.heart_points[index]
        current_x = win.winfo_x()
        current_y = win.winfo_y()

        # 移动弹窗
        step = 5
        if abs(current_x - target_x) > step:
            new_x = current_x + step if target_x > current_x else current_x - step
        else:
            new_x = target_x

        if abs(current_y - target_y) > step:
            new_y = current_y + step if target_y > current_y else current_y - step
        else:
            new_y = target_y

        win.geometry(f"200x100+{new_x}+{new_y}")
        self.root.after(10, lambda: self.animate_heart(index + 1))
        self.root.update()

    def fade_out(self, alpha):
        if alpha >= 1:
            self.root.destroy()
            return

        for win in self.windows:
            win.attributes('-alpha', 1 - alpha)
        self.root.after(50, lambda: self.fade_out(alpha + 0.05))
        self.root.update()

    def show_trigger_popup(self):
        trigger = tk.Toplevel(self.root)
        trigger.overrideredirect(True)
        trigger.attributes('-topmost', True)
        trigger.geometry("300x150+500+300")
        trigger.configure(bg="lightblue")

        label = tk.Label(trigger, text="每天都要保持好心情！", font=("微软雅黑", 14), bg="lightblue")
        label.pack(pady=20)

        def trigger_action():
            trigger.destroy()
            self.generate_random_popups()

        def reject_action():
            trigger.destroy()

        frame = tk.Frame(trigger, bg="lightblue")
        frame.pack(pady=10)

        tk.Button(frame, text="我不", font=("微软雅黑", 10), bg="lightcoral", command=reject_action).pack(side=tk.LEFT, padx=20)
        tk.Button(frame, text="收到！", font=("微软雅黑", 10), bg="lightgreen", command=trigger_action).pack(side=tk.LEFT, padx=20)

    def run(self):
        self.show_trigger_popup()
        self.root.mainloop()

if __name__ == "__main__":
    app = LovePopupApp()
    app.run()
