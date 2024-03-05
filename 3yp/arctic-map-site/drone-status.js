
// var map; // Declare `map` in the global scope


// document.addEventListener('DOMContentLoaded', async () => {
//     var map = L.map('drone-map').setView([90, 0], 3);
//     L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
//         attribution: '© OpenStreetMap contributors'
//     }).addTo(map);

//     await addDangerMapOverlay(map);

// });

// // Define the coordinates for the Arctic Sea boundary
// var arcticSeaCoords = [
//     [81, -10], // Starting point
//     [83, -10], // Eastern point
//     [83, 10], // Near North Pole
//     [81, 10], // Near North Pole, western side
//     [81, -10] // Closing the loop
// ];

// // Create a polygon from the coordinates and add it to the map
// var arcticSeaPolygon = L.polygon(arcticSeaCoords, {
//     color: 'blue',      // Outline color
//     fillColor: '#add8e6', // Fill color
//     fillOpacity: 0.3    // Use a semi-transparent fill
// }).addTo(map);

// // Optionally, zoom the map to the polygon
// map.fitBounds(arcticSeaPolygon.getBounds());

// // Add a popup to the polygon
// arcticSeaPolygon.bindPopup("Arctic Ocean");
// // Sample danger points data (latitude, longitude, intensity)

var map; // Declare `map` in the global scope

document.addEventListener('DOMContentLoaded', async () => {
    // Initialize the global `map` variable without redeclaring it
    map = L.map('drone-map').setView([90, 0], 3); 
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    await addDangerMapOverlay(map);

    // After map is initialized, add other layers
    addArcticSeaBoundary();

    // Initialize drone markers and statuses after the map has been initialized
    updateDroneMarkers(); // Ensure this function and any similar ones are defined to use the global `map`
    updateDroneStatuses(); // Make sure this doesn't directly require `map` to be passed in

    // Set intervals for refreshing drone markers and statuses
    setInterval(updateDroneStatuses, 10000); // Correct comment to match code: Refresh every 10 seconds
    setInterval(updateDroneMarkers, 10000); // Refresh drone markers every 10 seconds
});

function addArcticSeaBoundary() {
    // Define the coordinates for the Arctic Sea boundary
    var arcticSeaCoords = [
        [81, -10], // Starting point
        [83, -10], // Eastern point
        [83, 10], // Near North Pole
        [81, 10], // Near North Pole, western side
        [81, -10] // Closing the loop
    ];

    // Create a polygon from the coordinates and add it to the map
    var arcticSeaPolygon = L.polygon(arcticSeaCoords, {
        color: 'blue',      // Outline color
        fillColor: '#add8e6', // Fill color
        fillOpacity: 0.3    // Use a semi-transparent fill
    }).addTo(map);

    // Optionally, zoom the map to the polygon
    map.fitBounds(arcticSeaPolygon.getBounds());

    // Add a popup to the polygon
    arcticSeaPolygon.bindPopup("Arctic Ocean");
}


// Sample drone data - replace with real data
var drones = [
    {
        id: "drone1",
        lat: 83.0,
        lng: -10.0,
        battery: "75%",
        status: "Charging",
        speed: "0 km/h",
        height :"0 m",
        signalStrength:"N/A",
        task:"N/A"
    },
    {
        id: "drone2",
        lat: 82.0,
        lng: 0.0,
        battery: "67%",
        status: "Flying and Scanning",
        speed: "45 km/h",
        height: "1200 m",
        signalStrength: "Strong",
        task: "20/100"
    },
    {
        id: "drone3",
        lat: 83.0,
        lng: -10.0,
        battery: "10%",
        status: "Charging",
        speed: "0 km/h", // Assuming 0 since it's charging
        height: "0 m", // Assuming 0 since it's on the ground
        signalStrength: "N/A",
        task:"N/A"
    }
];

// // Call the function to add markers and update statuses
// updateDroneMarkers();
// updateDroneStatuses();

// // For a real application, you might set an interval to refresh the statuses
// setInterval(updateDroneStatuses, 10000); // Refresh every 5 seconds
// setInterval(updateDroneMarkers, 10000); // Refresh every 5 seconds

function updateDroneMarkers() {
    // Clear existing markers
    // Assuming `map` is your Leaflet map instance,
    // and you have a way to track and remove existing markers
    // If you're tracking markers, loop through them here and use map.removeLayer(marker) to clear them

    drones.forEach(drone => {
        // Create a marker for each drone
        var marker = L.marker([drone.lat, drone.lng]).addTo(map);

        // Bind a popup to the marker with detailed information
        marker.bindPopup(`<b>Drone ID: ${drone.id}</b><br>Battery: ${drone.battery}<br>Status: ${drone.status}`);
    });
}

// Function to simulate updating drone statuses (replace this with real data fetching logic)
function updateDroneStatuses() {

    // Update the DOM elements for drone statuses
    document.getElementById('drone1-battery').innerText = drones[0].battery;
    document.getElementById('drone1-current-status').innerText = drones[0].status;
    document.getElementById('drone1-speed').innerText = drones[0].speed;
    document.getElementById('drone1-height').innerText = drones[0].height;
    document.getElementById('drone1-signal-strength').innerText = drones[0].signalStrength;
    document.getElementById('drone1-task').innerText = drones[0].task;

    
    document.getElementById('drone2-battery').innerText = drones[1].battery;
    document.getElementById('drone2-current-status').innerText = drones[1].status;
    document.getElementById('drone2-speed').innerText = drones[1].speed;
    document.getElementById('drone2-height').innerText = drones[1].height;
    document.getElementById('drone2-signal-strength').innerText = drones[1].signalStrength;
    document.getElementById('drone2-task').innerText = drones[1].task;

    // Updates for the new drone
    document.getElementById('drone3-battery').innerText = drones[2].battery;
    document.getElementById('drone3-current-status').innerText = drones[2].status;
    document.getElementById('drone3-speed').innerText = drones[2].speed;
    document.getElementById('drone3-height').innerText = drones[2].height;
    document.getElementById('drone3-signal-strength').innerText = drones[2].signalStrength;
    document.getElementById('drone3-task').innerText = drones[2].task;
}

async function fetchDangerMap() {
    const response = await fetch('danger-map.txt');
    const text = await response.text();
    // Assuming each row is separated by a newline and each value by spaces
    const matrix = text.split('\n').map(row => row.trim().split(',').map(Number));
    return matrix;
}

// Function to add danger map overlay
async function addDangerMapOverlay(map) {
    const dangerMap = await fetchDangerMap(); // Fetch the matrix
    // Define the top-left and bottom-right corners of your map area
    var topLeft = L.latLng(83, -10);
    var bottomRight = L.latLng(81, 10);
    var gridSize = 200; // Simplified grid size for demonstration
    var cellSizeLat = (topLeft.lat - bottomRight.lat) / gridSize;
    var cellSizeLng = (bottomRight.lng - topLeft.lng) / gridSize;

    for (let i = 0; i < gridSize; i++) {
        for (let j = 0; j < gridSize; j++) {
            // Calculate cell boundaries
            var cellBounds = [
                [topLeft.lat - i * cellSizeLat, topLeft.lng + j * cellSizeLng],
                [topLeft.lat - (i + 1) * cellSizeLat, topLeft.lng + (j + 1) * cellSizeLng]
            ];

            // Simplified example to get danger level (1-10)
            // Replace this with actual logic to retrieve danger level from your matrix
            const dangerLevel = dangerMap[i][j];

            // Add rectangle for each grid cell
            L.rectangle(cellBounds, {color: getDangerColor(dangerLevel), weight: 0, fillOpacity: 0.4}).addTo(map);
        }
    }
}

// // Corrected random danger level generation to match the -4 to 2 range
// function addDangerMapOverlay(map) {
//     // Definitions for topLeft, bottomRight, gridSize, cellSizeLat, and cellSizeLng remain unchanged
//     var topLeft = L.latLng(83, -10);
//     var bottomRight = L.latLng(81, 10);
//     var gridSize = 200; // Simplified grid size for demonstration
//     var cellSizeLat = (topLeft.lat - bottomRight.lat) / gridSize;
//     var cellSizeLng = (bottomRight.lng - topLeft.lng) / gridSize;

//     for (let i = 0; i < gridSize; i++) {
//         for (let j = 0; j < gridSize; j++) {
//             var cellBounds = [
//                 [topLeft.lat - i * cellSizeLat, topLeft.lng + j * cellSizeLng],
//                 [topLeft.lat - (i + 1) * cellSizeLat, topLeft.lng + (j + 1) * cellSizeLng]
//             ];

//             // Generate danger level within the correct range
//             var dangerLevel = Math.floor(Math.random() * 7) - 4; // Generates numbers from -4 to 2

//             L.rectangle(cellBounds, {color: getDangerColor(dangerLevel), weight: 1, fillOpacity: 0.2}).addTo(map);
//         }
//     }
// }

// Function to determine color based on danger level
function getDangerColor(value) {
    switch (value) {
        case -4: return '#1a9850'; // Low danger, green
        case -3: return '#66bd63';
        case -2: return '#a6d96a';
        case -1: return '#d9ef8b';
        case 0:  return '#fee08b'; // Neutral, yellow
        case 1:  return '#fdae61';
        case 2:  return '#d73027'; // High danger, red
        default: return '#ddd'; // Default color for undefined values
    }
}




