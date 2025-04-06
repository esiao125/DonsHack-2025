window.onload = function()
{
    console.log("YIPPE");

    fetch('http://127.0.0.1:5000/view',
        {
            method: "GET"
        })
        .then(response => response.json())
        .then(data =>
        {
            console.log("Full Data: ", data);

            console.log("Success A: ", data.top_message, " : ", data.top_ranking);
            console.log("Success B: ", data.mid_message, " : ", data.mid_ranking);
            console.log("Success C: ", data.low_message, " : ", data.low_ranking);

            if(data.top_message === "NONE" || data.top_ranking == "0" || data.top_ranking == "-1")
            {
                document.getElementById("1st").textContent = `Not Enough Data Yet!`;
            }

            else
            {
                document.getElementById("1st").innerHTML = `<strong>(${data.top_ranking})</strong> ${data.top_message}`;
            }

            if(data.mid_message === "NONE"|| data.mid_ranking == "0" || data.mid_ranking == "-1")
            {
                document.getElementById("2nd").textContent = ``;
            }

            else
            {
                document.getElementById("2nd").innerHTML = `<strong>(${data.mid_ranking})</strong> ${data.mid_message}`;
            }

            if(data.low_message === "NONE" || data.low_ranking == "0" || data.low_ranking == "-1")
            {
                console.log("NONE 3RD");
                document.getElementById("3rd").textContent = ``;
            }

            else
            {
                console.log("YES 3RD");
                document.getElementById("3rd").innerHTML = `<strong>(${data.low_ranking})</strong> ${data.low_message}`;
            }
        })
        .catch((error) =>
        {
            console.error("Error", error);
        });
};