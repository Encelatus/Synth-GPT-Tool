function showConfirmButton() {
  // Check if a file was selected
  var fileInput = document.getElementById("document");
  if (fileInput.value) {
    // Show the confirm button
    document.getElementById("confirm-upload").style.display = "block";
  }
}

document.addEventListener("DOMContentLoaded", function () {
  fetch("/files")
    .then((response) => response.json())
    .then((data) => {
      const fileList = document.getElementById("file-list");
      fileList.innerHTML = "";
      data.forEach((file) => {
        let fileElement = document.createElement("div");
        fileElement.innerHTML = `
                <span>${file}</span>
                <button onclick="deleteFile('${file}')">🗑️</button>
                <button onclick="processFile('${file}')" style="color:green;">✓</button>
            `;
        fileList.appendChild(fileElement);
      });
    });
});

function deleteFile(filename) {
  fetch("/delete/" + filename, { method: "POST" })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        // Remove the file element
        alert("File deleted successfully");
        location.reload(); // Reload the page or call the function to fetch files list again
      } else {
        alert("Could not delete the file");
      }
    });
}

function processFile(filename) {
  fetch("/process/" + filename, { method: "POST" })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        alert(data.message);
        // Additional actions after processing, like updating the UI
      } else {
        alert("Could not process the file: " + data.error);
      }
    });
}

// Function to send a message to the Flask backend
function sendMessage() {
  const query = document.getElementById("message-input").value;
  if (query.trim() === "") return; // Don't send empty messages

  fetch("/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ query: query }),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error(`Server responded with status ${response.status}`);
      }
      return response.json();
    })
    .then((data) => {
      console.log(data); // For debugging
      if (data.response) {
        const responseOutput = document.getElementById("response-output");
        const newResponseDiv = document.createElement("div");
        newResponseDiv.textContent = data.response; // Add the server's response as text content
        responseOutput.appendChild(newResponseDiv); // Append the new div to the response output container
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

// Add an event listener to the message input for the "Enter" key press event
document.getElementById("message-input").addEventListener("keypress", function (e) {
  if (e.key === "Enter") {
    e.preventDefault();
    sendMessage(); // Call the sendMessage function when Enter is pressed
  }
});
