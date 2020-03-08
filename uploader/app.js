var express = require('express');
var busboy = require('connect-busboy');
var path = require('path');
var fs = require('fs-extra');

var app = express();
var router = express.Router();
app.use(busboy());
//app.use(express.static(path.join(__dirname, '/views')));
app.use(express.static(__dirname + '/views/'));

router.use(function (req,res,next) {
  console.log('/' + req.method);
  next();
});

router.get('/', function (req, res) {
    res.sendFile(path + 'index.html');
});

app.route('/upload')
    .post(function (req, res, next) {
        var fstream;
        req.pipe(req.busboy);
        req.busboy.on('file', function (fieldname, file, filename) {
            if (filename) {
                console.log("Uploading: " + filename);
                fstream = fs.createWriteStream(__dirname + '/media/' + filename + '-' + Date.now());
                file.pipe(fstream);
                fstream.on('close', function () {
                    console.log("Upload Finished of " + filename);
                });
            }
        });
        res.redirect('back');
    });

var server = app.listen(3030, function () {
    console.log('Listening on port %d', server.address().port);
});
