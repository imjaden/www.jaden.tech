/**
 * Main page JavaScript
 */

(function() {
    'use strict';

    // DOM Elements
    var body = document.body;
    var footer = document.querySelector('.footer');
    var mainContainer = document.querySelector('#main .container');
    var logo = document.getElementById('logo');
    var logoLink = document.getElementById('logo-link');

    /**
     * Responsive layout adjustment
     * Scale main content when viewport is smaller than content
     */
    function adjustMainHeight() {
        var availableHeight = body.clientHeight - footer.clientHeight - 40;
        if (availableHeight < mainContainer.clientHeight) {
            var scale = (availableHeight / mainContainer.clientHeight).toFixed(2);
            mainContainer.style.transform = 'scale(' + scale + ')';
            mainContainer.parentNode.style.padding = '0';
        }
    }

    // Initialize and bind resize event
    adjustMainHeight();
    window.addEventListener('resize', adjustMainHeight);

    /**
     * URL Parameter Utility
     * Parse, stringify, and set timestamp with replaceState
     */
    window.Param = {
        parse: function() {
            var params = {};
            var search = window.location.search.substring(1);
            var parts = search.split('&');

            for (var i = 0, len = parts.length; i < len; i++) {
                var pair = parts[i].split('=');
                if (pair[0] === '') continue;
                params[pair[0]] = (pair.length > 1 ? pair[1] : null);
            }

            return params;
        },

        toString: function(paramsHash) {
            var pairs = [];
            for (var key in paramsHash) {
                if (paramsHash.hasOwnProperty(key)) {
                    pairs.push(key + '=' + paramsHash[key]);
                }
            }
            return window.location.href.split('?')[0] + '?' + pairs.join('&');
        }
    };

    /**
     * Timestamp refresh logic
     * Refresh page if timestamp is missing or older than 1 hour
     */
    var params = window.Param.parse();
    var timestamp = Number(params.t);
    var oneHour = 60 * 60 * 1000;

    if (isNaN(timestamp) || timestamp - Math.floor(Date.now() / 1000) > 1 || (Date.now() - timestamp * 1000) > oneHour) {
        params.t = Math.floor(Date.now() / 1000);
        history.replaceState(null, '', window.Param.toString(params));
    }

    /**
     * QR Code toggle functionality
     * Switch between logo and QR code on click
     */
    var originalLogoSrc = logo.src;
    var qrCodeSrc = 'static/img/wechat-qr.png';
    var qrTimer = null;

    function toggleQRCode(event) {
        event.preventDefault();

        // Clear existing timer if any
        if (qrTimer) {
            clearTimeout(qrTimer);
            qrTimer = null;
        }

        // Toggle between original logo and QR code
        if (logo.src.indexOf('wechat-qr') !== -1) {
            logo.src = originalLogoSrc;
        } else {
            logo.src = qrCodeSrc;
            // Auto-revert after 60 seconds
            qrTimer = setTimeout(function() {
                logo.src = originalLogoSrc;
                qrTimer = null;
            }, 60000);
        }
    }

    // Bind click events for QR code toggle
    logo.addEventListener('click', toggleQRCode);
    logoLink.addEventListener('click', function(event) {
        if (event.target !== logo) {
            toggleQRCode(event);
        }
    });
})();