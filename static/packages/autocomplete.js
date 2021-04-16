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
        self.streetNumber.value = address.streetNumber;
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
        let match = customInput.match(/^(\w+\s?\w*)\s*(?:(\d*)\s*)?(?:,\s*(\w+\s?\w*)?\s*)?$/);
        let city = '';
        let street = '';
        let streetNumber = '';

        if (match == null) {
            return;
        }

        if (match[2] == null && match[3] == null) {
            city = match[1];
        }
        else if (match[3] == null) {
            street = match[1];
            streetNumber = match[2];
        }
        else if (match[2] == null) {
            street = match[1];
            city = match[3];
        } else {
            street = match[1];
            number = match[2];
            city = match[3];
        }

        self.formatted = customInput;
        self.city = city;
        self.street = street;
        self.streetNumber = streetNumber;
    }

    extractAddressComponents(self, place) {
        for (const component of place.address_components) {
            const componentType = component.types[0];

            switch (componentType) {
                case "street_number":
                    self.streetNumber = component.long_name;
                    break;

                case "route":
                    self.street = component.short_name;
                    break;

                case "locality":
                    self.city = component.long_name;
                    break;
            }
        }

        self.streetNumber ??= '';
        self.formatted = `${self.street} ${self.streetNumber}, ${self.city}`;
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
