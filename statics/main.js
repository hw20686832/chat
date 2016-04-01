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
        var num = Number($("#badge-" + message.name).text());
        num += message.num;
        $("#badge-" + message.name).text(num);

        if (num != 0) {
            $("#badge-" + message.name).show();
        }
    }
};
