function test(n) {
    if (n <= 1) {
        return n;
    }
    let a = test(n - 1);
    let b = test(n - 2);
    console.log("n=" + n + " a=" + a + " b=" + b);
    return a + b;
}
console.log(test(4));
