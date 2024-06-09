$(document).ready(function() {
  // Wrap every letter in a span
  var textWrapper = document.querySelector('.Iran .letters');
  textWrapper.innerHTML = textWrapper.textContent.replace(/([^\x00-\x80]|\w)/g, "<span class='letter'>$&</span>");
  var textWrapper = document.querySelector('.Wellness .letters');
  textWrapper.innerHTML = textWrapper.textContent.replace(/([^\x00-\x80]|\w)/g, "<span class='letter'>$&</span>");

  anime.timeline({loop: false})
  .add({
    targets: '.Iran .line',
    scaleY: [0,1],
    opacity: [0,1],
    easing: "easeOutExpo",
    duration: 700
  }).add({
    targets: '.Iran .line',
    translateX: [0, document.querySelector('.Iran .letters').getBoundingClientRect().width + 20],
    easing: "easeOutExpo",
    duration: 700,
    delay: 100
  }).add({
    targets: '.Iran .letter',
    opacity: [0,1],
    easing: "easeOutExpo",
    duration: 600,
    offset: '-=775',
    delay: (el, i) => 34 * (i+1)
  }).add({
    targets: '.line1',
    opacity: 0,
    duration: 200,
    easing: "easeOutExpo",
    delay: 200
  }).add({
    targets: '.Wellness .line',
    scaleY: [0,1],
    opacity: [0,1],
    easing: "easeOutExpo",
    duration: 700
  }).add({
    targets: '.Wellness .line',
    translateX: [0, document.querySelector('.Wellness .letters').getBoundingClientRect().width + 45],
    easing: "easeOutExpo",
    duration: 700,
    delay: 100
  }).add({
    targets: '.Wellness .letter',
    opacity: [0,1],
    easing: "easeOutExpo",
    duration: 600,
    offset: '-=775',
    delay: (el, i) => 34 * (i+1)
  }).add({
    targets: '.line2',
    opacity: 0,
    duration: 200,
    easing: "easeOutExpo",
    delay: 200
  })
  anime({
    targets: 'svg',
    scale: [0, 1],
  });
  anime({
    targets: '.polymorph',
    points: [{
      value: [
              '70 24 119.574 60.369 100.145 117.631 50.855 101.631 3.426 54.369',
              '70 41 118.574 59.369 111.145 132.631 60.855 84.631 20.426 60.369'
            ]
      },
      { value: '70 6 119.574 60.369 100.145 117.631 39.855 117.631 55.426 68.369' },
      { value: '70 57 136.574 54.369 89.145 100.631 28.855 132.631 38.426 64.369' },
      { value: '70 24 119.574 60.369 100.145 117.631 50.855 101.631 3.426 54.369' }
    ],
    easing: 'easeOutQuad',
    duration: 2000,
    loop: true
  });
  
  $("#user-guide").click(function() {
    $("#myModal").modal({
      backdrop: 'static',
      keyboard: false
    });
  });
  
});
