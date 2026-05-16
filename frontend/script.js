async function analyzeEmail() {
    const emailText = document.getElementById("emailText").value;

    const response = await fetch(
        "http://127.0.0.1:8082/analyze-email",
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                email_text: emailText
            })
        }
    );

    const data = await response.json();

    document.getElementById("result").innerHTML = `
        <div class="card">
            <h3>Analysis Result</h3>
            <p><strong>Category:</strong> ${data.category}</p>
            <p><strong>Priority:</strong> ${data.priority}</p>
            <p><strong>Suggested Reply:</strong> ${data.suggested_reply}</p>
        </div>
    `;
}


async function loadEmails() {
    const response = await fetch("http://127.0.0.1:8082/emails");

    const data = await response.json();

    let html = "";

    data.forEach(email => {
        html += `
            <div class="card">
                <p><strong>Email:</strong> ${email.email_text}</p>
                <p><strong>Category:</strong> ${email.category}</p>
                <p><strong>Priority:</strong> ${email.priority}</p>
                <p><strong>Reply:</strong> ${email.suggested_reply}</p>
            </div>
        `;
    });

    document.getElementById("emailList").innerHTML = html;
}