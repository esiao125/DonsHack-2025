var issue = document.getElementById("issue");
var form = document.getElementById("form");
var submitted = document.getElementById("submitted");
var place = document.getElementById("place");

if(form){
    form.addEventListener("submit", function(event) {
        event.preventDefault(); 

        function saveToJson() {
            const data = {
                "Location": place.value,
                "Issue": issue.value
            };

            var jsonBlob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });


            var link = document.createElement('a');
            link.href = URL.createObjectURL(jsonBlob);
            link.download = 'user_data.json';
            link.click();  // Trigger the download automatically

            // Save the data in localStorage for later use
            localStorage.setItem('formData', JSON.stringify(data));

            console.log('Saved data to localStorage:', data);
        }

        // Call saveToJson to handle the form submission
        saveToJson();

        // Display the "submitted" message
        submitted.style.display = 'block';

        // Clear input fields after submission
        issue.value = "";
        place.value = "";

        // Hide the "submitted" message after 3 seconds
        setTimeout(function() {
            submitted.style.display = 'none';
        }, 3000);
    });
}
