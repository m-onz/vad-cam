var fs = require('fs')
var watch = require('recursive-watch')
var http = require('http');
var mjpegServer = require('mjpeg-server');
http.createServer(function(req, res) {
	mjpegReqHandler = mjpegServer.createReqHandler(req, res);
	setInterval(function () {
		fs.readFile('./feed/0_latest.jpg', function (e, i) {
			if (e || !i) return
			mjpegReqHandler.write(i, function () {
			})
		})
	}, 200)
	res.on('error', function () {
		mjpegReqHandler.close()
	})
}).listen(8081);
