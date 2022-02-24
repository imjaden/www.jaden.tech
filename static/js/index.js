var body = document.body;
var footer = document.querySelector('.footer');
var main = document.querySelector('#main .container')
window.onresize = (function calcMainheight() {
  var shouldBeHeight = body.clientHeight - footer.clientHeight - 40;
  if(shouldBeHeight < main.clientHeight) {
    var scaleSize = (shouldBeHeight / main.clientHeight).toFixed(2);
    main.style.transform = 'scale(' + scaleSize + ')';
    main.parentNode.style.padding = 0;
  }
  return calcMainheight;
})();

var logo_border_radius = 0
var logo_border_radius_interval = 15;
var itl;
itl = setInterval(function() {
  var style = "border-radius:" + logo_border_radius + "%;";
  document.getElementById("logo").style = style
  if (logo_border_radius_interval > 0 && logo_border_radius >= 90) {
    logo_border_radius_interval = -15
  } else if (logo_border_radius_interval < 0 && logo_border_radius < 5) {
    logo_border_radius_interval = 15
  }
  logo_border_radius += logo_border_radius_interval;
}, 1000);