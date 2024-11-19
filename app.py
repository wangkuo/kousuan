from flask import Flask, render_template, request, jsonify
import random
from datetime import datetime

app = Flask(__name__)

VERSION = "1.0.1"  # 定义版本号

class MathProblemGenerator:
    def __init__(self):
        self.operators = {
            'add': '+',
            'subtract': '-',
            'multiply': '×',
            'divide': '÷'
        }
        self.generated_problems = set()  # 用于存储已生成的题目
    
    def generate_number(self, max_value):
        return random.randint(1, max_value)
    
    def check_carry(self, a, b):
        """检查加法是否需要进位"""
        return any(int(d1) + int(d2) > 9 for d1, d2 in zip(str(a).zfill(2), str(b).zfill(2)))
    
    def check_borrow(self, a, b):
        """检查减法是否需要退位"""
        return any(int(d1) < int(d2) for d1, d2 in zip(str(a).zfill(2), str(b).zfill(2)))
    
    def generate_teen_number(self):
        """生成十几的数字（11-19）"""
        return random.randint(11, 19)
    
    def generate_single_number(self):
        """生成个位数（1-9）"""
        return random.randint(1, 9)
    
    def generate_problem(self, max_value, operators, carry_enabled=False, 
                        borrow_enabled=False, num_count=2, blank_position=None,
                        teen_numbers=False):
        MAX_RETRIES = 100
        retry_count = 0
        
        while retry_count < MAX_RETRIES:
            try:
                numbers = []
                ops = []
                
                # 生成第一个数
                if teen_numbers:
                    numbers.append(self.generate_teen_number())
                else:
                    numbers.append(self.generate_number(max_value))
                
                # 生成运算符和后续数字
                for i in range(num_count - 1):
                    op = random.choice(operators)
                    ops.append(op)
                    
                    retry_inner = 0
                    while retry_inner < MAX_RETRIES:
                        if teen_numbers:
                            next_num = self.generate_single_number()
                        else:
                            next_num = self.generate_number(max_value)
                        
                        # 验证数字是否满足条件
                        if self.validate_number(op, numbers[-1], next_num, max_value, 
                                           carry_enabled, borrow_enabled, teen_numbers):
                            numbers.append(next_num)
                            break
                        retry_inner += 1
                    
                    if retry_inner >= MAX_RETRIES:
                        raise ValueError("无法生成满足条件的数字")
                
                # 计算结果
                result = numbers[0]
                for i, op in enumerate(ops):
                    if op == '+':
                        result += numbers[i + 1]
                    elif op == '-':
                        result -= numbers[i + 1]
                    elif op == '×':
                        result *= numbers[i + 1]
                    elif op == '÷':
                        result //= numbers[i + 1]
                
                # 验证结果是否在范围内
                if result <= max_value and result >= 0:
                    problem_str = self.format_problem(numbers, ops, result, blank_position)['problem']
                    
                    # 检查题目是否重复
                    if problem_str not in self.generated_problems:
                        self.generated_problems.add(problem_str)  # 添加到已生成题目集合
                        return self.format_problem(numbers, ops, result, blank_position)
                
            except Exception as e:
                print(f"生成题目时出错: {str(e)}")
            
            retry_count += 1
        
        raise ValueError("无法生成满足条件的题目")

    def validate_number(self, op, current_num, next_num, max_value, carry_enabled, borrow_enabled, teen_numbers=False):
        if teen_numbers:
            if op == '+':
                result = current_num + next_num
                # 确保结果不超过20且不需要进位
                return result <= 20 and (current_num % 10 + next_num) < 10
            elif op == '-':
                result = current_num - next_num
                # 确保结果仍然是十几且不需要退位
                return result >= 10 and (current_num % 10) >= next_num
            return False
        
        # 原有的验证逻辑
        if op == '+':
            if carry_enabled:
                return self.check_carry(current_num, next_num)
            return (current_num + next_num) <= max_value
        elif op == '-':
            if borrow_enabled:
                return self.check_borrow(current_num, next_num)
            return (current_num - next_num) >= 0
        elif op == '×':
            return (current_num * next_num) <= max_value
        elif op == '÷':
            return next_num != 0 and current_num % next_num == 0
        return False

    def format_problem(self, numbers, ops, result, blank_position):
        problem_parts = []
        for i in range(len(numbers)):
            if i == blank_position:
                problem_parts.append('()')
            else:
                problem_parts.append(str(numbers[i]))
            if i < len(ops):
                problem_parts.append(ops[i])
        problem_parts.append('=')
        
        if blank_position is not None:
            problem_parts.append(str(result))
            answer = numbers[blank_position]
        else:
            answer = result
            
        return {
            'problem': ' '.join(problem_parts),
            'answer': answer
        }

@app.route('/')
def index():
    return render_template('index.html', version=VERSION)  # 将版本号传递给模板

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.get_json()
        
        # 获取参数
        max_value = int(data['range'])
        operators = []
        if data['add']: operators.append('+')
        if data['subtract']: operators.append('-')
        if data['multiply']: operators.append('×')
        if data['divide']: operators.append('÷')
        
        if not operators:
            return jsonify({
                'error': '请至少选择一种运算类型'
            }), 400
        
        generator = MathProblemGenerator()
        problems = []
        
        # 获取是否生成十几加减几的题目
        teen_numbers = data.get('teen_numbers', False)
        
        # 生成题目
        type1_count = int(data['type1_count'])
        type2_count = int(data['type2_count'])
        total_problems = type1_count + type2_count
        
        if total_problems <= 0:
            return jsonify({
                'error': '请设置题目数量'
            }), 400
            
        # 生成两数运算题目
        for _ in range(type1_count):
            blank_position = None
            if random.random() < float(data['type1_blank_ratio']):
                blank_position = random.randint(0, 1)
            problem = generator.generate_problem(
                max_value=max_value,
                operators=operators,
                carry_enabled=data['carry'],
                borrow_enabled=data['borrow'],
                num_count=2,
                blank_position=blank_position,
                teen_numbers=teen_numbers
            )
            problems.append(problem)
        
        # 生成三数运算题目
        for _ in range(type2_count):
            blank_position = None
            if random.random() < float(data['type2_blank_ratio']):
                blank_position = random.randint(0, 2)
            problem = generator.generate_problem(
                max_value=max_value,
                operators=operators,
                carry_enabled=data['carry'],
                borrow_enabled=data['borrow'],
                num_count=3,
                blank_position=blank_position,
                teen_numbers=teen_numbers
            )
            problems.append(problem)
        
        return jsonify({
            'problems': problems,
            'total_problems': total_problems  # 返回题目数量
        })
        
    except Exception as e:
        return jsonify({
            'error': f'生成题目时出错: {str(e)}'
        }), 500

if __name__ == '__main__':
    app.run(debug=True) 