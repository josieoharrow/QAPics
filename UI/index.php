<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
    <link rel="stylesheet" type="text/css" href="style.css">
    <script type="text/javascript" src="http://code.jquery.com/jquery-1.7.1.min.js"></script>
    <script src="main.js"></script>
    <title>QA Pics</title>
  </head>
  <body>
    <h1 class="center-text">QA Pics</h1>
    <?php
    echo "Hello World!";
    ?>
    <button class="center-text center" onclick="openFile()">Open File</button>
    <br/>
    <span>Database location: </span><textarea rows="1" id="location" oninput="location_input()"></textarea>
    <br/>
    <div id="image_container"></div>
   
    <script>
      // You can also require other files to run in this process
      require('./renderer.js')
    </script>

  </body>
</html>
