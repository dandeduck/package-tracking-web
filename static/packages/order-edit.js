document.getElementById('package-modal').addEventListener('show.bs.modal', function (event) {
    document.getElementById('origin-address').value = event.relatedTarget.getAttribute('data-bs-origin-address')
    document.getElementById('origin-city').value = event.relatedTarget.getAttribute('data-bs-origin-city')
    document.getElementById('origin-street').value = event.relatedTarget.getAttribute('data-bs-origin-street')
    document.getElementById('origin-street-number').value = event.relatedTarget.getAttribute('data-bs-origin-street-number')
    
    document.getElementById('destination-address').value = event.relatedTarget.getAttribute('data-bs-destination-address')
    document.getElementById('destination-city').value = event.relatedTarget.getAttribute('data-bs-destination-city')
    document.getElementById('destination-street').value = event.relatedTarget.getAttribute('data-bs-destination-street')
    document.getElementById('destination-street-number').value = event.relatedTarget.getAttribute('data-bs-destination-street-number')
    
    document.getElementById('rate').value = event.relatedTarget.getAttribute('data-bs-rate')
    document.getElementById('name').value = event.relatedTarget.getAttribute('data-bs-name')
    document.getElementById('phone-number').value = event.relatedTarget.getAttribute('data-bs-phone-number')
    document.getElementById('notes').value = event.relatedTarget.getAttribute('data-bs-notes')
    document.getElementById('package-id').value = event.relatedTarget.getAttribute('data-bs-package-id')
})