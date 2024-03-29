"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g;
    return g = { next: verb(0), "throw": verb(1), "return": verb(2) }, typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (g && (g = 0, op[0] && (_ = 0)), _) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
var fs = require('fs');
var axios = require('axios');
var redis = require("redis");
var jwt = require('jsonwebtoken');
var date = require('date-and-time');
var cors = require('cors');
var client = redis.createClient({
    url: 'redis://redis:6379' // Cambiar localhost por nombre contenedor Docker
});
function connectRedis() {
    return __awaiter(this, void 0, void 0, function () {
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, client.connect()];
                case 1:
                    _a.sent();
                    return [2 /*return*/];
            }
        });
    });
}
connectRedis();
require('dotenv').config();
var app = require('express')();
app.use(cors());
var http = require('http');
var server = http.createServer(app);
var Server = require("socket.io").Server;
var io = new Server(server, {
// path: "/wserver"
});
// app.use((req : any, res : any, next : Function) => {
//     if (!req.headers.authorization) {
//         return res.status(403).json({ error: 'No credentials sent!' });
//     }
//     const token = req.headers.authorization.split(" ")[1];
//     try{
//         //jwt.verify(token, process.env.PRIVATE_KEY); // Comprobamos si el token ha sido firmado por nosotros - Descomentar en producción
//         next();
//     }catch(e){
//         return res.status(403).json({ error: 'The token provided is not valid!' });
//     }
// })
app.get('/getHourlyData', function (req, res) {
    var allLogs = getLogs();
    var logs = {};
    for (var log in allLogs) {
        getLastLogOfEveryHour(allLogs[log], logs, log);
    }
    return res.json(logs);
});
function getLastLogOfEveryHour(logs, newLogs, identifier) {
    newLogs[identifier] = [];
    var hour = 7;
    while (hour <= 21) {
        var last = logs.filter(function (element) {
            return element.hour == hour;
        });
        if (last[last.length - 1]) {
            newLogs[identifier].push(last[last.length - 1]);
        }
        hour++;
    }
}
var oneDay = 86400000;
var interval = 7200000;
var start = Date.now();
// Intervalo para que cada 24 horas de dumpee el json a la db
setInterval(function () { return __awaiter(void 0, void 0, void 0, function () {
    var now, elapsed;
    return __generator(this, function (_a) {
        now = Date.now();
        elapsed = now - start;
        if (elapsed >= oneDay) {
            start = Date.now();
            axios.post("http://laravel:8000/api/dump", getLogs())
                .catch(function (e) {
                console.log(e.message);
            })
                .then(function () {
                console.log("Data Dumped: " + new Date(Date.now()));
            });
        }
        return [2 /*return*/];
    });
}); }, interval);
function authMiddleware(socket, next) {
    return __awaiter(this, void 0, void 0, function () {
        return __generator(this, function (_a) {
            if (socket.handshake.auth.token) {
                try {
                    // jwt.verify(socket.handshake.auth.token, process.env.PRIVATE_KEY); // Comprobamos si el token ha sido firmado por nosotros - Descomentar en producción
                    next();
                }
                catch (e) {
                    next(new Error("The token provided is not valid"));
                }
            }
            else {
                next(new Error("You need to authenticate to establish a connection"));
            }
            return [2 /*return*/];
        });
    });
}
io.use(authMiddleware);
io.on('connection', function (socket) {
    console.log("socket connected: " + socket);
    socket.on('solar-panel-update', function (data) {
        if (instanceOfPanelUpdate(data)) {
            console.log("Inserting log...");
            var newDate = new Date(data.time * 1000);
            data.time = date.format(newDate, 'Y-M-D HH:mm:ss.SSS');
            data.hour = date.format(newDate, 'H');
            insertLog(data);
            io.emit('panel-update', data);
        }
    });
    io.to(socket.id).emit('test');
    socket.on('save-panel-id', function (data) {
        client.set(data.id, socket.id);
    });
    socket.on('solar-panel-command', function (data) { return __awaiter(void 0, void 0, void 0, function () {
        var socketId;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, client.get(data.id)];
                case 1:
                    socketId = _a.sent();
                    io.to(socketId).emit('command', {
                        command: data.command,
                    });
                    return [2 /*return*/];
            }
        });
    }); });
    socket.on('manual-data-dump', function () { return __awaiter(void 0, void 0, void 0, function () {
        return __generator(this, function (_a) {
            axios.post("http://laravel:8000/api/dump", getLogs())
                .then(function () {
                console.log("Data Dumped: " + new Date(Date.now()));
            })
                .catch(function (e) {
                console.log(e.message);
            });
            return [2 /*return*/];
        });
    }); });
});
function insertLog(data) {
    var file = fs.readFileSync('logs.json');
    var fileData = JSON.parse(file);
    if (fileData[data.id]) {
        fileData[data.id].push(data);
    }
    else {
        fileData[data.id] = [data];
    }
    var newData = JSON.stringify(fileData);
    fs.writeFileSync('logs.json', newData, function (err) {
        if (err)
            throw err;
        console.log("New data added");
    });
}
function instanceOfPanelUpdate(object) {
    return 'id' in object;
}
function getLogs() {
    var file = fs.readFileSync('logs.json');
    var fileData = JSON.parse(file);
    return fileData;
}
server.listen(3000, function () {
    console.log('listening on *:3000');
});
