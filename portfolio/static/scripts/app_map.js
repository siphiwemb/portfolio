let map;

function initMap() {

  const xhttp = new XMLHttpRequest();
  xhttp.open("GET", "/portfolio/get-all-users/", false);
  xhttp.send();

  users = JSON.parse(xhttp.responseText);

  const mapOptions = {
    zoom: 4,
    center: { lat: parseFloat(users[0].latitude), lng: parseFloat(users[0].longitude) },
  };

  map = new google.maps.Map(document.getElementById("map"), mapOptions);

  users.map(obj=>{

    const marker = new google.maps.Marker({
      position: { lat: parseFloat(obj.latitude), lng: parseFloat(obj.longitude) },
      map: map,
    });
      
    const infowindow = new google.maps.InfoWindow({
      content: `
        <p>Name: ${obj.first_name}</p>
        <p>Surname: ${obj.last_name}</p>
        <p>Surburb: ${obj.surburb}</p>
        <p>City: ${obj.city}</p>
      `,
    });
  
    google.maps.event.addListener(marker, "click", () => {
      infowindow.open(map, marker);
    });
  });

  
}