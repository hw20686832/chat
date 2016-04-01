$(document).ready(function() {
    if (!window.console) window.console = {};
    if (!window.console.log) window.console.log = function() {};

    updater.start();
});

var updater = {
    socket: null,

    start: function() {
        var url = "ws://" + location.host + "/update";
        updater.socket = new WebSocket(url);
        updater.socket.onmessage = function(event) {
            updater.updateMessage(JSON.parse(event.data));
        };
    },

    updateMessage: function(message) {
        $("#badge").html(message.num);
        var num = $("#badge").html();
        if (num != 0) {
            $("#badge").show();
        }
    }
};
