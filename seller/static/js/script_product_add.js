function previewImages(event) {
    var previewContainer = document.getElementById("preview");
    previewContainer.innerHTML = "";
  
    var files = event.target.files;
  
    for (var i = 0; i < files.length; i++) {
      var file = files[i];
      var reader = new FileReader();
  
      reader.onload = function (event) {
        var image = document.createElement("img");
        image.src = event.target.result;
        previewContainer.appendChild(image);
      };
  
      reader.readAsDataURL(file);
    }
  }
  