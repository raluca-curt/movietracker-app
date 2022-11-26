
// Image carousel for forms
let images = ["/static/images/1.jpg", "/static/images/2.jpg", "/static/images/3.jpg", "/static/images/4.jpg", "/static/images/5.jpg"]
n = 0
// Grab main

setInterval(() => {
    document.querySelector("main").style.background = `url(${images[n]}), rgba(43, 52, 63, 0.634)`
    document.querySelector("main").style.backgroundSize = 'cover';
    if (n < images.length-1)
    {
        n++
    } else {
        n = 0
    }
}, 5000)

