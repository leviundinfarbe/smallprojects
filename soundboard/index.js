#!/usr/bin/env node
const fs = require('fs');
const { exec } = require('child_process');

const express = require('express');
const app = express();
app.disable('x-powered-by');

function makeHead(page) {
    var head = `<!DOCTYPE html>
<html lang="en">
    <head>
        <title>${(typeof page.title == 'undefined') ? 'traumweh' : page.title}</title>
        <link rel="stylesheet" href="/css/styles.css">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta charset="utf-8">
        ${(typeof page.style == 'undefined') ? '' : page.style}
        ${(typeof page.script == 'undefined') ? '' : page.script}
    </head>`;
    return head;
};

app.get('/', (req, res) => {
    var page = new Object;
    page.title = "soundboard";
    page.script = `
        <script>
            function playSound(sound) {
                var xmlHttp = new XMLHttpRequest();
                xmlHttp.open("GET", \`/playSound?name=\${sound}\`, true);
                xmlHttp.send(null);
            };
            function stop() {
                var xmlHttp = new XMLHttpRequest();
                xmlHttp.open("GET", '/stop', true);
                xmlHttp.send(null);
            };
        </script>`;

    let response = makeHead(page)
    let categories = fs.readdirSync('./sounds');

    response += `
    <body>
        <div class="main">`;
    for (let [i, category] of categories.entries()) {
        response += `
            <h3>${category}</h3>`;
        var tmp = fs.readdirSync(`./sounds/${category}`);
        for (let [i, sound] of tmp.entries()) {
            response += `
                <button onclick="playSound('${sound}')">${sound.replace('.wav', '')}</button>`;
        }
    };
    response += `
        </div>
        <div class="stop">
            <button onclick="stop()">Stop</button>
        </div>
    </body>
</html>`;

    res.send(response);
});

app.get('/playSound', (req, res) => {
    if (!req.query.name) return;
    var name = req.query.name;
    var sounds = new Object;
    let categories = fs.readdirSync('./sounds');

    for (let [i, category] of categories.entries()) {
        var sounds = fs.readdirSync(`./sounds/${category}`);
        for (let [i, sound] of sounds.entries()) {
            if (name == sound) var check = `${category}/${sound}`;
        }
    };

    if (typeof check != 'undefined') exec(`aplay "/var/www/soundboard/sounds/${check}" &`);
    res.send();
});

app.get('/stop', (req, res) => {
    exec(`killall aplay`);
    res.send();
});

app.use('/css', express.static('./css'));

app.use(function(req, res, next) {
    if(req.accepts('html') && res.status(404)) return res.send("404");
});

app.listen(8082, () => console.log(`Webserver started`));

