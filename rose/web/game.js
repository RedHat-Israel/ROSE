
class App {
    client = null;
    controller = null;
    rate = null;
    context = null;
    dashboard = null;
    track = null;
    obstacles = null;
    cars = null;
    finish_line = null;

    ready() {
        this.controller = new Controller();
        this.rate = new Rate([0.5, 1.0, 2.0, 5.0, 10.0]);
        const imageLoader = new ImageLoader(() => {
            this.client = new Client(this.onmessage.bind(this), 2000);
        });

        this.context = document.querySelector("#game").getContext("2d");
        this.dashboard = new Dashboard();
        this.track = new Track(imageLoader);
        this.obstacles = new Obstacles(imageLoader);
        this.cars = new Cars(imageLoader);
        this.finish_line = new FinishLine(imageLoader);
        this.sound = new Sound("res/soundtrack/Nyan_Cat.ogg");
    }

    onmessage(m) {
        const msg = JSON.parse(m.data);
        if (msg.action !== "update") {
            console.log(`Ignoring unknown message: ${m.data}`);
            return;
        }

        const state = msg.payload;

        // Update
        this.controller.update(state);
        this.rate.update(state.rate);
        this.dashboard.update(state);
        this.track.update(state);
        this.obstacles.update(state);
        this.cars.update(state);
        this.finish_line.update(state);

        // Draw
        this.dashboard.draw(this.context);
        this.track.draw(this.context);
        this.obstacles.draw(this.context);
        this.cars.draw(this.context);
        this.finish_line.draw(this.context);
    }
}

class Client {
    constructor(onmessage, reconnect_msec) {
        this.onmessage = onmessage;
        this.reconnect_msec = reconnect_msec;
        this.socket = null;
        this.connect();
    }

    connect() {
        var wsuri = "ws://" + window.location.hostname + ":8880/ws";
        console.log("Connecting to " + wsuri);
        this.socket = new WebSocket(wsuri);
        this.socket.onopen = (e) => {
            console.log("Connected")
        };
        this.socket.onmessage = this.onmessage;
        this.socket.onclose = this.onclose.bind(this);
    }

    onclose(e) {
        console.log("Disconnected wasClean=" + e.wasClean + ", code=" +
            e.code + ", reason='" + e.reason + "')");
        this.socket = null;
        console.log("Reconnecting in " + this.reconnect_msec + " milliseconds");
        setTimeout(this.connect.bind(this), this.reconnect_msec);
    }
}

class Controller {
    constructor() {
        this.initializeEvents();
    }

    initializeEvents() {
        document.querySelector("#start").addEventListener("click", event => {
            event.preventDefault();
            this.start();
        });

        document.querySelector("#stop").addEventListener("click", event => {
            event.preventDefault();
            this.stop();
        });
    }

    start() {
        var self = this;
        self.disable();

        fetch("admin?running=1", {method: 'POST'})
            .then(() => {
                console.log("starting");
            })
            .catch((e) => {
                console.log("Error starting: " + e.toString());
            })
    }

    stop() {
        var self = this;
        self.disable();
        fetch("admin?running=0", {method: 'POST'})
            .then(() => {
                console.log("stopping");
            })
            .catch((e) => {
                console.log("Error stopping: " + e.toString());
            })
    }

    update(state) {
        if(state.players.length == 0){
            document.querySelector("#info").textContent = ("No players connected")
            document.querySelector("#start").setAttribute("disabled", "disabled");
            document.querySelector("#stop").setAttribute("disabled", "disabled");
        }
        else if (state.started) {
            document.querySelector("#info").textContent = ("")
            document.querySelector("#start").setAttribute("disabled", "disabled");
            document.querySelector("#stop").removeAttribute("disabled");
        } else {
            document.querySelector("#info").textContent = ("")
            document.querySelector("#start").removeAttribute("disabled");
            document.querySelector("#stop").setAttribute("disabled", "disabled");
        }
    }

    disable() {
        document.querySelector("#start").setAttribute("disabled", "disabled");
        document.querySelector("#stop").setAttribute("disabled", "disabled");
    }
}

class Rate {
    constructor(values) {
        this.values = values;
        this.rate = null;
        this.initializeEvents();
    }


    initializeEvents() {
        document.querySelector("#dec_rate").addEventListener("click", event => {
            event.preventDefault();
            this.decrease();
        });

        document.querySelector("#cur_rate").addEventListener("click", event => {
            event.preventDefault();
            this.post(1);
        });

        document.querySelector("#inc_rate").addEventListener("click", event => {
            event.preventDefault();
            this.increase();
        });
    }

    update(rate) {
        this.rate = rate;
        document.querySelector("#cur_rate").textContent = (rate + " FPS");
        this.validate();
    }

    validate() {
        if (this.rate == this.values[0]) {
            document.querySelector("#dec_rate").setAttribute("disabled", "disabled")
        } else {
            document.querySelector("#dec_rate").removeAttribute("disabled")
        }
        document.querySelector("#cur_rate").removeAttribute("disabled");
        if (this.rate == this.values[this.values.length-1]) {
            document.querySelector("#inc_rate").setAttribute("disabled", "disabled")
        } else {
            document.querySelector("#inc_rate").removeAttribute("disabled")
        }
    }

    disable() {
        document.querySelector("#rate_ctl button").setAttribute("disabled", "disabled");
    }

    decrease() {
        var i;
        for (i = this.values.length - 1; i >= 0; i--) {
            if (this.values[i] < this.rate) {
                this.post(this.values[i]);
                break;
            }
        }
    }

    increase() {
        var i;
        for (i = 0; i < this.values.length; i++) {
            if (this.values[i] > this.rate) {
                this.post(this.values[i]);
                break;
            }
        }
    }

    post(value) {
        var self = this;
        self.disable();
        fetch(`admin?rate=${value}`, {method: 'POST'})
            .then(() => {
                self.update(value);
            })
            .catch((e) => {
                self.validate();
                console.log("Error changing rate: " + e.toString());
            })
    }

}

class Dashboard {
    players = null;
    timeleft = null;

    update(state) {
        this.players = state.players;
        this.timeleft = state.timeleft;
    }

    draw() {
        const text = this.timeleft < 10 ? `0${this.timeleft}` : this.timeleft.toString();
        document.querySelector("#time_left").textContent = text;

        for (let player of this.players) {
            if (player.lane === 0) {
                document.querySelector("#left.player .name").textContent = player.name;
                document.querySelector("#left.player .score").textContent = player.score;
            } 
            if (player.lane === 1) {
                document.querySelector("#right.player .name").textContent = player.name;
                document.querySelector("#right.player .score").textContent = player.score;
            }
        }
    }
}

class Obstacles {
    constructor(loader) {
        this.track = null;
        this.textures = {};

        const obstacleNames = ["barrier", "bike", "crack", "penguin", "trash", "water"];

        obstacleNames.forEach(name => {
            loader.load(`res/obstacles/${name}.png`, (img) => {
                this.textures[name] = img;
            });
        });
    }

    update(state) {
        this.track = state.track;
    }

    draw(ctx) {
        for (let obstacle of this.track) {
            const img = this.textures[obstacle.name];
            const x = Config.left_margin + obstacle.x * Config.cell_width;
            const y = Config.top_margin + obstacle.y * Config.row_height;
            ctx.drawImage(img, x, y);
        }
    }
}

class Cars {
    constructor(loader) {
        this.players = null;
        this.textures = [null, null, null, null];

        for (let i = 0; i < 4; i++) {
            loader.load(`res/cars/car${i + 1}.png`, (img) => {
                this.textures[i] = img;
            });
        }
    }

    update(state) {
        this.players = state.players;
    }

    draw(ctx) {
        ctx.fillStyle = "rgb(0, 0, 0)";
        ctx.textBaseline = "top";
        ctx.font = "bold 15px sans-serif";
        ctx.textAlign = "center";

        for (let player of this.players) {
            const img = this.textures[player.car];
            const x = Config.left_margin + player.x * Config.cell_width;
            const y = player.y * Config.row_height;
            
            ctx.drawImage(img, x, y);
            
            const car_center = x + (img.width / 2);
            const car_bottom = y + img.height;
            
            ctx.fillText(player.name, car_center, car_bottom + 5);
        }
    }
}

class FinishLine {
    constructor(loader) {
        this.texture = null;
        this.timeleft = null;

        loader.load("res/end/final_flag.png", (img) => {
            this.texture = img;
        });
    }

    update(state) {
        this.timeleft = Math.max(state.timeleft, 0);
    }

    draw(ctx) {
        if (this.timeleft > Config.finish_line_duration) {
            return;
        }

        // Start at row 0, then move down until row finish_line_duration
        const row = Config.finish_line_duration - this.timeleft;
        const y = Config.row_height * row;

        ctx.drawImage(this.texture, 0, y);
    }
}

class Track {
    constructor(loader) {
        this.track = null;
        this.textures = [null, null, null];

        loader.load("res/bg/bg_1.png", (img) => {
            this.textures[0] = img;
        });
        loader.load("res/bg/bg_2.png", (img) => {
            this.textures[1] = img;
        });
        loader.load("res/bg/bg_3.png", (img) => {
            this.textures[2] = img;
        });
    }

    update(state) {
        this.track = state.track;
        if (state.started) {
            // Simulate track movement
            const last = this.textures.pop();
            this.textures.unshift(last);
        }
    }

    draw(ctx) {
        for (let i = 0; i < Config.track_length; i++) {
            const img = this.textures[i % this.textures.length];
            ctx.drawImage(img, 0, i * img.height);
        }
    }
}

class ImageLoader {
    constructor(done) {
        this.loading = 0;
        this.done = done;
    }

    load(url, done) {
        const img = new Image();
        this.loading++;
        img.onload = () => {
            done(img);
            this.loading--;
            if (this.loading === 0) {
                this.done();
            }
        };
        img.src = url;
    }
}

class Sound {
    constructor(filePath) {
        this.audio = new Audio();
        this.audio.src = filePath;
        this.playing = false;

        document.querySelector("#music_ctl").addEventListener("click", event => {
            event.preventDefault();
            if (this.playing) {
                this.pause();
                event.target.textContent = "Music";
            } else {
                this.play();
                event.target.textContent = "Mute";
            }
            this.playing = !this.playing;
        });
    }

    play() {
        this.audio.play();
    }

    pause() {
        this.audio.pause();
    }
}

const Config = {
    left_margin: 95,
    cell_width: 130,
    top_margin: 10,
    row_height: 65,
    track_length: 9,
    finish_line_duration: 5
};

const ROSE = new App();