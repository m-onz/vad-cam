var fs = require('fs')
var watch = require('recursive-watch')
var http = require('http');
var mjpegServer = require('mjpeg-server');
http.createServer(function(req, res) {
        mjpegReqHandler = mjpegServer.createReqHandler(req, res);
        turnips(mjpegReqHandler)
        res.on('error', function () {
                //mjpegReqHandler.close()
        })
}).listen(8081);

function turnips (handler) {
        var t = setTimeout(function () {
                fs.readFile('./feed/0_latest.jpg', function (e, i) {
                        if (e || i.length < 43000) {
                                clearInterval(t);
                                return turnips(handler);
                        }
                        handler.write(i, function () {
                                clearInterval(t)
                                turnips(handler)
                        })
                })
        }, 125)
}


