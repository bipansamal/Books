// sticky Navigation
let navbar = $(".navbar");

$(window).scroll(function () {
    // get the complete hight of window
    let oTop = $(".section-2").offset().top - window.innerHeight;
    if ($(window).scrollTop() > 50) {
        navbar.addClass("sticky");
    } else {
        navbar.removeClass("sticky");
    }
});


let nCount = function (selector) {
    $(selector).each(function () {
        let $this = $(this); // Cache the current element
        let countTo = parseInt($this.text(), 10); // Ensure the text is a number

        $({ Counter: 0 }).animate(
            { Counter: countTo }, // Target value
            {
                duration: 4000, // Animation duration
                easing: "swing", // Easing function
                step: function (value) {
                    $this.text(Math.ceil(value)); // Update the text on each step
                },
            }
        );
    });
};



let a = 0;
$(window).scroll(function(){
  // The .offset() method allows us to retrieve the current position of an element  relative to the document
  let oTop = $(".numbers").offset().top - window.innerHeight;
  if (a == 0 && $(window).scrollTop() >= oTop){
    a++;
    nCount(".rect > h1");
  }
});
