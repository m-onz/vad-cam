
var fs = require('fs')
var http = require('http')
var formidable = require('formidable')

http.createServer(function (req, res) {
  if (req.method === 'POST') {
    var form = new formidable.IncomingForm()
    form.uploadDir = './raw_upload'
    form.keepExtensions = true
    form.maxFieldsSize = 20 * 1024 * 1024
    form.maxFields = 11
    form.hash = 'sha1'
    form.on('progress', function(bytesReceived, bytesExpected) {
        console.log('progress::', bytesReceived, ' of ', bytesExpected)
    })
    form.parse(req, function (err, fields, files) {
      if (err) return res.end(JSON.stringify({ status: 'e rror'}))
      console.log(fields)
      res.end(JSON.stringify({ status:'success' }))
    })
    return
  }
  res.end(' ')
}).listen(3000)
