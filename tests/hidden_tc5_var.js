// Variation: non-palindrome
let str1 = "hello";
let rev1 = str1.split("").reverse().join("");
if (str1 === rev1) {
    console.log(str1 + " is a Palindrome");
} else {
    console.log(str1 + " is not a Palindrome");
}

// Another palindrome
let str2 = "madam";
let rev2 = str2.split("").reverse().join("");
if (str2 === rev2) {
    console.log(str2 + " is a Palindrome");
} else {
    console.log(str2 + " is not a Palindrome");
}

// String methods
let s = "Hello, World!";
console.log(s.toUpperCase());
console.log(s.toLowerCase());
console.log(s.includes("World"));
console.log(s.indexOf("World"));
console.log(s.slice(0, 5));
console.log(s.replace("World", "JavaScript"));
console.log(s.length);
