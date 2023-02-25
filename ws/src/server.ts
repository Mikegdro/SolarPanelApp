const fs = require('fs');
const axios = require('axios');
const redis = require("redis");
const jwt = require('jsonwebtoken');

const client = redis.createClient({
    url: 'redis://localhost:6379' // Cambiar localhost por nombre contenedor Docker
});
async function connectRedis(){
    await client.connect()
}
connectRedis();

require('dotenv').config();
const io = require("socket.io")(3000, {
    cors: {
        origin: ["http://localhost:8080"], // Aquí se pondrán el/los clientes que se conecten al ws
    },
});

const oneDay = 86400000;
const interval = 7200000;
let start = Date.now();

// Modelos de mensajes
interface PanelUpdate {
    id: string// Identificador único del panel
    time: string // Fecha del update
    type: string
    log: {
        sensor1: number
        sensor2: number
        sensor3: number
        sensor4: number
        motor1: number
        motor2: number
        battery: string
        potency: number
        image: string
        ocvOutput: string
    }
}

interface PanelCommand {
    id: string
    command: string
}

// Intervalo para que cada 24 horas de dumpee el json a la db
setInterval(async () =>{
    let now = Date.now();
    let elapsed = now - start;
    if(elapsed >= oneDay){
        start = Date.now();
        axios.post("http://laravel:8000/api/dump", getLogs())
            .catch((e : any) =>{
                console.log(e.message)
            })
            .then(() =>{
                console.log("Data Dumped: " + new Date(Date.now()));
            });
    }
}, interval)

async function authMiddleware(socket : any, next : Function){
    if(socket.handshake.auth.token){
        try{
            // jwt.verify(socket.handshake.auth.token, process.env.PRIVATE_KEY); // Comprobamos si el token ha sido firmado por nosotros - Descomentar en producción
            next();
        }catch(e){
            next(new Error("The token provided is not valid"));
        }
    }else{
        next(new Error("You need to authenticate to establish a connection"));
    }
}

io.use(authMiddleware);
io.on('connection', (socket : any) =>{
    console.log("socket connected: " + socket);
    
    socket.on('solar-panel-update', (data : PanelUpdate) =>{
        if(instanceOfPanelUpdate(data)){
            insertLog(data);
            io.emit('panel-update', data);
        }
    });

    socket.on('save-panel-id', (data : any) =>{
        console.log(data)
        client.set(data.id, socket.id);
    });

    socket.on('solar-panel-command', async (data : PanelCommand) =>{
        let socketId = await client.get(data.id);
        console.log(socketId)
        io.to(socketId).emit('command', {
            command: data.command,
        });
    });

    socket.on('manual-data-dump', async () =>{
        axios.post("http://laravel:8000/api/dump", getLogs())
        .then(() =>{
            console.log("Data Dumped: " + new Date(Date.now()));
        })
        .catch((e : any) =>{
            console.log(e.message)
        });
    });
})

function insertLog(data : PanelUpdate){
    let file = fs.readFileSync('logs.json');
    let fileData = JSON.parse(file);
    if(fileData[data.id]){
        fileData[data.id].push(data);
    }else{
        fileData[data.id] = [data];
    }
    let newData = JSON.stringify(fileData);
    fs.writeFileSync('logs.json', newData, (err : any) => {
        if(err) throw err;
        
        console.log("New data added");
    });  
}

function instanceOfPanelUpdate(object: any): object is PanelUpdate {
    return 'id' in object;
}

function getLogs(){
    let file = fs.readFileSync('logs.json');
    let fileData = JSON.parse(file);
    return fileData;
}