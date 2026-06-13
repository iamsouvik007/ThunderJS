// Test: object literals
let person = {name: "Alice", age: 25};
console.log(person.name);
console.log(person.age);

// Test: object methods
let keys = Object.keys(person);
console.log(keys.join(", "));

// Test: ternary operator
let x = 10;
let result = x > 5 ? "big" : "small";
console.log(result);

// Test: arrow function
let double = (n) => n * 2;
console.log(double(7));

// Test: array map
let nums = [1, 2, 3, 4, 5];
let doubled = nums.map((n) => n * 2);
console.log(doubled.join(", "));

// Test: array filter
let evens = nums.filter((n) => n % 2 === 0);
console.log(evens.join(", "));

// Test: array reduce
let sum = nums.reduce((acc, n) => acc + n, 0);
console.log(sum);

// Test: switch
let day = 3;
switch (day) {
    case 1:
        console.log("Monday");
        break;
    case 2:
        console.log("Tuesday");
        break;
    case 3:
        console.log("Wednesday");
        break;
    default:
        console.log("Other");
}

// Test: do...while
let count = 0;
do {
    count++;
} while (count < 3);
console.log(count);

// Test: typeof
console.log(typeof "hello");
console.log(typeof 42);
console.log(typeof true);

// Test: const
const PI = 3.14159;
console.log(PI);

// Test: string methods
let greeting = "  Hello, World!  ";
console.log(greeting.trim());
console.log("hello".toUpperCase());
console.log("WORLD".toLowerCase());
console.log("abcdef".substring(1, 4));
console.log("hello world".includes("world"));

// Test: for-each
let items = ["a", "b", "c"];
let collected = "";
items.forEach((item) => {
    collected += item;
});
console.log(collected);

// Test: type coercion
console.log("5" + 3);
console.log(5 + "3");
