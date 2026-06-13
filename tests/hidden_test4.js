// Higher-order functions with callbacks
function operate(arr, callback) {
    let result = [];
    for (let i = 0; i < arr.length; i++) {
        result.push(callback(arr[i]));
    }
    return result;
}

let nums = [1, 2, 3, 4, 5];
let squares = operate(nums, function(x) { return x * x; });
console.log(squares.join(", "));

let doubled = operate(nums, (x) => x * 2);
console.log(doubled.join(", "));

// Scope test
let x = 10;
function changeX() {
    x = 20;
}
changeX();
console.log(x);

// Nested function calls
function add(a, b) { return a + b; }
function multiply(a, b) { return a * b; }
console.log(add(multiply(2, 3), multiply(4, 5)));

// String number conversion
let numStr = "42";
let parsed = parseInt(numStr);
console.log(parsed + 8);
console.log(typeof parsed);

// Boolean logic
let a = true;
let b = false;
console.log(a && b);
console.log(a || b);
console.log(!a);
console.log(a && !b);

// Null/undefined checks
let val = null;
console.log(val === null);
console.log(val === undefined);
console.log(val == undefined);

// Multi-dimensional array
let matrix = [[1, 2], [3, 4], [5, 6]];
console.log(matrix[0][0]);
console.log(matrix[1][1]);
console.log(matrix[2][0]);

// Object with method-like property
let calculator = {
    add: function(a, b) { return a + b; },
    subtract: function(a, b) { return a - b; }
};
console.log(calculator.add(10, 5));
console.log(calculator.subtract(10, 5));

// Template-style string building
let name = "Alice";
let age = 30;
let message = "My name is " + name + " and I am " + age + " years old.";
console.log(message);

// Chained array operations
let data = [5, 3, 8, 1, 9, 2, 7];
let result = data.filter((n) => n > 3).sort((a, b) => a - b).map((n) => n * 10);
console.log(result.join(", "));

// For loop with continue
let evenSum = 0;
for (let i = 1; i <= 10; i++) {
    if (i % 2 !== 0) {
        continue;
    }
    evenSum += i;
}
console.log(evenSum);
