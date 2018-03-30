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
