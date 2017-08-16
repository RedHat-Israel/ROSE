if (typeof(ROSE) === "undefined") {
    ROSE = {};
}

ROSE.game = function() {
    var updater = null;
    var rates = [0.5, 1.0, 2.0, 5.0, 10.0];

    function update() {
        $.get("admin", null, "application/json")
            .done(function(state) {
                // Hide players in case a player disconnected
                $("#lane0").hide();
                $("#lane1").hide();
                // Update and show players
                for (n in state.players) {
                    var p = state.players[n];
                    $("#lane" + p.lane)
                        .text(p.name + ": " + p.score)
                        .show();
                }
                $("#timeleft").text(state.timeleft)
                if (state.started) {
                    $("#status").html("Running");
                    $("#start").attr("disabled", "disabled");
                    $("#stop").removeAttr("disabled");
                } else {
                    $("#status").html("Stopped");
                    $("#start").removeAttr("disabled");
                    $("#stop").attr("disabled", "disabled");
                }
                $("#rate").text(state.rate);
                validate_rate_control();
            })
            .fail(function() {
                $("#status").html("Server error");
            })
    }

    function start() {
        $("#status").html("Starting");
        $("#start").attr("disabled", "disabled");
        $.post("admin", {running: 1})
            .done(function() {
                $("#status").html("Running");
                $("#stop").removeAttr("disabled")
            })
            .fail(function() {
                $("#start").removeAttr("disabled")
                $("#status").html("Error starting");
            })
    }

    function stop() {
        $("#status").html("Stopping...");
        $("#stop").attr("disabled", "disabled");
        $.post("admin", {running: 0})
            .done(function() {
                $("#status").html("Stopped");
                $("#start").removeAttr("disabled")
            })
            .fail(function() {
                $("#stop").removeAttr("disabled")
                $("#status").html("Error stopping");
            })
    }

    function parse_rate() {
        return parseFloat($("#rate").text());
    }

    function disable_rate_control() {
        $("#dec_rate").attr("disabled", "disabled")
        $("#inc_rate").attr("disabled", "disabled")
    }

    function validate_rate_control() {
        var value = parse_rate();
        if (value == rates[0]) {
            $("#dec_rate").attr("disabled", "disabled")
        } else {
            $("#dec_rate").removeAttr("disabled")
        }
        if (value == rates[rates.length-1]) {
            $("#inc_rate").attr("disabled", "disabled")
        } else {
            $("#inc_rate").removeAttr("disabled")
        }
    }

    function decrease_rate() {
        var curr = parse_rate();
        for (i = rates.length - 1; i >= 0; i--) {
            if (rates[i] < curr) {
                set_rate(rates[i]);
                break;
            }
        }
    }

    function increase_rate() {
        var curr = parse_rate();
        for (i = 0; i < rates.length; i++) {
            if (rates[i] > curr) {
                set_rate(rates[i]);
                break;
            }
        }
    }

    function set_rate(value) {
        disable_rate_control();
        $.post("admin", {rate: value})
            .fail(function() {
                $("#status").text("Error setting rate");
            })
            .done(function() {
                $("#rate").text(value);
            })
            .always(function() {
                validate_rate_control()
            })
    }

    function ready() {
        $("#start").click(function(event) {
            event.preventDefault();
            start();
        });

        $("#stop").click(function(event) {
            event.preventDefault();
            stop();
        });

        $("#dec_rate").click(function(event) {
            event.preventDefault();
            decrease_rate();
        });

        $("#inc_rate").click(function(event) {
            event.preventDefault();
            increase_rate();
        });

        updater = setInterval(update, 1000);
        update();
    }

    // exports
    return {
        ready: ready
    };

}();
