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
            this.cities = [];

            this.newFlight = {
                airlines_id: 44,
                flight_types_id: 1,
                flight_classes_id: 1,
                origin: 1392685764,
                destination: 1392172935,
                source_airport: 2359,
                destination_airport: 2352,
                ticket_price: 0.0,
                aprox_duration: 0,
                seats_available: 0
            };

            this.getAllAirlines = function() {
                $http.get("api/airlines").then(
                    function(response) {
                        console.log(response);
                        that.airlines = response.data;
                    },
                    function(reason) {
                        console.log(reason);
                    }
                );
            };

            this.getFlightTypes = function() {
                $http.get("api/flight/types").then(
                    function(response) {
                        console.log(response);
                        that.flightTypes = response.data;
                    },
                    function(reason) {
                        console.log(reason);
                    }
                );
            };

            this.getFlightClasses = function() {
                $http.get("api/flight/classes").then(
                    function(response) {
                        console.log(response);
                        that.flightClasses = response.data;
                    },
                    function(reason) {
                        console.log(reason);
                    }
                );
            };

            this.getAllAirports = function() {
                $http.get("api/airports").then(
                    function(response) {
                        console.log(response);
                        that.airports = response.data;
                    },
                    function(reason) {
                        console.log(reason);
                    }
                );
            };

            this.getCities = function() {
                $http.get("/api/cities").then(
                    function(response) {
                        console.log(response);
                        that.cities = response.data;
                    },
                    function(reason) {
                        console.log(reason);
                    }
                );
            };

            this.addFlight = function() {
                $http.post("api/flights", that.newFlight).then(
                    function(response) {
                        console.log(response);
                        $state.go("dashboard.admin_home");
                    },
                    function(reason) {
                        console.log(reason);
                    }
                );
            };

            this.getFlight = function(id) {
                $http.get("api/flights/" + id).then(
                    function(response) {
                        console.log(response);
                        that.newFlight = response.data;
                    },
                    function(reason) {
                        console.log(reason);
                    }
                );
            };

            this.editFlight = function(id) {
                $http.put("api/flights/edit/" + id, that.newFlight).then(
                    function(response) {
                        console.log(response);
                        $state.go("dashboard.admin_home");
                    },
                    function(reason) {
                        console.log(reason);
                    }
                );
            };

            this.save = function() {
                if ($stateParams["id"]) {
                    that.editFlight($stateParams["id"]);
                } else {
                    that.addFlight();
                }
            };

            if ($stateParams["id"]) {
                that.getFlight($stateParams["id"]);
            }

            this.getAllAirlines();
            this.getFlightTypes();
            this.getFlightClasses();
            this.getAllAirports();
            this.getCities();
        }
    ]);
})(angular);
