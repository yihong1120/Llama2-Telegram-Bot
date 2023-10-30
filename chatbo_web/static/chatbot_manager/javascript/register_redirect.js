// Use JavaScript to handle the click event of the Register button
document.getElementById("registerBtn").addEventListener("click", function() {
    location.href = this.getAttribute('data-url');
});