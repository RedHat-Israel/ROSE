if (typeof(ROSE) === "undefined") {
    ROSE = {};
}

ROSE.game = function() {
    var controller = null;
    var rate = null;
    var context = null;
    var dashboard = null;

    function update() {
        $.get("admin", null, "application/json")
            .done(function(state) {
                // Update
                controller.update(state.started);
                rate.update(state.rate);
                dashboard.update(state.players, state.timeleft);

                // Draw
                dashboard.draw(context);
            })
            .fail(function(xhr) {
                console.log("Error updating: " + xhr.responseText);
            })
    }

    function ready() {
        controller = new ROSE.Controller();
        rate = new ROSE.Rate([0.5, 1.0, 2.0, 5.0, 10.0]);
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

ROSE.Controller = function() {
    var self = this;
    $("#start").click(function(event) {
        event.preventDefault();
        self.start();
    });

    $("#stop").click(function(event) {
        event.preventDefault();
        self.stop();
    });
}

ROSE.Controller.prototype.start = function() {
    var self = this;
    self.disable();
    $.post("admin", {running: 1})
        .done(function() {
            self.update(true);
        })
        .fail(function(xhr) {
            self.update(false);
            console.log("Error starting: " + xhr.responseText);
        })
}

ROSE.Controller.prototype.stop = function() {
    var self = this;
    self.disable();
    $.post("admin", {running: 0})
        .done(function() {
            self.update(false);
        })
        .fail(function(xhr) {
            self.update(true);
            console.log("Error stopping: " + xhr.responseText);
        })
}

ROSE.Controller.prototype.update = function(running) {
    if (running) {
        $("#start").attr("disabled", "disabled");
        $("#stop").removeAttr("disabled");
    } else {
        $("#start").removeAttr("disabled");
        $("#stop").attr("disabled", "disabled");
    }
}

ROSE.Controller.prototype.disable = function() {
    $("#start").attr("disabled", "disabled");
    $("#stop").attr("disabled", "disabled");
}

ROSE.Rate = function(values) {
    this.values = values;
    var self = this;

    $("#dec_rate").click(function(event) {
        event.preventDefault();
        self.decrease();
    });

    $("#inc_rate").click(function(event) {
        event.preventDefault();
        self.increase();
    });
}

ROSE.Rate.prototype.update = function(rate) {
    $("#rate").text(rate);
    this.validate();
}

ROSE.Rate.prototype.value = function() {
    return parseFloat($("#rate").text());
}

ROSE.Rate.prototype.validate = function() {
    var value = this.value();
    if (value == this.values[0]) {
        $("#dec_rate").attr("disabled", "disabled")
    } else {
        $("#dec_rate").removeAttr("disabled")
    }
    if (value == this.values[this.values.length-1]) {
        $("#inc_rate").attr("disabled", "disabled")
    } else {
        $("#inc_rate").removeAttr("disabled")
    }
}

ROSE.Rate.prototype.disable = function() {
    $("#dec_rate").attr("disabled", "disabled")
    $("#inc_rate").attr("disabled", "disabled")
}

ROSE.Rate.prototype.decrease = function() {
    var curr = this.value();
    for (i = this.values.length - 1; i >= 0; i--) {
        if (this.values[i] < curr) {
            this.post(this.values[i]);
            break;
        }
    }
}

ROSE.Rate.prototype.increase = function() {
    var curr = this.value();
    for (i = 0; i < this.values.length; i++) {
        if (this.values[i] > curr) {
            this.post(this.values[i]);
            break;
        }
    }
}

ROSE.Rate.prototype.post = function(value) {
    var self = this;
    self.disable();
    $.post("admin", {rate: value})
        .done(function() {
            self.update(value);
        })
        .fail(function(xhr) {
            self.validate();
            console.log("Error changing rate: " + xhr.responseText);
        })
}

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
