if (typeof(ROSE) === "undefined") {
    ROSE = {};
}

ROSE.game = function() {
    var rates = [0.5, 1.0, 2.0, 5.0, 10.0];
    var context = null;
    var dashboard = null;

    function update() {
        $.get("admin", null, "application/json")
            .done(function(state) {
                // Update
                update_control(state.started);
                update_rate(state.rate)
                update_status(state.started ? "Running" : "Stopped");
                dashboard.update(state.players, state.timeleft);

                // Draw
                dashboard.draw(context);
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

        context = $("#game").get(0).getContext("2d");
        dashboard = new ROSE.Dashboard();

        // TODO: wait until all images loaded.
        setInterval(update, 1000);
    }

    // exports
    return {
        ready: ready
    };

}();

ROSE.Dashboard = function() {
    this.players = null;
    this.timeleft = null;
    this.texture = new Image();
    this.texture.src = "res/dashboard/dashboard.png";
}

ROSE.Dashboard.prototype.update = function(players, timeleft) {
    this.players = players;
    this.timeleft = timeleft;
}

ROSE.Dashboard.prototype.draw = function(ctx) {
    ctx.drawImage(this.texture, 0, 0);

    var text = this.timeleft.toString()
    if (this.timeleft < 10) {
        text = "0" + text;
    }

    ctx.fillStyle = "rgb(153, 153, 153)";
    ctx.textBaseline = "middle";

    ctx.font = "bold 48px sans-serif";
    ctx.textAlign = "center";

    ctx.fillText(text, this.texture.width / 2, this.texture.height / 2);

    ctx.font = "bold 36px sans-serif";
    ctx.textAlign = "left";

    for (n in this.players) {
        var player = this.players[n];
        var text = player.name + ": " + player.score;
        ctx.fillText(text, 50 + player.lane * 530, this.texture.height / 2);
    }
}
