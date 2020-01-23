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

            $scope.today = new Date();
            let tick = function() {
                $scope.clock = Date.now();
            };
            tick();
            $interval(tick, 1000);

            $scope.max = 5;
            $scope.isReadonly = true;

            this.getAllUsers = function() {
                $http.get("/api/users").then(
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
                $http.delete("/api/users/" + id).then(
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
                $http.get("/api/accommodation").then(
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
                $http.delete("/api/accommodation/" + id).then(
                    function(response) {
                        console.log(response);
                        that.getAllAccommodations();
                    },
                    function(reason) {
                        console.log(reason);
                    }
                );
            };

            this.getAllUsers();
            this.getAllAccommodations();
        }
    ]);
})(angular);
