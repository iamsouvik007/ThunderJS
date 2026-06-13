// var declaration
var x = 5;
console.log(x);
x = 10;
console.log(x);

// FizzBuzz (common interview question variant)
for (let i = 1; i <= 15; i++) {
    if (i % 3 === 0 && i % 5 === 0) {
        console.log("FizzBuzz");
    } else if (i % 3 === 0) {
        console.log("Fizz");
    } else if (i % 5 === 0) {
        console.log("Buzz");
    } else {
        console.log(i);
    }
}

// Bubble sort
function bubbleSort(arr) {
    let n = arr.length;
    for (let i = 0; i < n - 1; i++) {
        for (let j = 0; j < n - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                let temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
        }
    }
    return arr;
}

let unsorted = [64, 34, 25, 12, 22, 11, 90];
bubbleSort(unsorted);
console.log(unsorted.join(", "));

// GCD
function gcd(a, b) {
    while (b !== 0) {
        let temp = b;
        b = a % b;
        a = temp;
    }
    return a;
}
console.log(gcd(12, 8));
console.log(gcd(54, 24));

// Prime check
function isPrime(n) {
    if (n <= 1) {
        return false;
    }
    for (let i = 2; i <= Math.floor(Math.sqrt(n)); i++) {
        if (n % i === 0) {
            return false;
        }
    }
    return true;
}
console.log(isPrime(7));
console.log(isPrime(12));
console.log(isPrime(29));

// Array of objects
let students = [
    {name: "Alice", grade: 90},
    {name: "Bob", grade: 85},
    {name: "Charlie", grade: 95}
];
let topStudent = students.find((s) => s.grade === 95);
console.log(topStudent.name);

let names = students.map((s) => s.name);
console.log(names.join(", "));

let highGrades = students.filter((s) => s.grade >= 90);
console.log(highGrades.length);

// Sum with reduce
let total = students.reduce((sum, s) => sum + s.grade, 0);
console.log(total);
