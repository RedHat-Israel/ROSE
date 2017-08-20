if (typeof(ROSE) === "undefined") {
    ROSE = {};
}

ROSE.game = function() {
    var rates = [0.5, 1.0, 2.0, 5.0, 10.0];

    function update() {
        $.get("admin", null, "application/json")
            .done(function(state) {
                update_control(state.started);
                update_rate(state.rate)
                update_status(state.started ? "Running" : "Stopped");
                update_dashboard(state.players, state.timeleft);
            })
            .fail(function() {
                update_status("Server error");
            })
    }

    function start() {
        update_status("Starting");
        disable_control();
        $.post("admin", {running: 1})
            .done(function() {
                update_control(true);
                update_status("Running");
            })
            .fail(function() {
                update_control(false);
                update_status("Error statrting");
            })
    }

    function stop() {
        update_status("Stopping");
        disable_control();
        $.post("admin", {running: 0})
            .done(function() {
                update_control(false);
                update_status("Stopped");
            })
            .fail(function() {
                update_control(true);
                update_status("Error stopping");
            })
    }

    function update_control(running) {
        if (running) {
            $("#start").attr("disabled", "disabled");
            $("#stop").removeAttr("disabled");
        } else {
            $("#start").removeAttr("disabled");
            $("#stop").attr("disabled", "disabled");
        }
    }

    function disable_control() {
        $("#start").attr("disabled", "disabled");
        $("#stop").attr("disabled", "disabled");
    }

    function update_dashboard(players, timeleft) {
        // Hide players in case a player disconnected
        $("#lane0").hide();
        $("#lane1").hide();

        // Update and show players
        for (n in players) {
            var p = players[n];
            $("#lane" + p.lane)
                .text(p.name + ": " + p.score)
                .show();
        }

        $("#timeleft").text(timeleft)
    }

    function update_status(value) {
        $("#status").text(value);
    }

    function update_rate(value) {
        $("#rate").text(value);
        validate_rate();
    }

    function parse_rate() {
        return parseFloat($("#rate").text());
    }

    function disable_rate() {
        $("#dec_rate").attr("disabled", "disabled")
        $("#inc_rate").attr("disabled", "disabled")
    }

    function validate_rate() {
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
        disable_rate();
        $.post("admin", {rate: value})
            .done(function() {
                update_rate(value);
            })
            .fail(function() {
                update_status("Error setting rate");
                validate_rate()
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

        setInterval(update, 1000);
        update();
    }

    // exports
    return {
        ready: ready
    };

}();
