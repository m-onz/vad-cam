
var watch = require('recursive-watch')
var fs = require('fs')

watch('./raw', function (p) {
  console.log('attempting to delete... ', p)
  setTimeout(function () {
    try {
      fs.unlinkSync('./'+p)
    } catch (e) {}
  }, 11000)
})
