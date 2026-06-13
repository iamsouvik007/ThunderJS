// Variation: different pattern size
for (let i = 1; i <= 3; i++) {
    let row = "";
    for (let j = 1; j <= i; j++) {
        row += "#";
    }
    console.log(row);
}

// Reverse triangle
for (let i = 5; i >= 1; i--) {
    let row = "";
    for (let j = 1; j <= i; j++) {
        row += "*";
    }
    console.log(row);
}
