class XSDTripListRow {
    constructor(row) {
        this.tripNavigate = this.tripNavigate.bind(this);
        this.row = row;
        const linkEl = row.querySelector('[data-trip-link]');
        if (linkEl) {
            this.url = linkEl.href;
            this.row.addEventListener('click', this.tripNavigate);
        }
    }

    tripNavigate() {
        return window.location = this.url;
    }
}

class XSDTripList {
    constructor() {
        this.tableEl = document.getElementById('xsd_trip-list');
        this.rows = [];
        for (const row of Array.from(this.tableEl.querySelectorAll('[data-trip-row]'))) {
            this.rows.push(new XSDTripListRow(row));
        }
    }
}

$(document).ready(function () {
    if (document.getElementById('xsd_trip-list')) {
        const tripList = new XSDTripList();
        return window.xtl = tripList;
    }
});
