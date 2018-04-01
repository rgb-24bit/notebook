// use strict
'use strict';

// output format
var format = 'result: ';


// array
var arr = [];
for (var num = 0; num < 100; ++num) {
    document.write(format + num);
    arr.push(num);
}
document.write('<hr/>');


// for ... in
for (var num in arr) {
    document.write(format + num);
}
document.write('<hr/>');


// string
var arr = ['\x48', '\x65', '\x6c', '\x6c', '\x6f', '\x20', '\u4e16', '\u754c'];
for (var ch in arr) {
    document.write(format + arr.join(''));
}
document.write('<hr/>');


// 中缀表达式 ==> 后缀表达式
function infix_to_suffix(infix_expression) {
    // 判断字符是否是数字字符
    function is_num(chr) {
        let num_chr = '0123456789';
        return num_chr.indexOf(chr) != -1;
    }

    // 判断运算符优先级 op1 > op2 ==> true
    function is_priority(op1, op2) {
        if (op1 === '+' || op1 === '-') {
            return false;
        }
        else if (op1 === '*' || op1 === '/') {
            return op2 === '+' || op2 === '-';
        }
        return true;  // 不存在比括号优先级高的运算符
    }

    let num = '';
    let res = [], st = [];
    for (let i = 0; i < infix_expression.length; ++i) {
        if (is_num(infix_expression[i])) {
            num += infix_expression[i];
            continue;
        }

        res.push(Number(num));
        num = '';

        if (infix_expression[i] == ')') {
            let last = st.pop();
            while (last != undefined && last != '(') {
                res.push(last);
                last = st.pop();
            }
            continue;
        }

        let last = st.pop();
        if (last === undefined || is_priority(infix_expression[i], last)) {
            st.push(last, infix_expression[i]);
        }
        else {
            while (last != undefined && !is_priority(infix_expression[i], last)) {
                res.push(last);
                last = st.pop();
            }
            st.push(last, infix_expression[i]);
        }
    }

    // 无输入后清空栈
    res.push(Number(num));
    st = st.reverse();
    for (let i in st) {
        if (st[i] != undefined) {
            res.push(st[i]);
            continue;
        }
        break;
    }

    return res;
}

document.write(infix_to_suffix('123*123+4+6+8/2'));
