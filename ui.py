import tkinter as tk
from tkinter import messagebox
from main7 import Reverse, Se, is_LL1


def on_check_grammar():
    grammar, select_dict = parse_grammar(text_grammar.get("1.0", tk.END))
    print("select_dict: ", select_dict)
    VN, VT = get_VN_VT(grammar)
    is_ll1, first, follow, select, analysis_table = is_LL1(grammar, VN, VT, select_dict)

    if not is_ll1:
        messagebox.showinfo("Grammar Check", "该文法不是LL1文法")
    else:
        messagebox.showinfo("Grammar Check", "该文法是LL1文法")
        display_results(grammar, VN, VT, first, follow, select, analysis_table)


def display_results(grammar, VN, VT, first, follow, select, analysis_table):
    result_text = f"非终结符: {', '.join(VN)}\n"
    result_text += f"终结符: {', '.join(VT)}\n\n"
    # 输出first集
    result_text += "FIRST 集:\n"
    for vn in VN:
        result_text += f"FIRST({vn}) = {first[vn]}\n"
    # 输出follow集
    result_text += "\nFOLLOW 集:\n"
    for vn in VN:
        result_text += f"FOLLOW({vn}) = {follow[vn]}\n"
    # 输出select集
    result_text += "\nSELECT 集:\n"
    for vn in VN:
        for prod in grammar[vn]:
            result_text += f"SELECT({vn}->{prod}): {select[vn][prod]}\n"
    # 输出分析表
    VTn = VT[:]
    VTn.remove('ε')
    VTn.append('#')
    result_text += "\n分析表:\n"
    analysis_table = {nt: {term: '' for term in VTn} for nt in VN}
    for nt in VN:
        for prod in grammar[nt]:
            for term in select[nt][prod]:
                analysis_table[nt][term] = prod
    result_text += f" "
    result_text += ''.join(str(i).center(10) for i in VTn)
    result_text += "\n"
    for S in VN:
        result_text += S
        for item in VTn:
            if analysis_table[S][item] == '':
                result_text += 'err'.center(10)
            else:
                result_text += analysis_table[S][item].center(10)
        print()
        result_text += "\n"


    text_result.delete("1.0", tk.END)
    text_result.insert(tk.END, result_text)


def on_analyze_string():
    result_text = ""
    grammar, select = parse_grammar(text_grammar.get("1.0", tk.END))
    VN, VT = get_VN_VT(grammar)
    input_str = list(entry_string.get())

    input_str.append("#")
    count = 0
    S = ["#"]
    S.append(VN[0])

    VTn = VT[:]
    VTn.append('#')
    analysis_table = {nt: {term: '' for term in VTn} for nt in VN}
    for nt in VN:
        for prod in grammar[nt]:
            for term in select[nt][prod]:
                analysis_table[nt][term] = prod

    result_text += "步骤\t符号栈S[i]\t输入串str[j]\t产生式\t\t\t\t原因\n"
    while len(S) != 0:
        count += 1
        s0 = input_str[0]
        topS = S[-1]

        if topS == "#" and s0 == "#":
            result_text += f"{count}\t{''.join(S).center(10)}\t{''.join(input_str).center(10)}\t\tacc\t\t匹配成功，输入符号串是该文法的句子\n"
            break
        elif topS in VT and(s0 in VT or s0 == "#"):
            if topS == s0:
                result_text += f"{count}\t{''.join(S).center(10)}\t{''.join(input_str).center(10)}\t\t匹配弹出 {s0}\t\t终结符匹配\n"
                S.pop()
                input_str.pop(0)
            else:
                result_text += f"{count}\t{''.join(S).center(10)}\t{''.join(input_str).center(10)}\t\t错误\t\t\t\t终结符不匹配\n"
                result_text += '该符号串不是该文法的句子'
                break
        elif topS in VN and(s0 in VT or s0 == "#"):
            print("topS in the VN now, topS is: ", topS)
            print("s0 is: ", s0)
            prod = analysis_table[topS][s0]
            if prod:
                result_text += f"{count}\t{''.join(S).center(10)}\t{''.join(input_str).center(10)}\t\t{topS}->{prod}\t\t根据分析表选择产生式\n"
                S.pop()
                if prod != 'ε':
                    S.extend(Reverse(prod))
            else:
                result_text += f"{count}\t{''.join(S).center(10)}\t{''.join(input_str).center(10)}\t\t错误\t\t分析表中无匹配产生式\n"
                result_text += '该符号串不是该文法的句子'
                break
        else:
            result_text += f"{count}\t{''.join(S).center(10)}\t{''.join(input_str).center(10)}\t\t错误\t\t\t\t无法识别的符号\n"
            result_text += '该符号串不是该文法的句子'
            break

    text_process.delete("1.0", tk.END)
    text_process.insert(tk.END, result_text)

def parse_grammar(grammar_text):
    try:
        grammar = {}
        lines = grammar_text.strip().split(";")
        for line in lines:
            if not line.strip():
                continue
            left, right = line.split("->")
            grammar[left.strip()] = [x.strip() for x in right.split("|")]
            # 获取select_dict
            VN, VT = get_VN_VT(grammar)
            select_dict = {}
            for nt in VN:
                select_dict[nt] = {}
                for prod in grammar[nt]:
                    select_dict[nt][prod] = Se(nt, prod, VN, VT, grammar)
    except Exception as e:
        messagebox.showinfo("Grammar Check", "文法错误")
        text_result.delete("1.0", tk.END)
    return grammar, select_dict


def get_VN_VT(grammar):
    VN = list(grammar.keys())
    VT = list(set(symbol for right in grammar.values() for prod in right for symbol in prod if
                  symbol.islower() or symbol in '+*()iε'))

    return VN, VT


# 创建主窗口
root = tk.Tk()
root.title("Grammar Analysis GUI")

# 创建并放置控件
tk.Label(root, text="输入文法 \t格式: E->TA;A->+TA|ε;T->FB;B->*FB|ε;F->i|(E):").grid(row=0, column=0, columnspan=2)

text_grammar = tk.Text(root, height=2, width=100)
text_grammar.grid(row=1, column=0, columnspan=2)

text_null = tk.Text(root,height=1, width=5)
text_null.grid(row=2,column=0)
null = 'ε'
text_null.insert(tk.END, null)

tk.Button(root, text="检查文法", command=on_check_grammar).grid(row=2, column=0, columnspan=2)

tk.Label(root, text="分析文法结果:").grid(row=3, column=0, columnspan=2)
text_result = tk.Text(root, height=30, width=100)
text_result.grid(row=4, column=0, columnspan=2)

tk.Label(root, text="输入字符串:").grid(row=5, column=0)
entry_string = tk.Entry(root, width=100)
entry_string.grid(row=5, column=1)

tk.Button(root, text="分析字符串", command=on_analyze_string).grid(row=6, column=0, columnspan=2)

tk.Label(root, text="分析字符串过程:").grid(row=7, column=0, columnspan=2)
text_process = tk.Text(root, height=20, width=100)
text_process.grid(row=8, column=0, columnspan=2)

# 启动主事件循环
root.mainloop()
