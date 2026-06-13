// Variation: different array, string array
let arr = [10, 20, 30, 40, 50];
let reversed = [...arr].reverse();
console.log("Original: " + arr.join(", "));
console.log("Reversed: " + reversed.join(", "));

// Array with push/pop
let stack = [];
stack.push(1);
stack.push(2);
stack.push(3);
console.log(stack.join(", "));
stack.pop();
console.log(stack.join(", "));

// Array slice
let nums = [1, 2, 3, 4, 5];
let sliced = nums.slice(1, 4);
console.log(sliced.join(", "));

// Array find
let found = nums.find((n) => n > 3);
console.log(found);
