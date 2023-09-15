// script.js
function confirmDelete() {
    return window.confirm("Are you sure you want to delete this risk?");
}
document.addEventListener('DOMContentLoaded', function() {
    const rows = document.querySelectorAll('tr[data-href]');
    rows.forEach(row => {
        row.addEventListener('mouseover', function() {
            this.classList.add('hover');
        });
        row.addEventListener('mouseout', function() {
            this.classList.remove('hover');
        });
    });
});

function updateBarChart(data) {
    const total = data['Open'] + data['In Progress'] + data['Closed'];
    document.getElementById('bar-open').style.height = `${(data['Open'] / total) * 100}%`;
    document.getElementById('bar-in-progress').style.height = `${(data['In Progress'] / total) * 100}%`;
    document.getElementById('bar-closed').style.height = `${(data['Closed'] / total) * 100}%`;
}

// Update this part of your existing JavaScript
fetch('/api/dashboard_data')
    .then(response => response.json())
    .then(data => {
        updateDashboard(data);
        updateBarChart(data['risk_count_by_status']);
    });

        fetch('/api/dashboard_data')
        .then(response => response.json())
        .then(data => {
            // Get the data from the API
            const { risk_count_by_status } = data;
            
            // Prepare data for the Chart
            const labels = Object.keys(risk_count_by_status);
            const values = Object.values(risk_count_by_status);

            // Initialize the Chart
            var ctx = document.getElementById('myChart').getContext('2d');
            var myChart = new myChart(ctx, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Risks by Status',
                        data: values,
                        backgroundColor: ['red', 'blue', 'green'],
                        borderColor: ['black', 'black', 'black'],
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        });