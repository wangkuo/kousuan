# 小学生口算题目生成器

这是一个专门为小学生设计的口算练习题目生成器。教师或家长可以根据学生的实际水平，灵活设置题目难度和类型。

## 功能特点

1. 数值范围选择
   - 10以内数值
   - 20以内数值
   - 50以内数值
   - 100以内数值

2. 运算类型选择
   - 加法（可选择是否包含进位）
   - 减法（可选择是否包含退位）
   - 乘法
   - 除法

3. 题型设置
   - 两数运算（如：1+2=）
   - 三数连续运算（如：1+2+3=）
   - 可设置每种题型的数量
   - 支持填空位置随机（如：1+()=3 或 1+2+()=6）

4. 排版功能
   - 整齐的题目布局
   - 包含日期、姓名、成绩栏
   - 适合打印的页面设计

## 使用方法

1. 启动程序：运行 `python app.py`
2. 访问：打开浏览器访问 `http://localhost:5000`
3. 设置参数：选择所需的题目参数
4. 生成试题：点击"生成试题"按钮
5. 打印：使用浏览器的打印功能打印试题

## 技术栈

- Python 3.11
- Flask
- HTML5
- CSS3
- JavaScript 