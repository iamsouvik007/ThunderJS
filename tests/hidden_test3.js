// Fibonacci
function fibonacci(n) {
    if (n <= 1) {
        return n;
    }
    return fibonacci(n - 1) + fibonacci(n - 2);
}
console.log(fibonacci(10));

// Factorial
function factorial(n) {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}
console.log(factorial(6));

// Closure
function makeCounter() {
    let count = 0;
    return function() {
        count++;
        return count;
    };
}
let counter = makeCounter();
console.log(counter());
console.log(counter());
console.log(counter());

// Array concat
let a = [1, 2];
let b = [3, 4];
let c = a.concat(b);
console.log(c.join(", "));

// String replace
let str = "Hello World";
console.log(str.replace("World", "JavaScript"));

// Number to string via concatenation
let num = 42;
let strNum = "" + num;
console.log(typeof strNum);
console.log(strNum);

// Nested loops with break
let found = false;
for (let i = 0; i < 5; i++) {
    if (i === 3) {
        found = true;
        break;
    }
}
console.log(found);

// Math operations
console.log(Math.max(1, 5, 3));
console.log(Math.min(1, 5, 3));
console.log(Math.abs(-7));

// JSON
let obj = {name: "test", value: 42};
let jsonStr = JSON.stringify(obj);
console.log(jsonStr);

// Array flat
let nested = [[1, 2], [3, 4], [5]];
let flat = nested.flat();
console.log(flat.join(", "));

// String startsWith/endsWith
console.log("hello world".startsWith("hello"));
console.log("hello world".endsWith("world"));
