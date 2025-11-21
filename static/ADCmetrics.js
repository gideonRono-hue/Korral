/* SIDEBAR */
const menu = document.getElementById('menu-label');
const sidebar = document.getElementsByClassName('sidebar')[0];

menu.addEventListener('click', function () {
    sidebar.classList.toggle('hide');
});

/* TOGGLE */

let activeOne = false;
let activeTwo = false;
let activeThree = false;

function toggle(toggleClass) {
    let toggle = document.querySelector('.' + toggleClass);

    if (toggleClass === 'toggleOne') {
        activeOne = !activeOne;
        toggle.classList.toggle('active', activeOne);

    } else if (toggleClass === 'toggleTwo') {
        activeTwo = !activeTwo;
        toggle.classList.toggle('active', activeTwo);

    } else if (toggleClass === 'toggleThree') {
        activeThree = !activeThree;
        toggle.classList.toggle('active', activeThree);
    }
}

/* ADC VOLTAGE GAUGE */

function fetchAdcData(pin) {
    return fetch(`/updateAdcData?pin=${pin}`)
        .then((response) => response.json())
        .then(data => {
            return data.adcValue; // Get ADC value from server response
        })
        .catch(error => {
            console.error("Error fetching ADC data:", error);
            return 0; // Return default value (0) if an error occurs
        });
}

function updateAdcGauge(pin, gaugeClass) {
    const gaugeElement = document.querySelector(`.${gaugeClass} .gauge`);

    fetchAdcData(pin)
        .then(adcValue => {
            const normalizedAdcValue = adcValue / 3.3; // Normalize ADC value (assuming max 3.3V)
            setGaugeValue(gaugeElement, normalizedAdcValue, `${adcValue.toFixed(2)} V`);

            // Repeat update every 6 seconds
            setTimeout(() => updateAdcGauge(pin, gaugeClass), 2000);
        });
}

function setGaugeValue(gauge, value, displayValue) {
    if (value < 0 || value > 1) {
        return;
    }

    const angle = value * 180; // Convert normalized value to an angle (0 to 180 degrees)
    gauge.querySelector(".gauge__fill").style.transform = `rotate(${angle}deg)`;
    gauge.querySelector(".gauge__cover").textContent = displayValue; // Display voltage value
}

// Start updating the ADC gauges for three pins
updateAdcGauge(1, 'gauge-card-1'); // Pin 1
updateAdcGauge(2, 'gauge-card-2'); // Pin 2
updateAdcGauge(3, 'gauge-card-3'); // Pin 3

/* LINE CHART */

// Function to update chart data and labels
function updateChart(chart, adc1Data, adc2Data, adc3Data, label) {
    if (chart.data.labels.length >= 30) {
        chart.data.labels.shift();
        chart.data.datasets[0].data.shift();
        chart.data.datasets[1].data.shift();
        chart.data.datasets[2].data.shift();
    }

    chart.data.labels.push(label); // Add new time label
    chart.data.datasets[0].data.push(adc1Data); // Add new ADC 1 data
    chart.data.datasets[1].data.push(adc2Data); // Add new ADC 2 data
    chart.data.datasets[2].data.push(adc3Data); // Add new ADC 3 data
    chart.update();
}

// Function to create a line chart
function createLineChart() {
    const ctx = document.getElementById('lineChart').getContext('2d');
    const lineChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [
                {
                    label: 'ADC Pin 1 (V)',
                    data: [],
                    borderColor: '#C51605',
                    backgroundColor: 'rgba(255, 133, 81, 0.2)',
                    tension: 0.4,
                    fill: true,
                },
                {
                    label: 'ADC Pin 2 (V)',
                    data: [],
                    borderColor: '#F86F03',
                    backgroundColor: 'rgba(255, 184, 77, 0.2)',
                    tension: 0.4,
                    fill: true,
                },
                {
                    label: 'ADC Pin 3 (V)',
                    data: [],
                    borderColor: '#1E90FF',
                    backgroundColor: 'rgba(30, 144, 255, 0.2)',
                    tension: 0.4,
                    fill: true,
                },
            ],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    type: 'category',
                    display: true,
                    grid: {
                        display: false,
                    },
                },
                y: {
                    display: true,
                    grid: {
                        display: true,
                    },
                },
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'bottom',
                },
            },
        },
    });

    return lineChart;
}

// Start updating the line chart every 15 seconds
function startUpdatingChart() {
    const lineChart = createLineChart();

    setInterval(async () => {
        const adc1Data = await fetchAdcData(1);
        const adc2Data = await fetchAdcData(2);
        const adc3Data = await fetchAdcData(3);
        const currentTime = moment().format('HH:mm'); 

        updateChart(lineChart, adc1Data, adc2Data, adc3Data, currentTime);
    }, 700);
}

// Start updating the line chart
startUpdatingChart();
