class AutocompleteField {
    constructor(input, city, street, streetNumber) {
        this.input = input;
        this.city = city;
        this.street = street;
        this.streetNumber = streetNumber;

        this.autocomplete = new google.maps.places.Autocomplete(input, {
            componentRestrictions: { country: 'il' },
            types: ['address']
        });
        this.autocomplete.addListener("place_changed", () => this.fillIn(this));
        this.input.onblur = () => this.fillIn(this);
    }

    fillIn(self) {
        const place = self.autocomplete.getPlace();
        let address = new Address(place, self.input.value);

        self.input.value = address.formatted;
        self.city.value = address.city;
        self.street.value = address.street;
        self.streetNumber.value = address.street_number;
    }
}

class Address {
    constructor(place, input) {
        if (typeof place === 'undefined' || typeof place.address_components === 'undefined')
            this.customAddressFormatting(this, input);
        else
            this.extractAddressComponents(this, place);
    }

    customAddressFormatting(self, customInput) {
        const numRegex = /\d+/;

        let components = customInput.split(',');
        let streetNumber;
        let street;
        let city;

        if (components.length == 1)
            city = components[0];
        else {
            if (components[1].charAt(0) === ' ')
                components[1] = components[1].substring(1);

            if (streetNumber = + components[0].match(numRegex)) {
                street = components[0];
                city = components[1];
            }
            else {
                streetNumber = +components[1].match(numRegex);
                street = components[1];
                city = components[0];
            }

            street = street.replace(/[0-9]/g, '').slice(0, -1);
            alert("'" + String(street) + "'");
        }

        street ??= '<no street>';

        if (typeof streetNumber === 'undefined' || streetNumber == '')
            streetNumber = 1;

        self.formatted = customInput;
        self.city = city;
        self.street = street;
        self.street_number = streetNumber;
    }

    extractAddressComponents(self, place) {

        for (const component of place.address_components) {
            const componentType = component.types[0];

            switch (componentType) {
                case "street_number":
                    self.streetNumber = component.long_name;
                    break;

                case "route":
                    self.streetName = component.short_name;
                    break;

                case "locality":
                    self.city = component.long_name;
                    break;
            }
        }

        self.formatted = `${self.streetName} ${self.streetNumber ?? 1}, ${self.city}`;
        self.streetNumber ??= 1;
    }
}

function initAutocomplete() {
    let destination = document.querySelector("#destination-address");
    let destinationCity = document.querySelector('#destination-city');
    let destinationStreet = document.getElementById('destination-street');
    let destinationStreetNumber = document.querySelector('#destination-street-number');

    new AutocompleteField(destination, destinationCity, destinationStreet, destinationStreetNumber);

    let origin = document.querySelector("#origin-address");
    let originCity = document.querySelector('#origin-city');
    let originStreet = document.querySelector('#origin-street');
    let originStreetNumber = document.querySelector('#origin-street-number');

    new AutocompleteField(origin, originCity, originStreet, originStreetNumber);
}
