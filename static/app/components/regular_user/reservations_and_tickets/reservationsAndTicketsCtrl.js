(function(angular) {
    let app = angular.module("app");

    app.controller("ReservationsAndTicketsCtrl", [
        "$http",
        "$scope",
        function($http, $scope) {
            let that = this;

            this.tickets = [];
            this.reservations = [];

            this.userID = null;

            $scope.max = 5;
            $scope.isReadonly = true;

            this.getUser = function() {
                $http.get("api/user").then(
                    function(response) {
                        console.log(response);
                        that.userID = response.data.id;
                        that.getTickets();
                        that.getReservations();
                    },
                    function(reason) {
                        console.log(reason);
                    }
                );
            };

            this.getTickets = function() {
                $http.get("api/tickets/" + that.userID).then(
                    function(response) {
                        console.log(response);
                        that.tickets = response.data;
                    },
                    function(reason) {
                        console.log(reason);
                    }
                );
            };

            this.deleteTicket = function(flight_id, ticket_id) {
                $http.delete("api/tickets/" + flight_id + "/" + ticket_id).then(
                    function(response) {
                        console.log(response);
                        that.getTickets();
                    },
                    function(reason) {
                        console.log(reason);
                    }
                );
            };

            this.getReservations = function() {
                $http.get("api/reservations/" + that.userID).then(
                    function(response) {
                        console.log(response);
                        that.reservations = response.data;
                    },
                    function(reason) {
                        console.log(reason);
                    }
                );
            };

            this.deleteReservation = function(accommodation_id, reservation_id) {
                $http.delete("api/reservations/" + accommodation_id + "/" + reservation_id).then(
                    function(response) {
                        console.log(response);
                        that.getReservations();
                    },
                    function(reason) {
                        console.log(reason);
                    }
                );
            };

            that.getUser();
        }
    ]);
})(angular);
