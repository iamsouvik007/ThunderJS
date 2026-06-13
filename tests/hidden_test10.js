// Immediately returned function call chain
function createGreeter(greeting) {
    return function(name) {
        return greeting + ", " + name + "!";
    };
}
let greet = createGreeter("Hello");
console.log(greet("Alice"));
console.log(greet("Bob"));

// Array map with index
let arr = ["a", "b", "c"];
let indexed = arr.map((val, i) => i + ": " + val);
console.log(indexed.join(", "));

// Reduce to build object
let pairs = [["x", 1], ["y", 2], ["z", 3]];
let obj = pairs.reduce((acc, pair) => {
    acc[pair[0]] = pair[1];
    return acc;
}, {});
console.log(obj.x);
console.log(obj.y);
console.log(obj.z);

// Flatten and sum
let nested = [[1, 2], [3, 4], [5, 6]];
let total = nested.flat().reduce((sum, n) => sum + n, 0);
console.log(total);

// String to array and back
let word = "JavaScript";
let chars = word.split("");
chars.sort();
console.log(chars.join(""));

// Countdown with while
let countdown = "";
let i = 5;
while (i > 0) {
    countdown += i;
    if (i > 1) {
        countdown += ", ";
    }
    i--;
}
console.log(countdown);

// Object with dynamic keys
let field = "color";
let config = {};
config[field] = "blue";
config["size"] = 10;
console.log(config.color);
console.log(config.size);

// Truthy/falsy in ternary
let val1 = "" ? "truthy" : "falsy";
let val2 = "hello" ? "truthy" : "falsy";
let val3 = 0 ? "truthy" : "falsy";
let val4 = 1 ? "truthy" : "falsy";
console.log(val1);
console.log(val2);
console.log(val3);
console.log(val4);
