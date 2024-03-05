fetch('danger-map.txt')
  .then(response => response.text())
  .then(text => console.log(text))
  .catch(error => console.error('Fetch error:', error));
