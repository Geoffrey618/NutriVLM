import os
import json
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import pandas as pd

# 加载DishWeight.xlsx数据
dish_weight_df = pd.read_excel('DishWeight.xlsx')

# 假设Excel文件中的列名分别是 '更正菜品名', '称重/g', 和 '营养分析'
dish_name_col = '菜品名'
weight_col = '称重/g'
nutrition_col = '营养分析'

# 问题模板
image_recognition_questions_single = [
    "图中有哪道菜？",
    "这幅图里展示了什么食物？",
    "请告诉我图片里的菜品。",
    "图片中显示的是哪种菜？",
    "图里有哪种食物？",
    "这张图片里有什么菜？",
    "你能识别出图中的食物吗？",
    "这张图里有哪道菜？",
    "请列出图片中的菜品。",
    "图中的食物是什么？"
]

image_recognition_questions_multiple = [
    "图中有哪些菜肴？",
    "请告诉我图片里的所有菜品。",
    "这张图片里展示了哪些菜？",
    "图中显示了什么食物？",
    "这幅图里有哪些菜品？",
    "能识别出图片中的菜肴吗？",
    "图里有几种食物？",
    "请列出图中的菜肴。",
    "这张图片中有哪些菜？",
    "图中的菜品有哪些？"
]

weight_questions_single = [
    "图中的菜肴重多少克？",
    "这道菜的重量是多少？",
    "请告诉我图片里这道菜的重量。",
    "这张图片里的菜有多重？",
    "能估算一下图中这道菜的重量吗？",
    "请问这道菜的重量是多少？",
    "图里这道菜有多重？",
    "这道菜各重多少克？",
    "请计算出图中这道菜的重量。",
    "图中的这道菜有多少克？"
]

weight_questions_multiple = [
    "图中的菜肴分别重多少克？",
    "图中的菜品各自有多重？",
    "每道菜的重量是多少？",
    "这些菜的重量分别是多少克？",
    "请告诉我图中每道菜的重量。",
    "图中的菜肴重量各是多少？",
    "每道菜分别有多重？",
    "能估算图中每道菜的重量吗？",
    "这张图里的菜各重多少？",
    "请问这些菜的重量是多少？"
]

nutrition_questions_single = [
    "图中的菜肴有什么营养价值？",
    "这道菜的营养成分是什么？",
    "请分析图中这道菜的营养成分。",
    "这道菜的营养价值如何？",
    "图中这道菜有哪些营养素？",
    "能告诉我这道菜的营养价值吗？",
    "请告诉我图中这道菜的营养成分。",
    "能分析图中这道菜的营养成分吗？",
    "图里的这道菜含有哪些营养成分？",
    "这道菜的营养价值是什么？"
]

nutrition_questions_multiple = [
    "图中的菜肴有什么营养价值？",
    "每道菜的营养成分是什么？",
    "这些菜肴的营养价值如何？",
    "请分析图中菜肴的营养成分。",
    "这些菜分别有哪些营养素？",
    "图中菜肴的营养价值是什么？",
    "请告诉我图中每道菜的营养成分。",
    "能分析图中菜的营养价值吗？",
    "这些菜的营养成分各是什么？",
    "图中的菜肴有哪些营养成分？"
]

assistant_prefixes = ["图中有", "图片中的菜品是", "如图有", "桌子上有", "如图，桌子上有", "桌子上摆放着", "图里有", "如图所示，有"]
weight_connectors = ["重", "为", "是", "的重量是", "约重", "的重量大约是", "大约为", "大约重", "的重量为"]

class AnnotationTool:
    def __init__(self, master):
        self.master = master
        self.master.title("JSON标注工具")

        # 加载并更新JSON数据
        self.data = self.load_and_update_json('Task2TrainingSet.json', 'images')
        self.current_index = 0

        # 创建界面控件
        self.create_widgets()
        # 显示当前图片和问题
        self.display_image()

    def load_and_update_json(self, json_file, image_dir):
        # 加载现有的JSON数据
        if os.path.exists(json_file):
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            data = []

        # 获取JSON中已有的图片列表
        existing_images = {entry['image'][0] for entry in data}

        # 检查目录中的新图片
        all_images = {os.path.join(image_dir, f) for f in os.listdir(image_dir) if f.endswith(('.jpg', '.JPG', '.png', ',PNG'))}
        new_images = all_images - existing_images

        # 将新图片添加到JSON数据中
        for image in new_images:
            entry = {
                "image": [image],
                "messages": [
                    {"role": "user", "content": ""},
                    {"role": "assistant", "content": ""},
                    {"role": "user", "content": ""},
                    {"role": "assistant", "content": ""},
                    {"role": "user", "content": ""},
                    {"role": "assistant", "content": ""}
                ]
            }
            data.append(entry)

        # 保存更新后的JSON数据
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        return data

    def save_json(self):
        # 保存JSON数据
        with open('Task2TrainingSet.json', 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def create_widgets(self):
        # 图片路径标签
        self.image_path_label = tk.Label(self.master, text="", font=('Arial', 10, 'italic'))
        self.image_path_label.pack(pady=5)

        # 图片标签
        self.image_label = tk.Label(self.master)
        self.image_label.pack(pady=5)

        # 进度框架
        progress_frame = tk.Frame(self.master)
        progress_frame.pack(pady=5)

        # 当前进度标签
        self.progress_label = tk.Label(progress_frame, text="", font=('Arial', 12, 'bold'))
        self.progress_label.pack(side=tk.LEFT, padx=5)

        # 跳转至第n张图片的输入框
        self.progress_entry = tk.Entry(progress_frame, font=('Arial', 12, 'bold'), width=7, justify='center')
        self.progress_entry.pack(side=tk.LEFT, padx=5)

        # 跳转按钮
        self.jump_button = tk.Button(progress_frame, text="跳转", bg='lightpink', command=self.jump_to_image,
                                     font=('Arial', 12, 'bold'))
        self.jump_button.pack(side=tk.LEFT, padx=5)

        # 问题标签
        self.question_label = tk.Label(self.master, text="请输入当前图中所含菜品编号（空格分隔）",
                                       font=('Arial', 12, 'bold'))
        self.question_label.pack(pady=5)

        # 问题文本框
        self.question_text = tk.Entry(self.master, font=('Arial', 12))
        self.question_text.pack(padx=5, pady=5)
        self.question_text.bind("<Return>", lambda event: self.save_entry())

        # 按钮框架
        button_frame = tk.Frame(self.master)
        button_frame.pack(pady=10)

        # 按钮配置
        button_config = {
            "font": ('Arial', 12, 'bold'),
            "height": 2,
            "width": 15,
        }

        # 保存按钮
        self.save_button = tk.Button(button_frame, text="保存修改", command=self.save_entry, bg='lightblue', fg='black',
                                     **button_config)
        self.save_button.grid(row=0, column=0, padx=5)

        # 上一张按钮
        self.prev_button = tk.Button(button_frame, text="上一张", command=self.prev_image, bg='lightgreen', fg='black',
                                     **button_config)
        self.prev_button.grid(row=0, column=1, padx=5)

        # 下一张按钮
        self.next_button = tk.Button(button_frame, text="下一张", command=self.next_image, bg='lightgreen', fg='black',
                                     **button_config)
        self.next_button.grid(row=0, column=2, padx=5)

        # 退出按钮
        self.exit_button = tk.Button(button_frame, text="退出", command=self.exit_tool, bg='red', fg='white',
                                     **button_config)
        self.exit_button.grid(row=0, column=3, padx=5)

    def display_image(self):
        # 显示当前图片和问题
        if self.data:
            entry = self.data[self.current_index]
            image_path = entry['image'][0]
            img = Image.open(image_path)
            img = img.resize((400, 300), Image.Resampling.LANCZOS)
            img = ImageTk.PhotoImage(img)
            self.image_label.config(image=img)
            self.image_label.image = img

            # 更新图片路径标签
            self.image_path_label.config(text=f"当前文件：{image_path}", font=('Arial', 12, 'bold'))

            # 更新进度标签
            self.progress_label.config(text=f"正在处理图片 {self.current_index + 1} / {len(self.data)}")

    def save_entry(self):
        numbers_str = self.question_text.get().strip()
        if not numbers_str:
            messagebox.showwarning("警告", "请输入有效的菜品编号！")
            return

        numbers = list(map(int, numbers_str.split()))
        entry = self.data[self.current_index]

        if len(numbers) == 1:
            question = random.choice(image_recognition_questions_single)
            weight_question = random.choice(weight_questions_single)
            nutrition_question = random.choice(nutrition_questions_single)
        else:
            question = random.choice(image_recognition_questions_multiple)
            weight_question = random.choice(weight_questions_multiple)
            nutrition_question = random.choice(nutrition_questions_multiple)

        entry['messages'][0]['content'] = question
        entry['messages'][2]['content'] = weight_question
        entry['messages'][4]['content'] = nutrition_question

        dish_names = "，".join([dish_weight_df.iloc[num - 1][dish_name_col].replace(" ", "") for num in numbers])
        prefix = random.choice(assistant_prefixes)
        entry['messages'][1]['content'] = f"{prefix}{dish_names}。"

        weights = "，".join([
            f"{dish_weight_df.iloc[num - 1][dish_name_col].replace(' ', '')}{random.choice(weight_connectors)}{dish_weight_df.iloc[num - 1][weight_col]}克"
            for num in numbers])
        entry['messages'][3]['content'] = weights.replace(" ", "") + "。"

        nutrition = "\n".join([dish_weight_df.iloc[num - 1][nutrition_col].replace(" ", "") for num in numbers])
        entry['messages'][5]['content'] = nutrition.replace(" ", "")

        self.save_json()
        self.question_text.delete(0, tk.END)
        self.next_image()

    def prev_image(self):
        # 显示上一张图片
        if self.current_index > 0:
            self.current_index -= 1
            self.display_image()

    def next_image(self):
        # 显示下一张图片
        if self.current_index < len(self.data) - 1:
            self.current_index += 1
            self.display_image()

    def jump_to_image(self):
        # 跳转至指定图片
        try:
            index = int(self.progress_entry.get()) - 1
            if 0 <= index < len(self.data):
                self.current_index = index
                self.display_image()
            else:
                messagebox.showwarning("警告", "输入的数字超出范围！")
        except ValueError:
            messagebox.showwarning("警告", "请输入有效的数字！")

    def exit_tool(self):
        # 退出工具并保存数据
        self.save_json()
        self.master.quit()


if __name__ == "__main__":
    root = tk.Tk()
    app = AnnotationTool(root)
    root.mainloop()