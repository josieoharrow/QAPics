// Modules to control application life and create native browser window
const {app, BrowserWindow} = require('electron')
var fs = require('fs');

// Keep a global reference of the window object, if you don't, the window will
// be closed automatically when the JavaScript object is garbage collected.
let mainWindow

function createWindow () {
  // Create the browser window.
  mainWindow = new BrowserWindow({width: 400, height: 400})

  // and load the index.html of the app.
  mainWindow.loadFile('index.html')
  // Open the DevTools.
  mainWindow.webContents.openDevTools()
  // Emitted when the window is closed.
  mainWindow.on('closed', function () {
    // Dereference the window object, usually you would store windows
    // in an array if your app supports multi windows, this is the time
    // when you should delete the corresponding element.
    mainWindow = null
  })
}

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.on('ready', createWindow)

// Quit when all windows are closed.
app.on('window-all-closed', function () {
  // On macOS it is common for applications and their menu bar
  // to stay active until the user quits explicitly with Cmd + Q
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

app.on('activate', function () {
  // On macOS it's common to re-create a window in the app when the
  // dock icon is clicked and there are no other windows open.
  if (mainWindow === null) {
    createWindow()
  }
})

function openFile() {
    const {dialog} = require('electron').remote
    dialog.showOpenDialog(
   {
    filters: [
      {name: 'Images', extensions: ['png']}
    ]
   }, 
   function(filepaths, bookmarks) {
     var _img = fs.readFileSync(filepaths[0]).toString('base64');
     var _out = '<img src="data:image/png;base64,' + _img + '" />';
     var _target = document.getElementById('image_container');
     _target.insertAdjacentHTML('beforeend', _out);
      return;
    });
}

function location_input() {
 
  dir = "../Output"
  var fileextension = ".png";
  var _target = document.getElementById('outout_image_container');
  _target.innerHTML = "";
  fs.readdirSync(dir).forEach(file => {
    if (file.indexOf(".png") != -1) {
      //Directory
      _target.insertAdjacentHTML('beforeend', "<li onclick=\"toggle_display_image('" + file + "')\">" + file);
    }
  })
  print_dir_images(_target, dir);
}

function print_dir_images(target, dir) {
  fs.readdirSync(dir).forEach(file => {
    if (file.indexOf(".png") != -1) {
      var _img = fs.readFileSync(dir + "/" + file).toString('base64');
      var _out = '<img style="display: none; width: 75px;" id="' + file + '" src="data:image/png;base64,' + _img + '" /> <br/>';
      target.insertAdjacentHTML('beforeend', _out);
    }
  })
}

function toggle_display_image(id_name) {
  if (document.getElementById(id_name).style.display == "block") {
    document.getElementById(id_name).style.display = "none";
  } else {
    document.getElementById(id_name).style.display = "block";
  }
}

/*
function drawLayer(el, layer_start_x, layer_start_y, layer_x, layer_y, color = "yellow") {
  would eventually like to do output processing on the UI side to speed the algorithm up.
  $(el).addClass("absolute");
  $(el).insertAdjacentHTML('beforeend', "")
  var canvas = ''
}*/
