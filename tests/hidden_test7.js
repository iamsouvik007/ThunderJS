// String bracket indexing
let str = "hello";
console.log(str[0]);
console.log(str[4]);

// Array bracket access
let arr = [10, 20, 30];
console.log(arr[0]);
console.log(arr[2]);

// Array.from
let chars = Array.from("hello");
console.log(chars.join(", "));

// Math.round edge cases
console.log(Math.round(2.5));
console.log(Math.round(2.4));
console.log(Math.round(-1.5));

// Object.keys iteration
let obj = {a: 1, b: 2, c: 3};
let keys = Object.keys(obj);
for (let i = 0; i < keys.length; i++) {
    console.log(keys[i] + ": " + obj[keys[i]]);
}

// Spread into function args
function sum(a, b, c) {
    return a + b + c;
}
let args = [1, 2, 3];
console.log(sum(...args));

// Nested ternary
let score = 85;
let grade = score >= 90 ? "A" : score >= 80 ? "B" : score >= 70 ? "C" : "F";
console.log(grade);

// String concat with number
console.log("Score: " + 100);
console.log(100 + " points");

// Falsy values
console.log(Boolean(0));
console.log(Boolean(""));
console.log(Boolean(null));
console.log(Boolean(undefined));
console.log(Boolean(1));
console.log(Boolean("hello"));

// Array destructuring via indexing
let pair = [10, 20];
let first = pair[0];
let second = pair[1];
console.log(first + ", " + second);

// Nested array operations
let matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]];
let flat = matrix.flat();
console.log(flat.join(", "));
let sum2 = flat.reduce((a, b) => a + b, 0);
console.log(sum2);
