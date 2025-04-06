window.onload = function()
{
    var issue = document.getElementById("issue");
    var form = document.getElementById("form");
    var submitted = document.getElementById("submitted");
    var place = document.getElementById("place");
    var button = document.getElementById("button");

    button.addEventListener("click", function(event)
    {
        event.preventDefault();

        var issueDesc = issue.value;
        var location = place.value;

        if(issueDesc && location)
        {
            submitted.style.display = 'block';

            var data = new FormData();
            data.append("location", location);
            data.append("issue", issueDesc);

            fetch('http://127.0.0.1:5000/submit',
                {
                    method: "POST",
                    body: data
                })
                .then(response => response.json())
                .then(data =>
                {
                    console.log("Success: ", data);
                })
                .catch((error) =>
                {
                    console.error("Error", error);
                });

            // Clear input fields after submission
            issue.value = "";
            place.value = "";

            // Hide the "submitted" message after 3 seconds
            setTimeout(function(){
                submitted.style.display = 'none';
            }, 3000);
        }

        else
        {
            alert("Please fill out both fields")
        }
    })
}

// window.onload = function() {
//     var issue = document.getElementById("issue");
//     var form = document.getElementById("form");
//     var submitted = document.getElementById("submitted");
//     var place = document.getElementById("place");

//     if (form) {

//         // Make a request to the Flask route
//         var data =
//         {
//             location: place,
//             issue: issue
//         }

//         fetch('http://127.0.0.1:5000/run',
//         {
//             method: 'POST',
//             body: JSON.stringify(data)
//         })
//         .then(response => response.json())
//         .then(data =>
//         {
//             console.log(data.message)
//         }
//         )
//         .catch(error => console.error('Error: ', error));


//         form.addEventListener("submit", function(event) {
//             event.preventDefault();

//             function saveToJson() {
//                 const data = {
//                     "Location": place.value,
//                     "Issue": issue.value
//                 };

//                 var jsonBlob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });

//                 var link = document.createElement('a');
//                 link.href = URL.createObjectURL(jsonBlob);
//                 link.download = 'user_data.json';
//                 //link.click();  // Trigger the download automatically

//                 // Save the data in localStorage for later use
//                 localStorage.setItem('formData', JSON.stringify(data));

//                 console.log('Saved data to localStorage:', data);
//             }

//             // Call saveToJson to handle the form submission
//             saveToJson();

//             // Display the "submitted" message
//             submitted.style.display = 'block';

//             // Clear input fields after submission
//             issue.value = "";
//             place.value = "";

//             // Hide the "submitted" message after 3 seconds
//             setTimeout(function() {
//                 submitted.style.display = 'none';
//             }, 3000);
//         });
//     }
// };