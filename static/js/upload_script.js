console.log("Script loaded");

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
  var actionUrl = window.location.protocol + "//" + window.location.host + "/upload";
  document.getElementById("upload-form").action = actionUrl;
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
  // Show loader
  document.getElementById("loader").style.display = "block";

  alert(filename + " submitted for processing");
  console.log("Processing file:", filename);
  const pdfUrl = `/pdf/${encodeURIComponent(filename)}`;
  console.log("PDF URL:", pdfUrl);

  fetch("/process/" + encodeURIComponent(filename), { method: "POST" })
    .then((response) => {
      if (!response.ok) {
        throw new Error(`Server responded with status ${response.status}`);
      }
      return response.json();
    })
    .then((data) => {
      if (data.success) {
        console.log("File processed successfully:", data.message);
        alert(data.message);
      } else {
        console.error("Could not process the file:", data.error);
        alert("Could not process the file: " + data.error);
      }
    }).catch((error) => {
      console.error("Fetch error:", error);
    }).finally(() => {
      // Hide loader
      document.getElementById("loader").style.display = "none";
    });
}




// Function to send a message to the Flask backend
function sendMessage() {
  // Show loader
  document.getElementById("loader").style.display = "block";

  alert("Message sent"); // For debugging
  const query = document.getElementById("message-input").value;
  if (query.trim() === "") {
    // Hide loader if the query is empty
    document.getElementById("loader").style.display = "none";
    return; // Don't send empty messages
  }

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
    }).finally(() => {
      // Hide loader
      document.getElementById("loader").style.display = "none";
    });
}

// Add an event listener to the message input for the "Enter" key press event
document.getElementById("message-input").addEventListener("keypress", function (e) {
  if (e.key === "Enter") {
    alert("Message sent"); // For debugging
    e.preventDefault();
    sendMessage(); // Call the sendMessage function when Enter is pressed
  }
});

document.getElementById("clear-database").addEventListener("click", function () {
  // First confirmation dialog
  if (confirm("Are you sure you want to clear the database?")) {
    // Second confirmation dialog with input
    var userInput = prompt("If you want to clear the database please type 'yes' below");
    if (userInput.toLowerCase() === 'yes') {
      console.log("Button clicked"); // This will confirm that the button click is being recognized.

      fetch("/clear-database", { method: "POST" })
        .then((response) => {
          console.log("Received response from the server"); // Confirms that a response was received.
          return response.json();
        })
        .then((data) => {
          console.log("Response parsed to JSON", data); // Shows the data received from the server.
          if (data.success) {
            alert("Database cleared successfully");
          } else {
            alert("Could not clear the database");
          }
        })
        .catch((error) => {
          console.error("Error:", error); // Catches any errors in the fetch request.
        });
    } else {
      // User typed something other than 'yes' or pressed cancel on the second dialog
      console.log("Database clearing aborted by the user.");
    }
  } else {
    // User pressed 'No' on the first confirmation dialog
    console.log("Database clearing aborted by the user.");
  }
});


// Function to clear the chat window
function clearChat() {
  const responseOutput = document.getElementById("response-output");
  responseOutput.innerHTML = ''; // Clear all child elements of the chat output container
}