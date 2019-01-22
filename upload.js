
var watch = require('recursive-watch')
var request = require('request')
var crypto = require('crypto')
var fs = require('fs')

function hash (thing) {
  return crypto.createHash('SHA1').update(thing).digest('hex')
}

var CAM_INDEX = 0
var SERVER_URL = 'http://localhost:3000'

watch('./raw', function (p) {
  var image = fs.createReadStream(p)
  var formData = {
    detex: image,
    path: p,
    index: CAM_INDEX
  }
  request.post({
      url: SERVER_URL+'/raw',
      formData: formData
    },
    function optionalCallback(err, httpResponse, body) {
      if (err) {
        return console.error('upload failed:', err)
      }
      console.log(body)
    }
  )
})
