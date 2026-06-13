// Variation: check multiple Armstrong numbers
function isArmstrong(num) {
    let temp = num;
    let sum = 0;
    while (temp > 0) {
        let digit = temp % 10;
        sum += digit ** 3;
        temp = Math.floor(temp / 10);
    }
    return sum === num;
}

console.log(isArmstrong(0));
console.log(isArmstrong(1));
console.log(isArmstrong(370));
console.log(isArmstrong(371));
console.log(isArmstrong(407));
console.log(isArmstrong(100));
