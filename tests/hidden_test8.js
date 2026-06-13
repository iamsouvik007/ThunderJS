// console.log with special values
console.log(null);
console.log(undefined);
console.log(true);
console.log(false);
console.log(NaN);

// Number checks
console.log(isNaN(NaN));
console.log(isNaN(42));
console.log(isNaN("hello"));

// Type conversions
console.log(Number("42"));
console.log(Number(""));
console.log(Number(true));
console.log(Number(false));
console.log(Number(null));
console.log(String(42));
console.log(String(true));
console.log(String(null));

// While with decrement
let n = 5;
let result = 1;
while (n > 0) {
    result = result * n;
    n--;
}
console.log(result);

// do-while basic
let counter = 0;
do {
    counter++;
} while (counter < 5);
console.log(counter);

// Switch with default
let fruit = "mango";
switch (fruit) {
    case "apple":
        console.log("Apple");
        break;
    case "banana":
        console.log("Banana");
        break;
    default:
        console.log("Unknown fruit");
}

// Nested if-else
function classify(n) {
    if (n > 0) {
        if (n > 100) {
            return "large positive";
        } else {
            return "small positive";
        }
    } else if (n < 0) {
        return "negative";
    } else {
        return "zero";
    }
}
console.log(classify(50));
console.log(classify(150));
console.log(classify(-5));
console.log(classify(0));
