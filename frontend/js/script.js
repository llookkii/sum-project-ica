function calculateSum() {
    const num1 = parseFloat(document.getElementById('number1').value);
    const num2 = parseFloat(document.getElementById('number2').value);

    fetch('/api/calculate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ num1, num2 })
    })
        .then(response => response.json())
        .then(data => {
            document.getElementById('result').textContent = `The sum is: ${data.result}`;
            fetchHistory();
        })
        .catch(error => console.error('Error:', error));
}

function fetchHistory() {
    fetch('/api/history')
        .then(response => response.json())
        .then(data => {
            const historyList = document.getElementById('history-list');
            historyList.innerHTML = '';
            data.forEach(entry => {
                const li = document.createElement('li');
                li.textContent = `Sum of ${entry.num1} and ${entry.num2} is ${entry.result}`;
                historyList.appendChild(li);
            });
        })
        .catch(error => console.error('Error:', error));
}

// Fetch history on page load
document.addEventListener('DOMContentLoaded', fetchHistory);
