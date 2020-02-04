(function(angular) {
    let app = angular.module("app");

    app.controller("AdminHomeCtrl", [
        "$http",
        "$scope",
        "$interval",
        function($http, $scope, $interval) {
            let that = this;

            this.users = [];
            this.accommodations = [];
            this.flights = [];

            $scope.today = new Date();
            let tick = function() {
                $scope.clock = Date.now();
            };
            tick();
            $interval(tick, 1000);

            $scope.max = 5;
            $scope.isReadonly = true;

            this.getAllUsers = function() {
                $http.get("api/users").then(
                    function(response) {
                        console.log(response);
                        that.users = response.data;
                    },
                    function(reason) {
                        console.log(reason);
                    }
                );
            };

            this.deleteUser = function(id) {
                $http.delete("api/users/" + id).then(
                    function(response) {
                        console.log(response);
                        that.getAllUsers();
                    },
                    function(reason) {
                        console.log(reason);
                    }
                );
            };

            this.getAllAccommodations = function() {
                $http.get("api/accommodation").then(
                    function(response) {
                        console.log(response);
                        that.accommodations = response.data;
                    },
                    function(reason) {
                        console.log(reason);
                    }
                );
            };

            this.deleteAccommodation = function(id) {
                $http.delete("api/accommodation/" + id).then(
                    function(response) {
                        console.log(response);
                        that.getAllAccommodations();
                    },
                    function(reason) {
                        console.log(reason);
                    }
                );
            };

            this.getAllFlights = function() {
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

            this.deleteFlight = function(id) {
                $http.delete("api/flights/" + id).then(
                    function(response) {
                        console.log(response);
                        that.getAllFlights();
                    },
                    function(reason) {
                        console.log(reason);
                    }
                );
            };

            this.getAllUsers();
            this.getAllAccommodations();
            this.getAllFlights();
        }
    ]);
})(angular);
