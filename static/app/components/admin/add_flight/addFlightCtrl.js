(function(angular) {
    let app = angular.module("app");

    app.controller("AddFlightCtrl", [
        "$http",
        "$state",
        "$stateParams",
        function($http, $state, $stateParams) {
            let that = this;

            this.airlines = [];
            this.flightTypes = [];
            this.flightClasses = [];
            this.airports = [];

            this.newFlight = {
                airlines_id: null,
                flight_types_id: null,
                flight_classes_id: null,
                origin: null,
                destination: null,
                source_airport: null,
                destination_airport: null,
                aprox_duration: null
            };
        }
    ]);
})(angular);
