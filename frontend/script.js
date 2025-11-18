async function askAI() {
    const query = document.getElementById("ai_input").value;

    const res = await fetch("/ask-ai", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({query})
    });

    const data = await res.json();
    document.getElementById("ai_output").innerText = JSON.stringify(data, null, 2);
}
