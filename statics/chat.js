$(document).ready(function() {
    if (!window.console) window.console = {};
    if (!window.console.log) window.console.log = function() {};

    $("#messageform").on("submit", function() {
        newMessage($(this));
        return false;
    });

    $("#message").select();
    updater.start();
});

function newMessage(form) {
    var message = form.formToDict();
    if (message.body.length > 0) {
        updater.socket.send(JSON.stringify(message));
    }
    form.find("input[id=message]").val("").select();
}

jQuery.fn.formToDict = function() {
    var fields = this.serializeArray();
    var json = {};
    for (var i = 0; i < fields.length; i++) {
        json[fields[i].name] = fields[i].value;
    }
    if (json.next) delete json.next;
    return json;
};

var updater = {
    socket: null,

    start: function() {
        var dst = $("input[name=dst]").val();
        var url = "ws://" + location.host + "/pip?dst=" + dst;
        updater.socket = new WebSocket(url);
        updater.socket.onmessage = function(event) {
            updater.showMessage(JSON.parse(event.data));
        };
    },

    showMessage: function(message) {
        var existing = $("#m" + message.id);
        var src = $("input[name=src]").val();
        if (existing.length > 0) return;
        var node = $(message.html);

        if (message.src === src) {
            node.addClass("float-right");
        }
        node.hide();
        $("#inbox").append(node);
        node.slideDown();
    }
};
