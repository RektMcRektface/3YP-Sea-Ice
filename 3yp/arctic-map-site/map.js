// app.js
var map = L.map('map').setView([90, 0], 3); // Latitude 90, Longitude 0, Zoom level 3

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

// Example: Adding a marker in the Arctic
var marker = L.marker([90, 0]).addTo(map);
marker.bindPopup("<b>Hello Arctic!</b><br>This is the North Pole.").openPopup();

// Define the coordinates for the Arctic Sea boundary
var arcticSeaCoords = [
    [51.1436, -20], // Starting point
    [75, -20], // Eastern point
    [75, 20], // Near North Pole
    [51.1436, 20], // Near North Pole, western side
    [51.1436, -20] // Closing the loop
];

// Create a polygon from the coordinates and add it to the map
var arcticSeaPolygon = L.polygon(arcticSeaCoords, {
    color: 'blue',      // Outline color
    fillColor: '#add8e6', // Fill color
    fillOpacity: 0.5    // Use a semi-transparent fill
}).addTo(map);

// Optionally, zoom the map to the polygon
map.fitBounds(arcticSeaPolygon.getBounds());

// Add a popup to the polygon
arcticSeaPolygon.bindPopup("Arctic Sea Area");

