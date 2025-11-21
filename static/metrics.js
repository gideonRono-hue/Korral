/* SIDEBAR */
const menu = document.getElementById('menu-label');
const sidebar = document.getElementsByClassName('sidebar')[0];

menu.addEventListener('click', function() {
     sidebar.classList.toggle('hide');
})


/* TOGGLE */

let activeOne = false;
let activeTwo = false;
let activeThree = false;
let activeFour = false;

function toggle(toggleClass) {
  let toggle = document.querySelector('.' + toggleClass);

  if (toggleClass === 'toggleOne') {
    activeOne = !activeOne;
    if (activeOne) {
      toggle.classList.add('active');
      fetch('');
    } else {
      toggle.classList.remove('active');
      fetch('');
    }

  } else if (toggleClass === 'toggleTwo') {
    activeTwo = !activeTwo;
    if (activeTwo) {
      toggle.classList.add('active');
      fetch('');
    } else {
      toggle.classList.remove('active');
      fetch('');
    }

  } else if (toggleClass === 'toggleThree') {
    activeThree = !activeThree;
    if (activeThree) {
      toggle.classList.add('active');
      fetch('');
    } else {
      toggle.classList.remove('active');
      fetch('');
    }

  } else if (toggleClass === 'toggleFour') {
    activeFour = !activeFour;
    if (activeFour) {
      toggle.classList.add('active');
      fetch('');
    } else {
      toggle.classList.remove('active');
      fetch('');
    }
  }
}


/* TEMPERATURE GAUGE */

// Function to fetch actual temperature data from the server
function fetchTemperatureData() {
    return fetch(`/updateData`)
        .then((response) => response.json())
        .then(data => {
            return data.readingTemp; // Get temperature value from server response
        })
        .catch(error => {
            console.error("Error fetching temperature data:", error);
            return 0; // Return default value (0) if an error occurs
        });
}
// Function to update the temperature gauge value
function updateTemperatureGauge() {
    const gaugeElement = document.querySelector(".gauge-card-1 .gauge");

    // Fetch actual temperature data from the server using fetchTemperatureData()
    fetchTemperatureData()
        .then(temperatureInCelsius => {
            // Normalize temperature value to a range of 0 to 1 (assuming max 100 degrees Celsius)
            const normalizedTemperature = temperatureInCelsius / 100;

            // Update the temperature gauge value
            setTemperatureGaugeValue(gaugeElement, normalizedTemperature);

            // Repeat update every 6 seconds
            setTimeout(updateTemperatureGauge, 6000);
        });
}

// Function to set the temperature gauge value
function setTemperatureGaugeValue(gauge, value) {
    if (value < 0 || value > 1) {
        return;
    }

    const angle = value * 180; // Convert normalized value to an angle (0 to 180 degrees)
    gauge.querySelector(".gauge__fill").style.transform = `rotate(${angle}deg)`;
    gauge.querySelector(".gauge__cover").textContent = `${Math.round(value * 100)}°C`; // Display temperature value in degrees Celsius
}


// Start updating the temperature gauge every 6 seconds
updateTemperatureGauge();


/* HUMIDITY GAUGE */

// Function to fetch actual humidity data from the server
function fetchHumidityData() {
    return fetch(`/updateData`)
        .then((response) => response.json())
        .then(data => {
            return data.readingHum; // Get humidity value from server response
        })
        .catch(error => {
            console.error("Error fetching humidity data:", error);
            return 0; // Return default value (0) if an error occurs
        });
}

// Function to update the humidity gauge value
function updateHumidityGauge() {
    const gaugeElement = document.querySelector(".gauge-card-2 .gauge");

    // Fetch actual humidity data from the server using fetchHumidityData()
    fetchHumidityData()
        .then(humidityInPercentage => {
            // Normalize humidity value to a range of 0 to 1 (assuming max 100 percent)
            const normalizedHumidity = humidityInPercentage / 100;

            // Update the humidity gauge value
            setHumidityGaugeValue(gaugeElement, normalizedHumidity);

            // Repeat update every 6 seconds
            setTimeout(updateHumidityGauge, 6000);
        });
}

// Function to set the humidity gauge value
function setHumidityGaugeValue(gauge, value) {
    if (value < 0 || value > 1) {
        return;
    }

    const angle = value * 180; // Convert normalized value to an angle (0 to 180 degrees)
    gauge.querySelector(".gauge__fill").style.transform = `rotate(${angle}deg)`;
    gauge.querySelector(".gauge__cover").textContent = `${Math.round(value * 100)}%`; // Display humidity value
}

// Start updating the humidity gauge every 6 seconds
updateHumidityGauge();


/* ALTITUDE GAUGE */

// Function to fetch actual altitude data from the server
function fetchAltitudeData() {
    return fetch(`/updateData`)
        .then((response) => response.json())
        .then(data => {
            return data.readingAlt; // Get altitude value from server response
        })
        .catch(error => {
            console.error("Error fetching altitude data:", error);
            return 0; // Return default value (0) if an error occurs
        });
}
// Function to update the altitude gauge value
function updateAltitudeGauge() {
    const gaugeElement = document.querySelector(".gauge-card-3 .gauge");

    // Fetch actual altitude data from the server using fetchAltitudeData()
    fetchAltitudeData()
        .then(altitudeInMetre => {
            // Normalize altitude value to a range of 0 to 1 (assuming max 2000 meters)
            const normalizedAltitude = altitudeInMetre / 1000;

            // Update the altitude gauge value
            setAltitudeGaugeValue(gaugeElement, normalizedAltitude);

            // Repeat update every 6 seconds
            setTimeout(updateAltitudeGauge, 6000);
        });
}

// Function to set the altitude gauge value
function setAltitudeGaugeValue(gauge, value) {
    if (value < 0 || value > 1) {
        return;
    }

    gauge.querySelector(".gauge__fill").style.transform = `rotate(${value / 2}turn)`;
    gauge.querySelector(".gauge__cover").textContent = `${Math.round(value * 1000)} m`; // Display altitude value in meters
}

// Start updating the altitude gauge every 6 seconds
updateAltitudeGauge();


/* PRESSURE GAUGE */

// Function to fetch actual pressure data from the server
function fetchPressureData() {
    return fetch(`/updateData`)
        .then((response) => response.json())
        .then(data => {
            return data.readingPress; // Get pressure value from server response
        })
        .catch(error => {
            console.error("Error fetching pressure data:", error);
            return 0; // Return default value (0) if an error occurs
        });
}
// Function to update the pressure gauge value
function updatePressureGauge() {
    const gaugeElement = document.querySelector(".gauge-card-4 .gauge");

    // Fetch actual pressure data from the server using fetchPressureData()
    fetchPressureData()
        .then(PressureInHpa => {
            // Normalize pressure value to a range of 0 to 1 (assuming max 6000 hPa)
            const normalizedPressure = PressureInHpa / 6000;

            // Update the pressure gauge value
            setPressureGaugeValue(gaugeElement, normalizedPressure);

            // Repeat update every 6 seconds
            setTimeout(updatePressureGauge, 6000);
        });
}

// Function to set the pressure gauge value
function setPressureGaugeValue(gauge, value) {
    if (value < 0 || value > 1) {
        return;
    }

    gauge.querySelector(".gauge__fill").style.transform = `rotate(${value * 180}deg)`;
    gauge.querySelector(".gauge__cover").textContent = `${(value * 6000).toFixed(2)} hPa`; // Display pressure value in hectopascals
}

// Start updating the pressure gauge every 6 seconds
updatePressureGauge();


/* NOISE LEVEL */

// Function to fetch actual noise data from the server
function fetchNoiseData() {
    return fetch(`/updateNoise`)
        .then((response) => response.json())
        .then(data => {
            return data.readingNoise; // Get noise value from server response
        })
        .catch(error => {
            console.error("Error fetching noise data:", error);
            return 0; // Return default value (0) if an error occurs
        });
}
// Function to update the noise gauge value
function updateNoiseGauge() {
    const gaugeElement = document.querySelector(".gauge-card-6 .gauge");

    // Fetch actual noise data from the server using fetchNoiseData()
    fetchNoiseData()
        .then(noiseIndB => {
            // Normalize noise value to a range of 0 to 1 (assuming max 120 dB)
            const normalizedNoise = noiseIndB / 100;

            // Update the noise gauge value
            setNoiseGaugeValue(gaugeElement, normalizedNoise);

            // Repeat update every 6 seconds
            setTimeout(updateNoiseGauge, 10000);
        });
}

// Function to set the noise gauge value
function setNoiseGaugeValue(gauge, value) {
    if (value < 0 || value > 1) {
        return;
    }

    gauge.querySelector(".gauge__fill").style.transform = `rotate(${value * 180}deg)`;
    gauge.querySelector(".gauge__cover").textContent = `${Math.round(value * 100)} dB`; // Display noise level in dB
}

// Start updating the noise gauge
updateNoiseGauge();



/* LINE CHART */

// Function to update chart data and labels
function updateChart(chart, temperatureData, humidityData, label) {
    // Remove oldest data if the number of data points exceeds a certain limit (e.g., 30 data points)
    if (chart.data.labels.length >= 30) {
        chart.data.labels.shift();
        chart.data.datasets[0].data.shift();
        chart.data.datasets[1].data.shift();
    }

    chart.data.labels.push(label); // Add new time label
    chart.data.datasets[0].data.push(temperatureData); // Add new temperature data
    chart.data.datasets[1].data.push(humidityData); // Add new humidity data
    chart.update();
}

// Function to create a line chart
function createLineChart() {
    const ctx = document.getElementById('lineChart').getContext('2d');
    const lineChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [], // Insert time labels here
            datasets: [
                {
                    label: 'Temperature (°C)',
                    data: [], // Temperature data will be filled dynamically
                    borderColor: '#C51605',
                    backgroundColor: 'rgba(255, 133, 81, 0.2)',
                    tension: 0.4,
                    fill: true,
                },
                {
                    label: 'Humidity (%)',
                    data: [], // Humidity data will be filled dynamically
                    borderColor: '#F86F03',
                    backgroundColor: 'rgba(255, 184, 77, 0.2)',
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
                    type: 'category', // If using time labels
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

    // Update chart data and labels every 15 seconds
    setInterval(async () => {
        // Get current temperature and humidity data from simulation
        const temperatureData = await getActualTemperatureData();
        const humidityData = await getActualHumidityData();
        const currentTime = moment().format('HH:mm'); // Get current time and format as 'Hour:Minute'

        updateChart(lineChart, temperatureData, humidityData, currentTime);
    }, 15000); // Set interval to 5000 milliseconds (5 seconds)
}

// Function to get actual temperature data from the server
async function getActualTemperatureData() {
    const response = await fetch('/updateData');
    const data = await response.json();
    return data.readingTemp;
}

// Function to get actual humidity data from the server
async function getActualHumidityData() {
    const response = await fetch('/updateData');
    const data = await response.json();
    return data.readingHum;
}

// Start updating the line chart
startUpdatingChart();
