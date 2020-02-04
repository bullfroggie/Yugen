(function(angular) {
    let app = angular.module("app");

    app.controller("FlightsCtrl", [
        "$http",
        "$state",
        function($http, $state) {
            let that = this;

            this.flights = [];
            this.flightTicket = {
                flights_id: null,
                users_id: null
            };

            this.from = null;
            this.to = null;

            this.getFlights = function() {
                $http.get("api/flights").then(
                    function(response) {
                        console.log(response);
                        that.flights = response.data;
                    },
                    function(reason) {
                        console.log(reason);
                    }
                );
            };

            this.searchFlight = function() {
                if (that.from == null || that.to == null) {
                    return;
                }

                $http.get("api/flights/search/" + that.from + "/" + that.to).then(
                    function(response) {
                        console.log(response);
                        that.flights = response.data;
                    },
                    function(reason) {
                        console.log(reason);
                    }
                );
            };

            this.getUser = function() {
                $http.get("api/user").then(
                    function(response) {
                        console.log(response);
                        that.flightTicket.users_id = response.data.id;
                    },
                    function(reason) {
                        console.log(reason);
                    }
                );
            };

            this.purchaseTicket = function(id) {
                that.flightTicket.flights_id = id;
                $http.post("api/flights/ticket", that.flightTicket).then(
                    function(response) {
                        console.log(response);
                        $state.go("dashboard.reservations_and_tickets");
                    },
                    function(reason) {
                        console.log(reason);
                    }
                );
            };

            this.getUser();
        }
    ]);
})(angular);
