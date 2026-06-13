// Let without initializer
let x;
console.log(x);
x = 42;
console.log(x);

// For with i--
for (let i = 5; i > 0; i--) {
    console.log(i);
}

// Boolean to string
console.log("result: " + true);
console.log("result: " + false);

// Null checks
let val = null;
if (val === null) {
    console.log("is null");
}
if (!val) {
    console.log("falsy");
}

// Object shorthand
let name = "Alice";
let age = 25;
let person = {name, age};
console.log(person.name);
console.log(person.age);

// Computed property access
let key = "name";
console.log(person[key]);

// Nested function returns
function outer() {
    function inner() {
        return 42;
    }
    return inner();
}
console.log(outer());

// Multiple console.log args
console.log("hello", "world");
console.log(1, 2, 3);

// Empty array
let empty = [];
console.log(empty.length);
console.log(Array.isArray(empty));

// String length
console.log("hello".length);

// Chained string methods
let result = "  Hello World  ".trim().toLowerCase();
console.log(result);

// Array spread in middle
let a = [1, 2, 3];
let b = [0, ...a, 4];
console.log(b.join(", "));

// String repeat
console.log("ab".repeat(3));

// indexOf with -1
console.log([1, 2, 3].indexOf(5));
console.log("hello".indexOf("xyz"));
