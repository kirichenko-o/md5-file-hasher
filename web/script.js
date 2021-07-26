function get_name(str){
  if (str.lastIndexOf('\\')){
      var i = str.lastIndexOf('\\')+1;
  }
  else{
      var i = str.lastIndexOf('/')+1;
  }
  var filename = str.slice(i);
  var fileInput = document.getElementById("fileformlabel");
  fileInput.innerHTML = filename;
}

function upload() {
  const fileInput = document.getElementById("file");
  const formData = new FormData();
  const request = new XMLHttpRequest();

  if (!fileInput.files[0]) {
    alert("Please choose file!");
    return;
  }

  formData.set("file", fileInput.files[0]);
  request.open("POST", "http://localhost:8000/upload");

  request.onload = function (event) {
    if(request.status === 201) {
      console.log(request.responseText);
      document.getElementById("result-id").innerHTML = "Id: "
        + JSON.parse(request.responseText).id
        + " (use this value for getting result)";
    } else {
      alert(request.responseText);
    }

    fileInput.value = "";
    var fileformlabel = document.getElementById("fileformlabel");
    fileformlabel.innerHTML = "";
  }

  request.send(formData);
}

function get_task_info() {
  const idInput = document.getElementById("id-input");
  if (!idInput.value) {
    alert("Please set id!");
    return;
  }

  const request = new XMLHttpRequest();
  request.open("GET", "http://localhost:8000/get_task_info/" + idInput.value);

  request.onload = function (event) {
    if(request.status === 200) {
        let json = JSON.parse(request.responseText);
        document.getElementById("result").innerHTML =
            "Id: " + json.id + "<br>" +
            "Task state: " + json.task_state + "<br>" +
            "File name: " + json.original_file_name + "<br>" +
            "Hash: " + json.md5_hash;
    } else {
      alert(request.responseText);
    }
    idInput.value = ""
  }

  request.send();
}