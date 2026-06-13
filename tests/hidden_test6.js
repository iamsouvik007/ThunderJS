// Palindrome number check
function isPalindromeNumber(num) {
    let str = "" + num;
    let reversed = str.split("").reverse().join("");
    return str === reversed;
}
console.log(isPalindromeNumber(121));
console.log(isPalindromeNumber(123));
console.log(isPalindromeNumber(1221));

// Power of two
function isPowerOfTwo(n) {
    if (n <= 0) {
        return false;
    }
    while (n > 1) {
        if (n % 2 !== 0) {
            return false;
        }
        n = Math.floor(n / 2);
    }
    return true;
}
console.log(isPowerOfTwo(16));
console.log(isPowerOfTwo(18));
console.log(isPowerOfTwo(1));

// Count vowels
function countVowels(str) {
    let count = 0;
    let vowels = "aeiouAEIOU";
    for (let i = 0; i < str.length; i++) {
        if (vowels.includes(str.charAt(i))) {
            count++;
        }
    }
    return count;
}
console.log(countVowels("Hello World"));
console.log(countVowels("rhythm"));

// Reverse string using loop
function reverseStr(s) {
    let result = "";
    for (let i = s.length - 1; i >= 0; i--) {
        result += s.charAt(i);
    }
    return result;
}
console.log(reverseStr("hello"));
console.log(reverseStr("JavaScript"));

// Two sum
function twoSum(nums, target) {
    for (let i = 0; i < nums.length; i++) {
        for (let j = i + 1; j < nums.length; j++) {
            if (nums[i] + nums[j] === target) {
                return [i, j];
            }
        }
    }
    return [];
}
let indices = twoSum([2, 7, 11, 15], 9);
console.log(indices.join(", "));

// Max in array
function findMax(arr) {
    let max = arr[0];
    for (let i = 1; i < arr.length; i++) {
        if (arr[i] > max) {
            max = arr[i];
        }
    }
    return max;
}
console.log(findMax([3, 7, 2, 9, 1, 5]));

// Sum of digits
function sumOfDigits(n) {
    let sum = 0;
    while (n > 0) {
        sum += n % 10;
        n = Math.floor(n / 10);
    }
    return sum;
}
console.log(sumOfDigits(12345));
console.log(sumOfDigits(9999));
