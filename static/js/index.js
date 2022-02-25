var body = document.body;
var footer = document.querySelector('.footer');
var main = document.querySelector('#main .container');
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
var svg = document.getElementById("background").getSVGDocument()
var style, node, random, last_path, last_path_style;
setInterval(function() {
  style = "border-radius:" + logo_border_radius + "%;";
  document.getElementById("logo").style = style
  if (logo_border_radius_interval > 0 && logo_border_radius >= 90) {
    logo_border_radius_interval = -15
  } else if (logo_border_radius_interval < 0 && logo_border_radius < 5) {
    logo_border_radius_interval = 15
  }
  logo_border_radius += logo_border_radius_interval;

  // if(svg) {
  //   last_path.style = last_path_style;
  //   random = Math.floor(Math.random()*node.childNodes.length)
  //   last_path = node.childNodes.item(random)
  //   last_path_style = last_path.getAttribute("style")
  //   last_path.style = "stroke:#ff0"
  // } else {
  //   svg = document.getElementById("background").getSVGDocument()
  //   node = svg.documentElement;
  //   random = Math.floor(Math.random()*node.childNodes.length)
  //   last_path = node.childNodes.item(random)
  //   last_path_style = last_path.getAttribute("style")
  // }
}, 1000);
