var Class = function(parent) {
  var klass = function() {
    this.init.apply(this, arguments);
  };

  if (parent) {
    var subclass = function() {};
    subclass.prototype = parent.prototype;
    klass.prototype = new subclass;
  };

  klass.prototype.init = function() {};

  klass.fn = klass.prototype;
  klass.fn.parent = klass;
  klass._super = klass.__proto__;

  klass.extend = function(obj) {
    var extended = obj.extended;
    for (var i in obj) {
      klass[i] = obj[i];
    }
    if (extended) extended(klass);
  };

  klass.include = function(obj) {
    var included = obj.included;
    
    for (var i in obj) {
      klass.fn[i] = obj[i];
    }
    if (included) included(klass);
  };

  return klass;
};

var PubSub = {
    subscribe : function(event, handler) {
        var handlers = this._handlers || (this._handlers = {});
        (this._handlers[event] || (this._handlers[event] = [])).push(handler);
        return this;
    },
    
    publish : function(event, handler) {
        var args = Array.prototype.slice.call(arguments, 0);
        var event = args.shift();
        var list, handlers ,i, l;
        if (!(handlers = this._handlers)) return this;
        if (!(list = this._handlers[event])) return this;
        
        for (i = 0, l = list.length; i < l; i++) {
            list[i].apply(this, args);
        }
        return this;
    }
};

var Notifier = {
    info : function(message) {
        $("#info").html(message);
        $("#info").dialog();
    },
    warn : function(message) {
        $("#warn").html(message);
        $("#warn").dialog({
            modal : true
        });
    },
    error : function(message) {
        $("#error").html(message);
        $("#error").dialog({
            modal : true
        });
    }
};

var User = new Class;
User.extend({
    getCurrentUser : function() {
        var username = $.cookies.get("username");
        var token = $.cookies.get("token");
        if (null == token) return null;
        return new User(username, token);
    },
    usernameExists : function(username) {
        // todo: invoke remote service
        return false;
    },
    signup : function(username, password) {
        // todo: encrypt w/ public key
        var encrypted = password;
        var token = remoteSignup(username, encrypted);
        // todo: js exception mechanism
        if (null == token) {
            return null;
        }
        $.cookies.set("username", username);
        $.cookies.set("token", token);
        return new User(username, token);
    },
    remoteSignup : function(username, password) {
        // todo: invoke remote service
        return null;
    },
    signin : function(password) {
        
    }
});

User.include({
    init : function(username, token) {
        this.username = username;
        this.token = token;
    }
});