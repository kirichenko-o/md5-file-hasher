URL = "http://localhost:8000";

function get_name(str){
  if (str.lastIndexOf("\\")) {
      var i = str.lastIndexOf("\\") + 1;
  }
  else {
      var i = str.lastIndexOf("/") + 1;
  }

  var filename = str.slice(i);
  var fileInput = document.getElementById("fileformlabel");

  fileInput.innerHTML = filename;
}

function upload() {
  const fileInput = document.getElementById("file");
  const uploadButton = document.getElementById("upload-button");

  if (!fileInput.files[0]) {
    alert("Please choose file!");
    return;
  }

  if (uploadButton.hasAttribute('disabled')) {
    return;
  }

  const idEl = document.getElementById("result-id");
  const fileformlabel = document.getElementById("fileformlabel");

  idEl.innerHTML = "";
  uploadButton.innerText = "Uploading...";
  uploadButton.setAttribute('disabled', 'disabled');

  const formData = new FormData();
  const request = new XMLHttpRequest();

  formData.set("file", fileInput.files[0]);
  request.open("POST", URL + "/upload");

  fileformlabel.innerHTML = "";
  fileInput.value = "";

  request.onload = function (event) {
    if(request.status === 201) {
      document.getElementById("result-id").innerHTML =
        JSON.parse(request.responseText).id + " (use this value for getting result)";
    } else if (request.responseText) {
      alert("The remote server returned an error: \n\r" + JSON.parse(request.responseText).detail);
    } else {
      alert("Unrecognized error")
    }

    uploadButton.innerText = "Run task";
    uploadButton.removeAttribute('disabled');
  }

  request.send(formData);
}

function get_task_info() {
  const idInput = document.getElementById("id-input");

  if (!idInput.value) {
    alert("Please set Id!");
    return;
  }

  if (!/^\d+$/.test(idInput.value)) {
    alert("Please set correct Id!");
    return;
  }

  const resultEl = document.getElementById("result");
  const request = new XMLHttpRequest();
  request.open("GET", URL + "/get_task_info/" + idInput.value);

  idInput.value = "";
  resultEl.innerHTML = "Loading...";

  request.onload = function (event) {
    if(request.status === 200) {
        const json = JSON.parse(request.responseText);
        document.getElementById("result").innerHTML =
            "<b>Id: </b>" + json.id + "<br>" +
            "<b>Task state: </b>" + json.task_state + "<br>" +
            "<b>File name: </b>" + json.original_file_name + "<br>" +
            "<b>Hash: </b>" + (json.md5_hash || "");
    } else if (request.responseText) {
      resultEl.innerHTML = "";
      alert("The remote server returned an error: \n\r" + JSON.parse(request.responseText).detail);
    } else {
      alert("Unrecognized error")
    }
  }

  request.send();
}