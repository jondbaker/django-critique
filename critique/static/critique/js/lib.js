(function($){
    window.djCritique = {
        cookie: {
            get: function(k, d) {
                var cookies = document.cookie.split(';');

                for (var i = 0; i < cookies.length; i++) {
                    var key = cookies[i].substr(
                        0, cookies[i].indexOf('=')).replace(/\s/g, '');

                    if (k === key) {
                        return cookies[i].substr(cookies[i].indexOf('=')+1);
                    }
                }
                return d;
            },
            set: function(k, v) {
                document.cookie = k + '=' + v + ';';
            }
        },
        string: {
            toTitleCase: function(s) {
                return str.replace(/\w\S*/g, function(txt) {
                    return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
                });

            }
        },
        utils: {
            validateEmail: function(e) {
                // @see http://stackoverflow.com/questions/46155/validate-email-address-in-javascript
                var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
                return re.test(e);
            }
        }
    };
})(jQuery);
