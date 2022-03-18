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
}, 1000);

window.Param = {
  parse: function() {
    var params = {},
        search = window.location.search.substring(1),
        parts = search.split('&'),
        pairs = [];

    for(var i = 0, len = parts.length; i < len; i++) {
      pairs = parts[i].split('=');
      if(pairs[0] === '') continue
      params[pairs[0]] = (pairs.length > 1 ? pairs[1] : null);
    }

    return params;
  },
  toString: function(paramsHash) {
    var pairs = [];
    for(var key in paramsHash) {
      pairs.push(key + "=" + paramsHash[key]);
    }
    
    return window.location.href.split("?")[0] + "?" + pairs.join("&");
  },
  redirectTo: function(paramsHash) {
    window.location.href = window.Param.toString(paramsHash);
  }
}

var params = Param.parse()
var t = params.t
if (typeof(t) === 'undefined' || (Date.now() - t) > 60*60*1000) {
  params.t = Date.now()
  Param.redirectTo(params)
}




