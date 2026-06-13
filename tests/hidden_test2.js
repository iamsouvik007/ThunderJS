// Callback functions
function applyOperation(a, b, operation) {
    return operation(a, b);
}

let result1 = applyOperation(10, 5, (a, b) => a + b);
console.log(result1);

let result2 = applyOperation(10, 5, (a, b) => a - b);
console.log(result2);

// Function expression
let multiply = function(a, b) {
    return a * b;
};
console.log(multiply(3, 4));

// Array some/every/find
let numbers = [1, 2, 3, 4, 5];
console.log(numbers.some((n) => n > 3));
console.log(numbers.every((n) => n > 0));
console.log(numbers.find((n) => n > 3));

// Array sort
let unsorted = [3, 1, 4, 1, 5];
unsorted.sort((a, b) => a - b);
console.log(unsorted.join(", "));

// Nested objects
let obj = {a: {b: {c: 42}}};
console.log(obj.a.b.c);

// String split and join
let csv = "one,two,three";
let parts = csv.split(",");
console.log(parts.length);
console.log(parts.join(" - "));

// Array push/pop
let stack = [];
stack.push(1);
stack.push(2);
stack.push(3);
console.log(stack.pop());
console.log(stack.length);

// Logical operators
console.log(true && false);
console.log(true || false);
console.log(!true);

// Else if
let score = 75;
if (score >= 90) {
    console.log("A");
} else if (score >= 80) {
    console.log("B");
} else if (score >= 70) {
    console.log("C");
} else {
    console.log("F");
}

// Array indexOf
let fruits = ["apple", "banana", "cherry"];
console.log(fruits.indexOf("banana"));
console.log(fruits.indexOf("grape"));
console.log(fruits.includes("cherry"));

// Object.values and Object.entries
let colors = {r: 255, g: 128, b: 0};
console.log(Object.values(colors).join(", "));

// Array.isArray
console.log(Array.isArray([1, 2, 3]));
console.log(Array.isArray("hello"));

// Decrement
let counter = 10;
counter--;
console.log(counter);

// Prefix increment
let val = 5;
console.log(++val);
console.log(val);
