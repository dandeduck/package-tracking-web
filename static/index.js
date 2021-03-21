function initAutocomplete() {
    origin = document.querySelector("#destination-address");
    destination = document.querySelector("#origin-address");
    
    options = {
        componentRestrictions: { country: "il" },
        fields: ["address_components", "geometry"],
        types: ["address"],
    };

    new google.maps.places.SearchBox(origin, options);
    new google.maps.places.SearchBox(destination, options);
}